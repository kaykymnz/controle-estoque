class InventoryError(Exception):
    """Erro base da aplicação de estoque."""


class ValidationError(InventoryError):
    """Dados informados não atendem às regras de domínio."""


class DuplicateSkuError(InventoryError):
    """O SKU já está reservado por um produto."""


class ProductNotFoundError(InventoryError):
    """O produto solicitado não foi encontrado."""


class MovementNotFoundError(InventoryError):
    """A movimentação solicitada não foi encontrada."""


class InsufficientStockError(InventoryError):
    """A operação deixaria o saldo do produto negativo."""


class InvalidDataFileError(InventoryError):
    """Um arquivo JSON de dados está inválido ou não pôde ser lido."""

    def __init__(self, path: str, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Não foi possível ler o arquivo de dados '{path}': {reason}")
