"""
Script de compatibilidad para mantener funcionalidad con archivos legacy.
Permite ejecutar menu_principal.py redirigiendo a la nueva estructura.
"""
import sys
from pathlib import Path

# Agregar src al path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Importar y ejecutar el nuevo main
from main import main

if __name__ == "__main__":
    print("⚠️  Usando archivo legacy menu_principal.py")
    print("💡 Se recomienda usar: python -m src.main")
    print("🚀 Iniciando aplicación...\n")
    main()
