import hashlib
from collections import defaultdict
from pathlib import Path

from controle_estoque.domain.models import Movement, Product, normalize_sku
from controle_estoque.infrastructure.persistence.json_store import read_json, write_json_atomically
from controle_estoque.infrastructure.persistence.serializers import (
    movement_from_dict,
    movement_to_dict,
    product_from_dict,
    product_to_dict,
)


def _sku_hash(sku: str) -> str:
    return hashlib.sha256(normalize_sku(sku).encode("utf-8")).hexdigest()


class JsonProductRepository:
    """Repositório de produtos em registros JSON individuais."""

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._records_dir = data_dir / "products" / "records"
        self._registry_dir = data_dir / "products" / "indexes" / "sku_registry"

    def _record_path(self, sku: str) -> Path:
        digest = _sku_hash(sku)
        return self._records_dir / digest[:2] / f"{digest}.json"

    def _registry_path(self, sku: str) -> Path:
        return self._registry_dir / f"{_sku_hash(sku)[:2]}.json"

    def get_by_sku(self, sku: str) -> Product | None:
        sku = normalize_sku(sku)
        registry_path = self._registry_path(sku)
        relative_path: object = None
        if registry_path.exists():
            relative_path = read_json(registry_path).get(sku)
        record_path = self._data_dir / relative_path if isinstance(relative_path, str) else self._record_path(sku)
        if not record_path.exists():
            return None
        product = product_from_dict(read_json(record_path), str(record_path))
        return product if product.sku == sku else None

    def save(self, product: Product) -> None:
        record_path = self._record_path(product.sku)
        write_json_atomically(record_path, product_to_dict(product))

        registry_path = self._registry_path(product.sku)
        registry = read_json(registry_path) if registry_path.exists() else {}
        registry[product.sku] = record_path.relative_to(self._data_dir).as_posix()
        write_json_atomically(registry_path, registry)

    def list_all(self) -> list[Product]:
        if not self._records_dir.exists():
            return []
        return [
            product_from_dict(read_json(path), str(path))
            for path in sorted(self._records_dir.glob("*/*.json"))
        ]

    def rebuild_indexes(self) -> None:
        shards: dict[str, dict[str, str]] = defaultdict(dict)
        for product in self.list_all():
            record_path = self._record_path(product.sku)
            shards[_sku_hash(product.sku)[:2]][product.sku] = record_path.relative_to(self._data_dir).as_posix()
        desired_paths = {self._registry_dir / f"{prefix}.json" for prefix in shards}
        for prefix, entries in shards.items():
            write_json_atomically(self._registry_dir / f"{prefix}.json", entries)
        if self._registry_dir.exists():
            for path in self._registry_dir.glob("*.json"):
                if path not in desired_paths:
                    path.unlink()


class JsonMovementRepository:
    """Repositório de movimentações e índice derivado por produto."""

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._records_dir = data_dir / "movements" / "records"
        self._index_dir = data_dir / "movements" / "indexes" / "by_product"

    def _record_path(self, movement: Movement) -> Path:
        timestamp = movement.created_at
        return self._records_dir / f"{timestamp.year:04d}" / f"{timestamp.month:02d}" / f"{movement.movement_id}.json"

    def _index_path(self, sku: str) -> Path:
        return self._index_dir / f"{_sku_hash(sku)[:2]}.json"

    def get_by_id(self, movement_id: str) -> Movement | None:
        if not self._records_dir.exists():
            return None
        for path in self._records_dir.glob("*/*/*.json"):
            movement = movement_from_dict(read_json(path), str(path))
            if movement.movement_id == movement_id:
                return movement
        return None

    def save(self, movement: Movement) -> None:
        record_path = self._record_path(movement)
        write_json_atomically(record_path, movement_to_dict(movement))

        index_path = self._index_path(movement.sku)
        index = read_json(index_path) if index_path.exists() else {}
        paths = index.setdefault(movement.sku, [])
        relative_path = record_path.relative_to(self._data_dir).as_posix()
        if not isinstance(paths, list):
            paths = []
            index[movement.sku] = paths
        if relative_path not in paths:
            paths.append(relative_path)
        write_json_atomically(index_path, index)

    def list_all(self) -> list[Movement]:
        if not self._records_dir.exists():
            return []
        return [
            movement_from_dict(read_json(path), str(path))
            for path in sorted(self._records_dir.glob("*/*/*.json"))
        ]

    def list_by_sku(self, sku: str) -> list[Movement]:
        sku = normalize_sku(sku)
        index_path = self._index_path(sku)
        if not index_path.exists():
            return []
        paths = read_json(index_path).get(sku, [])
        if not isinstance(paths, list):
            return []
        movements: list[Movement] = []
        for relative_path in paths:
            if not isinstance(relative_path, str):
                continue
            path = self._data_dir / relative_path
            if not path.exists():
                continue
            movement = movement_from_dict(read_json(path), str(path))
            if movement.sku == sku:
                movements.append(movement)
        return movements

    def rebuild_indexes(self) -> None:
        shards: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
        for movement in self.list_all():
            record_path = self._record_path(movement)
            shards[_sku_hash(movement.sku)[:2]][movement.sku].append(
                record_path.relative_to(self._data_dir).as_posix()
            )
        desired_paths = {self._index_dir / f"{prefix}.json" for prefix in shards}
        for prefix, entries in shards.items():
            write_json_atomically(self._index_dir / f"{prefix}.json", dict(entries))
        if self._index_dir.exists():
            for path in self._index_dir.glob("*.json"):
                if path not in desired_paths:
                    path.unlink()
