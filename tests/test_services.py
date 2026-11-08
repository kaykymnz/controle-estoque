from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from controle_estoque.application.services import MovementService, ProductService
from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import DuplicateSkuError, InsufficientStockError, ValidationError
from controle_estoque.infrastructure.persistence.repositories import JsonMovementRepository, JsonProductRepository


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 11, 7, 16, 0, tzinfo=UTC)


@pytest.fixture
def services(tmp_path, now: datetime) -> tuple[ProductService, MovementService, JsonProductRepository, JsonMovementRepository]:
    products = JsonProductRepository(tmp_path)
    movements = JsonMovementRepository(tmp_path)
    return (
        ProductService(products, movements, clock=lambda: now),
        MovementService(products, movements, clock=lambda: now),
        products,
        movements,
    )


def test_creates_automatic_sku(services) -> None:
    _, _, product_repository, movement_repository = services
    automatic_products = ProductService(
        product_repository, movement_repository,
        uuid_factory=lambda: UUID("12345678-0000-0000-0000-000000000000"),
    )

    assert automatic_products.create("Teclado").sku == "PRD-12345678"


def test_automatic_sku_retries_after_collision(services) -> None:
    _, _, product_repository, movement_repository = services
    first_uuid = UUID("12345678-0000-0000-0000-000000000000")
    second_uuid = UUID("87654321-0000-0000-0000-000000000000")
    product_repository.save(
        ProductService(product_repository, movement_repository, uuid_factory=lambda: first_uuid).create("Existente")
    )
    generated_values = iter([first_uuid, second_uuid])
    products = ProductService(product_repository, movement_repository, uuid_factory=lambda: next(generated_values))

    assert products.create("Novo").sku == "PRD-87654321"


def test_edits_only_permitted_product_data(services) -> None:
    products, _, _, _ = services
    sku = products.create("Teclado").sku

    updated = products.update(sku, "Teclado RGB", "ABNT2", "Periféricos", Decimal("50"), Decimal("90"))

    assert (updated.sku, updated.current_stock, updated.name, updated.cost_price) == (
        sku, 0, "Teclado RGB", Decimal("50")
    )


def test_filters_products_by_individual_columns(services) -> None:
    products, _, _, _ = services
    first = products.create("Teclado")
    products.create("Mouse", category="Periféricos")

    assert products.list_products(sku=first.sku) == [first]
    assert [product.name for product in products.list_products(name="mouse")] == ["Mouse"]
    assert [product.name for product in products.list_products(category="perif")] == ["Mouse"]


def test_entry_exit_edit_and_cancel_recalculate_stock(services) -> None:
    products, movements, product_repository, _ = services
    sku = products.create("Teclado").sku
    entry = movements.create(sku, MovementType.ENTRY, 10)
    exit_movement = movements.create(sku, MovementType.EXIT, 4)

    updated_exit = movements.update(exit_movement.movement_id, MovementType.EXIT, 3, "Ajuste")
    cancelled = movements.cancel(updated_exit.movement_id)

    assert product_repository.get_by_sku(sku).current_stock == 10
    assert entry.is_deleted is False
    assert cancelled.is_deleted is True


def test_rejects_exit_that_makes_stock_negative(services) -> None:
    products, movements, _, _ = services
    sku = products.create("Teclado").sku

    with pytest.raises(InsufficientStockError):
        movements.create(sku, MovementType.EXIT, 1)


def test_cancelling_entry_is_blocked_when_it_makes_stock_negative(services) -> None:
    products, movements, _, _ = services
    sku = products.create("Teclado").sku
    entry = movements.create(sku, MovementType.ENTRY, 5)
    movements.create(sku, MovementType.EXIT, 5)

    with pytest.raises(InsufficientStockError):
        movements.cancel(entry.movement_id)


def test_product_with_positive_stock_cannot_be_deleted_and_deleted_product_rejects_new_movement(services) -> None:
    products, movements, _, _ = services
    product = products.create("Teclado")
    sku = product.sku
    movements.create(sku, MovementType.ENTRY, 1)
    with pytest.raises(InsufficientStockError):
        products.delete(sku)

    movements.create(sku, MovementType.EXIT, 1)
    deleted = products.delete(sku)
    assert deleted.is_deleted is True
    with pytest.raises(ValidationError, match="excluído"):
        movements.create(sku, MovementType.ENTRY, 1)
