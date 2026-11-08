from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import InvalidDataFileError, ValidationError
from controle_estoque.domain.models import Movement, Product


def _timestamp_to_text(timestamp: datetime | None) -> str | None:
    return timestamp.isoformat() if timestamp is not None else None


def _timestamp_from_text(value: object, path: str, field: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidDataFileError(path, f"campo '{field}' deve ser texto ISO 8601")
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError as error:
        raise InvalidDataFileError(path, f"campo '{field}' contém data inválida") from error
    if timestamp.tzinfo is None:
        raise InvalidDataFileError(path, f"campo '{field}' deve conter timezone")
    return timestamp


def _price_from_text(value: object, path: str, field: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InvalidDataFileError(path, f"campo '{field}' deve ser texto decimal")
    try:
        return Decimal(value)
    except InvalidOperation as error:
        raise InvalidDataFileError(path, f"campo '{field}' contém decimal inválido") from error


def product_to_dict(product: Product) -> dict[str, Any]:
    return {
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "cost_price": f"{product.cost_price:.2f}" if product.cost_price is not None else None,
        "sale_price": f"{product.sale_price:.2f}" if product.sale_price is not None else None,
        "current_stock": product.current_stock,
        "created_at": _timestamp_to_text(product.created_at),
        "updated_at": _timestamp_to_text(product.updated_at),
        "is_deleted": product.is_deleted,
        "deleted_at": _timestamp_to_text(product.deleted_at),
    }


def product_from_dict(data: dict[str, Any], path: str) -> Product:
    try:
        return Product(
            sku=data["sku"],
            name=data["name"],
            description=data.get("description"),
            category=data.get("category"),
            cost_price=_price_from_text(data.get("cost_price"), path, "cost_price"),
            sale_price=_price_from_text(data.get("sale_price"), path, "sale_price"),
            current_stock=data["current_stock"],
            created_at=_timestamp_from_text(data["created_at"], path, "created_at"),
            updated_at=_timestamp_from_text(data["updated_at"], path, "updated_at"),
            is_deleted=data.get("is_deleted", False),
            deleted_at=_timestamp_from_text(data.get("deleted_at"), path, "deleted_at"),
        )
    except (KeyError, TypeError, ValidationError) as error:
        raise InvalidDataFileError(path, f"registro de produto inválido: {error}") from error


def movement_to_dict(movement: Movement) -> dict[str, Any]:
    return {
        "movement_id": movement.movement_id,
        "sku": movement.sku,
        "type": movement.type.value,
        "quantity": movement.quantity,
        "note": movement.note,
        "created_at": _timestamp_to_text(movement.created_at),
        "updated_at": _timestamp_to_text(movement.updated_at),
        "is_deleted": movement.is_deleted,
        "deleted_at": _timestamp_to_text(movement.deleted_at),
    }


def movement_from_dict(data: dict[str, Any], path: str) -> Movement:
    try:
        return Movement(
            movement_id=data["movement_id"],
            sku=data["sku"],
            type=MovementType(data["type"]),
            quantity=data["quantity"],
            note=data.get("note"),
            created_at=_timestamp_from_text(data["created_at"], path, "created_at"),
            updated_at=_timestamp_from_text(data["updated_at"], path, "updated_at"),
            is_deleted=data.get("is_deleted", False),
            deleted_at=_timestamp_from_text(data.get("deleted_at"), path, "deleted_at"),
        )
    except (KeyError, TypeError, ValueError, ValidationError) as error:
        raise InvalidDataFileError(path, f"registro de movimentação inválido: {error}") from error
