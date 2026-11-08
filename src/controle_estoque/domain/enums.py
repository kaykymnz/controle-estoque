from enum import StrEnum


class MovementType(StrEnum):
    """Tipos de movimentação que afetam o estoque."""

    ENTRY = "ENTRY"
    EXIT = "EXIT"
