import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from controle_estoque.domain.exceptions import InvalidDataFileError


def read_json(path: Path) -> dict[str, Any]:
    """Lê um objeto JSON e informa o caminho quando os dados forem inválidos."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as error:
        raise InvalidDataFileError(str(path), str(error)) from error

    if not isinstance(data, dict):
        raise InvalidDataFileError(str(path), "o conteúdo deve ser um objeto JSON")
    return data


def write_json_atomically(path: Path, data: dict[str, Any]) -> None:
    """Grava JSON em arquivo temporário e substitui o destino ao final."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, ensure_ascii=False, indent=2)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
    except OSError:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
