# Guía de Migración - v1.0 a v2.0

## Cambios Principales

### Estructura de Carpetas

**Antes (v1.0):**
```
RenombradorPDF/
├── menu_principal.py
├── renombrador_alistamientos.py
├── renombrador_preparatorias.py
└── renombrador_viajes_ld.py
```

**Después (v2.0):**
```
RenombradorPDF/
├── src/
│   ├── main.py
│   ├── ui/
│   ├── renamers/
│   ├── utils/
│   └── config/
└── tests/
```

### Cómo Ejecutar

**Antes:**
```powershell
python menu_principal.py
```

**Ahora:**
```powershell
python -m src.main
# o
python src/main.py
```

### Imports

**Antes:**
```python
import renombrador_alistamientos
```

**Ahora:**
```python
from src.renamers import AlistamientosRenamerApp
```

### Clases Renombradas

| Antes | Ahora |
|-------|-------|
| `PDFRenamerApp` | `AlistamientosRenamerApp` |
| `PreparatoriaRenamerApp` | `PreparatoriaRenamerApp` (sin cambios) |
| `PDFRenamerApp` (viajes) | `ViajeLDRenamerApp` |

## Compatibilidad hacia Atrás

Los archivos antiguos se mantienen temporalmente para compatibilidad, pero es recomendable migrar a la nueva estructura.

### Ejecutar Archivos Legacy

```powershell
# Aún funciona (con advertencia)
python menu_principal.py

# Redirige automáticamente a la nueva estructura
python menu_principal_legacy.py
```

## Nuevas Funcionalidades en v2.0

### 1. Validadores Reutilizables

```python
from src.utils.validators import DateValidator, LocomotiveValidator

# Validar fecha
if DateValidator.validate_date("05-02"):
    print("Fecha válida")

# Validar locomotora
if LocomotiveValidator.validate_locomotive_number("107"):
    print("Locomotora válida")
```

### 2. Formateadores

```python
from src.utils.formatters import LocomotiveFormatter, FilenameFormatter

# Formatear locomotora
locomotive = LocomotiveFormatter.format_locomotive_number("22")
# Resultado: "G-022"

# Generar nombre de archivo
filename = FilenameFormatter.format_checklist("05-02", "G-022")
# Resultado: "05-02 CHECKLIST G-022.pdf"
```

### 3. Configuración Centralizada

```python
from src.config import Settings

# Acceder a configuraciones
path = Settings.DEFAULT_PATH
width = Settings.WINDOW_WIDTH
```

### 4. Tests

```powershell
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src
```

## Extender la Aplicación

### Crear un Nuevo Renombrador

1. Crear archivo en `src/renamers/mi_renombrador.py`:

```python
from ..ui.base_renamer import BaseRenamerUI
from ..utils.validators import DateValidator
from ..utils.formatters import FilenameFormatter

class MiRenamerApp(BaseRenamerUI):
    def __init__(self, root):
        super().__init__(root, "Mi Renombrador")
    
    def setup_control_frame(self, control_frame):
        # Tu UI personalizada aquí
        pass
    
    def rename_file(self):
        # Tu lógica de renombrado aquí
        pass
```

2. Agregar a `src/renamers/__init__.py`:

```python
from .mi_renombrador import MiRenamerApp

__all__ = ['AlistamientosRenamerApp', 'PreparatoriaRenamerApp', 
           'ViajeLDRenamerApp', 'MiRenamerApp']
```

3. Agregar al menú en `src/ui/menu_principal.py`:

```python
from ..renamers import MiRenamerApp

buttons = [
    # ... botones existentes ...
    ("Mi Nuevo Renombrador", MiRenamerApp),
]
```

## Cronograma de Deprecación

- **v2.0 - v2.5**: Archivos legacy disponibles con advertencias
- **v3.0**: Se eliminarán archivos legacy
- **Migración recomendada**: Antes de v3.0

## Soporte

Para problemas durante la migración:
1. Revisa esta guía
2. Consulta el README.md actualizado
3. Ejecuta los tests: `pytest`
4. Verifica que todas las dependencias estén instaladas
