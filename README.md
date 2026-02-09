# RenombradorPDF v2.0

Programa profesional para renombrar archivos PDF escaneados de forma estandarizada en carpetas compartidas.

Permite visualizar secciones específicas del documento y aplicar formatos de nombre consistentes con mínima entrada de datos, facilitando la localización y organización de archivos.

## ✨ Características

- 🔄 Renombrado automático con múltiples formatos predefinidos
- 👁️ Vista previa inteligente de documentos PDF
- 📋 Estandarización automática de nombres
- 🎨 Interfaz gráfica intuitiva con menú de selección
- 🧪 Suite completa de tests unitarios
- 📦 Arquitectura modular y mantenible
- 🏗️ Tres renombradores especializados:
  - **ALs / CheckLists LOCs**: Para alistamientos y checklists de locomotoras
  - **PREPARATORIA CCEE**: Para documentos de preparatoria
  - **Viajes LD**: Para documentos de viajes de larga distancia

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Windows Terminal o PowerShell 7+ (recomendado)

## 🚀 Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone https://github.com/salamonepablo/RenombradorPDF.git
cd RenombradorPDF
```

### 2. Crear un entorno virtual (recomendado)
```powershell
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias
```powershell
# Dependencias de producción
pip install -r requirements.txt

# Dependencias de desarrollo (opcional, para tests)
pip install -r requirements-dev.txt
```

Las dependencias incluyen:
- *💻 Uso de la Aplicación

### Ejecutar en modo desarrollo
```powershell
# Asegúrate de que el venv esté activado
.\.venv\Scripts\Activate.ps1

# Ejecutar la aplicación desde la nueva estructura
python -m src.main

# O alternativa con el archivo directo
python src/main.py
```

La interfaz principal te permitirá acceder a los diferentes tipos de renombradores.

Para más detalles, consulta la [Guía de Usuario completa](docs/user_guide.md
pyt🧪 Ejecutar Tests

La aplicación incluye una suite completa de tests unitarios y de integración:

```powershell
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests específicos
pytest tests/test_validators.py
pytest tests/test_formatters.py
```

### Cobertura de tests

Los tests cubren:
- ✅ Validadores de entrada (fechas, locomotoras, trenes)
- ✅ Formateadores de datos
- ✅ Generación de nombres de archivo
- ✅ Flujos completos de renombrado

## 🏗️ hon menu_principal.py
```
📦 Generación del Distribuible

Para crear un ejecutable standalone de la aplicación:

### 1. Instalar PyInstaller
```powershell
pip install pyinstaller
```

### 2. Generar el distribuible
```powershell
# Limpiar compilaciones previas (recomendado)
Remove-Item -Recurse -Force build, dist

# Compilar el ejecutable
pyinstaller RenombradorUnificado.spec
```

### 3. Ubicación del ejecutable
El distribuible se encontrará en:
```
dist/RenombradorUnificado/RenombradorUnificado.exe
```

### 4. Distribuir la aplicación
La carpeta `dist/RenombradorUnificado/` contiene todos los archivos necesarios. Puedes:
- Comprimirla como `.zip` para distribuir
- Crear un instalador con herramientas adicionales
- Compartir la carpeta directamente

**Nota**: El usuario final solo necesita ejecutar el `
# Si aún no está instalado
pip install pyinstaller
```

### 2. Generar el distribuible
```powershell
# Asegúrate de estar en la carpeta del proyecto
cd C:\Users\pablo.salamone\Programmes\RenombradorPDF

# Limpiar compilaciones previas (opcional pero recomendado)
Rem📁 Estructura del Proyecto

```
RenombradorPDF/
├── src/                                # Código fuente principal
│   ├── __init__.py
│   ├── main.py                         # Punto de entrada de la aplicación
│   ├── ui/                             # Módulos de interfaz de usuario
│   │   ├── __init__.py
│   │   ├── base_renamer.py            # Clase base para renombradores
│   │   └── menu_principal.py          # Menú principal
│   ├── renamers/                       # Módulos de renombrado específicos
│   │   ├── __init__.py
│   │   ├── alistamientos.py           # Renombrador de alistamientos
│   │   ├── preparatorias.py           # Renombrador de preparatorias
│  🛠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fitz'"
Asegúrate de instalar las dependencias:
```powershell
pip install PyMuPDF Pillow
```

### Error al ejecutar desde PowerShell
Si tienes problemas de ejecución de scripts, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Los tests no se ejecutan
Verifica que hayas instalado las dependencias de desarrollo:
```powershell
pip install -r requirements-dev.txt
```

### Imports no funcionan al ejecutar tests
Los tests están configurados para agregar `src/` al path automáticamente. Si aún tienes problemas, ejecuta desde la raíz del proyecto:
```powershell
python -m pytest
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Ejecuta los tests (`pytest`)
4. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
5. Push a la rama (`git push origin feature/AmazingFeature`)
6. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 👤 Autor

**Pablo Salamone**

## 🔄 Changelog

### Version 2.0.0 (2026-02-09)
- 🏗️ Arquitectura completamente refactorizada
- 📦 Estructura modular con separación de responsabilidades
- 🧪 Suite completa de tests unitarios
- 📚 Documentación mejorada
- ⚡ Clase base reutilizable para nuevos renombradores
- 🔧 Configuración centralizada
- 🎨 Código más limpio y mantenible

### Version 1.0.0
- ✨ Versión inicial
- 🔄 Tres tipos de renombradores
- 👁️ Vista previa de PDFs
- 🖥️ Interfaz gráfica básica ├── test_formatters.py
│   ├── test_alistamientos.py
│   └── test_viajes_ld.py
├── docs/                               # Documentación
│   └── user_guide.md                  # Guía de usuario
├── .venv/                              # Entorno virtual (no en git)
├── build/                              # Artefactos de compilación (generado)
├── dist/                               # Ejecutables distribuibles (generado)
├── .gitignore                          # Archivos ignorados por git
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias de producción
├── requirements-dev.txt                # Dependencias de desarrollo
├── pyproject.toml                      # Configuración del proyecto
├── setup.py                            # Script de instalación
└── RenombradorUnificado.spec          # Configuración de PyInstaller
```

### Archivos legacy (mantener para compatibilidad)
```
├── menu_principal.py                   # Punto de entrada antiguo
├── renombrador_alistamientos.py        # Versión antigua
├── renombrador_preparatorias.py        # Versión antigua
└── renombrador_viajes_ld.py            # Versión antigua
La carpeta `dist/RenombradorUnificado/` contiene todos los archivos necesarios para ejecutar la aplicación. Puedes:
- Comprimirla como `.zip` para distribuir
- Crear un instalador con herramientas adicionales si es necesario
- Compartir la carpeta directamente

**Nota**: El usuario final solo necesita ejecutar `RenombradorUnificado.exe` sin tener Python instalado.

## Estructura del Proyecto
```
RenombradorPDF/
├── menu_principal.py              # Interfaz principal de la aplicación
├── renombrador_alistamientos.py   # Módulo para renombrado de alistamientos y checklists
├── renombrador_preparatorias.py   # Módulo para renombrado de preparatorias
├── renombrador_viajes_ld.py       # Módulo para renombrado de viajes de larga distancia
├── RenombradorUnificado.spec      # Configuración de PyInstaller
├── requirements.txt               # Dependencias del proyecto
├── README.md                       # Este archivo
├── .venv/                          # Entorno virtual (no incluir en git)
├── build/                          # Artefactos de compilación (generado)
└── dist/                           # Ejecutables distribuibles (generado)
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fitz'"
Asegúrate de instalar las dependencias:
```powershell
pip install PyMuPDF Pillow
```

### Error al ejecutar desde PowerShell
Si tienes problemas de ejecución de scripts, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
