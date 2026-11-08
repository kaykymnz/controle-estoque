from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from controle_estoque.application.interfaces import MovementRepository, ProductRepository
from controle_estoque.domain.enums import MovementType
from controle_estoque.domain.exceptions import (
    DuplicateSkuError,
    InsufficientStockError,
    MovementNotFoundError,
    ProductNotFoundError,
    ValidationError,
)
from controle_estoque.domain.models import Movement, Product, normalize_sku


class StockReconciliationService:
    """Recalcula o cache de saldo a partir das movimentações canônicas ativas."""

    def __init__(self, products: ProductRepository, movements: MovementRepository) -> None:
        self._products = products
        self._movements = movements

    def reconcile_product(self, sku: str) -> Product:
        normalized_sku = normalize_sku(sku)
        product = self._products.get_by_sku(normalized_sku)
        if product is None:
            raise ProductNotFoundError(f"Produto não encontrado: {normalized_sku}")

        stock = sum(
            movement.quantity if movement.type is MovementType.ENTRY else -movement.quantity
            for movement in self._movements.list_by_sku(normalized_sku)
            if not movement.is_deleted
        )
        reconciled = replace(product, current_stock=stock, updated_at=datetime.now(UTC))
        self._products.save(reconciled)
        return reconciled

    def reconcile_all(self) -> list[Product]:
        return [self.reconcile_product(product.sku) for product in self._products.list_all()]


class ProductService:
    """Casos de uso para cadastro, edição e exclusão lógica de produtos."""

    def __init__(
        self,
        products: ProductRepository,
        movements: MovementRepository,
        clock: Callable[[], datetime] | None = None,
        uuid_factory: Callable[[], UUID] = uuid4,
    ) -> None:
        self._products = products
        self._clock = clock or (lambda: datetime.now(UTC))
        self._uuid_factory = uuid_factory
        self._reconciliation = StockReconciliationService(products, movements)

    def create(
        self,
        name: str,
        description: str | None = None,
        category: str | None = None,
        cost_price: Decimal | None = None,
        sale_price: Decimal | None = None,
    ) -> Product:
        resolved_sku = self._generate_sku()
        if self._products.get_by_sku(resolved_sku) is not None:
            raise DuplicateSkuError(f"SKU já cadastrado: {resolved_sku}")
        now = self._clock()
        product = Product(
            resolved_sku, name, description, category, cost_price, sale_price, 0, now, now
        )
        self._products.save(product)
        return product

    def update(
        self,
        sku: str,
        name: str,
        description: str | None,
        category: str | None,
        cost_price: Decimal | None,
        sale_price: Decimal | None,
    ) -> Product:
        product = self._get_required(sku)
        updated = replace(
            product,
            name=name,
            description=description,
            category=category,
            cost_price=cost_price,
            sale_price=sale_price,
            updated_at=self._clock(),
        )
        self._products.save(updated)
        return updated

    def delete(self, sku: str) -> Product:
        product = self._reconciliation.reconcile_product(sku)
        if product.current_stock != 0:
            raise InsufficientStockError("Não é possível excluir produto com saldo diferente de zero.")
        deleted = replace(product, is_deleted=True, deleted_at=self._clock(), updated_at=self._clock())
        self._products.save(deleted)
        return deleted

    def list_products(
        self,
        sku: str = "",
        name: str = "",
        category: str = "",
        stock_status: str = "all",
        include_deleted: bool = False,
    ) -> list[Product]:
        sku, name, category = sku.strip().upper(), name.strip().casefold(), category.strip().casefold()
        products = [
            product
            for product in self._products.list_all()
            if (include_deleted or not product.is_deleted)
            and (not sku or sku in product.sku)
            and (not name or name in product.name.casefold())
            and (not category or category in (product.category or "").casefold())
            and (stock_status == "all" or (stock_status == "zero" and product.current_stock == 0)
            or stock_status == "positive" and product.current_stock > 0)
        ]
        return sorted(products, key=lambda product: product.sku)

    def _get_required(self, sku: str) -> Product:
        normalized_sku = normalize_sku(sku)
        product = self._products.get_by_sku(normalized_sku)
        if product is None:
            raise ProductNotFoundError(f"Produto não encontrado: {normalized_sku}")
        return product

    def _generate_sku(self) -> str:
        while True:
            sku = f"PRD-{self._uuid_factory().hex[:8].upper()}"
            if self._products.get_by_sku(sku) is None:
                return sku


class MovementService:
    """Casos de uso que preservam a integridade do saldo do estoque."""

    def __init__(
        self,
        products: ProductRepository,
        movements: MovementRepository,
        clock: Callable[[], datetime] | None = None,
        uuid_factory: Callable[[], UUID] = uuid4,
    ) -> None:
        self._products = products
        self._movements = movements
        self._clock = clock or (lambda: datetime.now(UTC))
        self._uuid_factory = uuid_factory

    def create(self, sku: str, movement_type: MovementType, quantity: int, note: str | None = None) -> Movement:
        product = self._get_product_for_new_movement(sku)
        now = self._clock()
        movement = Movement(
            f"MOV-{self._uuid_factory()}", product.sku, movement_type, quantity, note, now, now
        )
        resulting_stock = self._resulting_stock(product.sku, new_effect=self._effect(movement))
        self._assert_non_negative(resulting_stock)
        self._movements.save(movement)
        self._save_stock(product, resulting_stock)
        return movement

    def update(
        self, movement_id: str, movement_type: MovementType, quantity: int, note: str | None = None
    ) -> Movement:
        existing = self._get_active_movement(movement_id)
        updated = replace(existing, type=movement_type, quantity=quantity, note=note, updated_at=self._clock())
        resulting_stock = self._resulting_stock(
            existing.sku, old_effect=self._effect(existing), new_effect=self._effect(updated)
        )
        self._assert_non_negative(resulting_stock)
        self._movements.save(updated)
        self._save_stock(self._get_product(existing.sku), resulting_stock)
        return updated

    def cancel(self, movement_id: str) -> Movement:
        existing = self._get_active_movement(movement_id)
        resulting_stock = self._resulting_stock(existing.sku, old_effect=self._effect(existing))
        self._assert_non_negative(resulting_stock)
        cancelled = replace(existing, is_deleted=True, deleted_at=self._clock(), updated_at=self._clock())
        self._movements.save(cancelled)
        self._save_stock(self._get_product(existing.sku), resulting_stock)
        return cancelled

    def list_movements(
        self,
        sku: str = "",
        movement_type: MovementType | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        include_cancelled: bool = False,
    ) -> list[Movement]:
        normalized_sku = sku.strip().upper()
        movements = [
            movement
            for movement in self._movements.list_all()
            if (include_cancelled or not movement.is_deleted)
            and (not normalized_sku or normalized_sku in movement.sku)
            and (movement_type is None or movement.type is movement_type)
            and (start_date is None or movement.created_at.date() >= start_date)
            and (end_date is None or movement.created_at.date() <= end_date)
        ]
        return sorted(movements, key=lambda movement: movement.created_at, reverse=True)

    def _get_product_for_new_movement(self, sku: str) -> Product:
        product = self._get_product(sku)
        if product.is_deleted:
            raise ValidationError("Produto excluído não aceita novas movimentações.")
        return product

    def _get_product(self, sku: str) -> Product:
        normalized_sku = normalize_sku(sku)
        product = self._products.get_by_sku(normalized_sku)
        if product is None:
            raise ProductNotFoundError(f"Produto não encontrado: {normalized_sku}")
        return product

    def _get_active_movement(self, movement_id: str) -> Movement:
        movement = self._movements.get_by_id(movement_id)
        if movement is None:
            raise MovementNotFoundError(f"Movimentação não encontrada: {movement_id}")
        if movement.is_deleted:
            raise ValidationError("Movimentação cancelada não pode ser alterada novamente.")
        return movement

    def _resulting_stock(self, sku: str, old_effect: int = 0, new_effect: int = 0) -> int:
        current_stock = sum(
            self._effect(movement) for movement in self._movements.list_by_sku(sku) if not movement.is_deleted
        )
        return current_stock - old_effect + new_effect

    @staticmethod
    def _effect(movement: Movement) -> int:
        return movement.quantity if movement.type is MovementType.ENTRY else -movement.quantity

    @staticmethod
    def _assert_non_negative(stock: int) -> None:
        if stock < 0:
            raise InsufficientStockError("A operação deixaria o estoque negativo.")

    def _save_stock(self, product: Product, stock: int) -> None:
        self._products.save(replace(product, current_stock=stock, updated_at=self._clock()))
