from controle_estoque.app.paths import ensure_data_dir
from controle_estoque.presentation.main_window import MainWindow


def main() -> None:
    ensure_data_dir()
    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    main()
