import os
import sys
from pathlib import Path


APP_NAME = "ControleEstoque"


def project_root() -> Path:
    """Retorna a raiz do repositório durante o desenvolvimento."""
    return Path(__file__).resolve().parents[3]


def resolve_data_dir() -> Path:
    """Resolve o diretório gravável conforme desenvolvimento ou executável."""
    if getattr(sys, "frozen", False):
        local_app_data = (
            Path(os.environ["LOCALAPPDATA"])
            if os.environ.get("LOCALAPPDATA")
            else Path.home() / "AppData" / "Local"
        )
        return local_app_data / APP_NAME / "data"
    return project_root() / "data"


def ensure_data_dir() -> Path:
    data_dir = resolve_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
