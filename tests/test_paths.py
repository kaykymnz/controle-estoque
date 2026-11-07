from pathlib import Path

from controle_estoque.app import paths


def test_development_data_dir_is_project_data_directory(monkeypatch) -> None:
    monkeypatch.setattr(paths.sys, "frozen", False, raising=False)

    assert paths.resolve_data_dir() == paths.project_root() / "data"


def test_ensure_data_dir_creates_directory(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "data"
    monkeypatch.setattr(paths, "resolve_data_dir", lambda: target)

    assert paths.ensure_data_dir() == target
    assert target.is_dir()
