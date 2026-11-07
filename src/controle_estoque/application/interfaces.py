from typing import Protocol

from controle_estoque.domain.models import Movement, Product


class ProductRepository(Protocol):
    def get_by_sku(self, sku: str) -> Product | None: ...

    def save(self, product: Product) -> None: ...


class MovementRepository(Protocol):
    def get_by_id(self, movement_id: str) -> Movement | None: ...

    def save(self, movement: Movement) -> None: ...
