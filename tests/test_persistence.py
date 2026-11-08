from datetime import UTC, datetime
from decimal import Decimal

import pytest

from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import InvalidDataFileError
from controle_estoque.domain.models import Movement, Product
from controle_estoque.application.services import StockReconciliationService
from controle_estoque.infrastructure.persistence.repositories import JsonMovementRepository, JsonProductRepository, _sku_hash


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 11, 7, 15, 30, tzinfo=UTC)


def test_product_is_persisted_and_found_after_repository_recreation(tmp_path, now: datetime) -> None:
    product = Product(" sku-001 ", "Teclado", None, "Periféricos", Decimal("10"), Decimal("20"), 0, now, now)
    JsonProductRepository(tmp_path).save(product)

    loaded = JsonProductRepository(tmp_path).get_by_sku("SKU-001")

    assert loaded == product
    assert list(tmp_path.rglob("*.tmp")) == []


def test_sku_registry_is_rebuildable(tmp_path, now: datetime) -> None:
    repository = JsonProductRepository(tmp_path)
    product = Product("SKU-001", "Teclado", None, None, None, None, 0, now, now)
    repository.save(product)
    for registry_file in (tmp_path / "products" / "indexes" / "sku_registry").glob("*.json"):
        registry_file.unlink()

    repository.rebuild_indexes()

    assert repository.get_by_sku("SKU-001") == product


def test_rebuilding_product_indexes_removes_obsolete_shards(tmp_path, now: datetime) -> None:
    repository = JsonProductRepository(tmp_path)
    sku = "SKU-001"
    repository.save(Product(sku, "Teclado", None, None, None, None, 0, now, now))
    obsolete_prefix = "ff" if _sku_hash(sku)[:2] != "ff" else "00"
    obsolete_shard = tmp_path / "products" / "indexes" / "sku_registry" / f"{obsolete_prefix}.json"
    obsolete_shard.write_text('{"REMOVED": "products/records/none.json"}', encoding="utf-8")

    repository.rebuild_indexes()

    assert not obsolete_shard.exists()


def test_movement_index_is_rebuildable_and_filters_by_sku(tmp_path, now: datetime) -> None:
    repository = JsonMovementRepository(tmp_path)
    movement = Movement("MOV-001", "SKU-001", MovementType.ENTRY, 5, "Reposição", now, now)
    repository.save(movement)
    for index_file in (tmp_path / "movements" / "indexes" / "by_product").glob("*.json"):
        index_file.unlink()

    repository.rebuild_indexes()

    assert repository.list_by_sku("sku-001") == [movement]


def test_invalid_json_reports_affected_path(tmp_path) -> None:
    records_dir = tmp_path / "products" / "records" / "aa"
    records_dir.mkdir(parents=True)
    invalid_file = records_dir / "invalid.json"
    invalid_file.write_text("{invalid", encoding="utf-8")

    with pytest.raises(InvalidDataFileError) as error:
        JsonProductRepository(tmp_path).list_all()

    assert str(invalid_file) in str(error.value)


def test_stock_cache_is_reconciled_from_active_movements(tmp_path, now: datetime) -> None:
    products = JsonProductRepository(tmp_path)
    movements = JsonMovementRepository(tmp_path)
    products.save(Product("SKU-001", "Teclado", None, None, None, None, 99, now, now))
    movements.save(Movement("MOV-001", "SKU-001", MovementType.ENTRY, 8, None, now, now))
    movements.save(Movement("MOV-002", "SKU-001", MovementType.EXIT, 3, None, now, now))
    movements.save(Movement("MOV-003", "SKU-001", MovementType.ENTRY, 5, None, now, now, is_deleted=True))

    reconciled = StockReconciliationService(products, movements).reconcile_product("sku-001")

    assert reconciled.current_stock == 5
    assert products.get_by_sku("SKU-001").current_stock == 5
