from controle_estoque.app.paths import ensure_data_dir
from controle_estoque.application.services import MovementService, ProductService
from controle_estoque.infrastructure.persistence.repositories import JsonMovementRepository, JsonProductRepository
from controle_estoque.presentation.main_window import MainWindow


def main() -> None:
    data_dir = ensure_data_dir()
    products, movements = JsonProductRepository(data_dir), JsonMovementRepository(data_dir)
    window = MainWindow(ProductService(products, movements), MovementService(products, movements))
    window.mainloop()


if __name__ == "__main__":
    main()
