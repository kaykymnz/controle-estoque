from datetime import UTC, datetime
from decimal import Decimal

import pytest

from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import ValidationError
from controle_estoque.domain.models import Movement, Product, normalize_sku


def test_normalize_sku_removes_external_whitespace_and_uppercases() -> None:
    assert normalize_sku("  sku-001  ") == "SKU-001"


def test_product_requires_name() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError, match="Nome"):
        Product("SKU-1", " ", None, None, None, None, 0, now, now)


def test_product_rejects_negative_price() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError, match="Preço de custo"):
        Product("SKU-1", "Produto", None, None, Decimal("-0.01"), None, 0, now, now)


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_movement_requires_positive_integer_quantity(quantity: object) -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError, match="inteiro positivo"):
        Movement("MOV-1", "sku-1", MovementType.ENTRY, quantity, None, now, now)  # type: ignore[arg-type]
