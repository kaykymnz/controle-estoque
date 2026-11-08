from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import ValidationError


def normalize_sku(sku: str) -> str:
    """Remove espaços externos e normaliza o SKU para maiúsculas."""
    normalized = sku.strip().upper()
    if not normalized:
        raise ValidationError("SKU é obrigatório.")
    return normalized


def validate_price(value: Decimal | None, field_name: str) -> None:
    if value is not None and value < Decimal("0"):
        raise ValidationError(f"{field_name} não pode ser negativo.")


@dataclass(frozen=True, slots=True)
class Product:
    sku: str
    name: str
    description: str | None
    category: str | None
    cost_price: Decimal | None
    sale_price: Decimal | None
    current_stock: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "sku", normalize_sku(self.sku))
        if not self.name.strip():
            raise ValidationError("Nome do produto é obrigatório.")
        if self.current_stock < 0:
            raise ValidationError("Saldo atual não pode ser negativo.")
        validate_price(self.cost_price, "Preço de custo")
        validate_price(self.sale_price, "Preço de venda")


@dataclass(frozen=True, slots=True)
class Movement:
    movement_id: str
    sku: str
    type: MovementType
    quantity: int
    note: str | None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "sku", normalize_sku(self.sku))
        if not self.movement_id.strip():
            raise ValidationError("Identificador da movimentação é obrigatório.")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValidationError("Quantidade deve ser um inteiro positivo.")
