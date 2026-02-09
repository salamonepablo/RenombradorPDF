"""
Punto de entrada principal de la aplicación RenombradorPDF.
"""
from src.ui.menu_principal import MenuPrincipal


def main():
    """Función principal que inicia la aplicación."""
    app = MenuPrincipal()
    app.run()


if __name__ == "__main__":
    main()
