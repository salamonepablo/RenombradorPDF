# RenombradorPDF

Programa para renombrar archivos escaneados de forma genérica en una carpeta compartida.

Permite ver sectores del documento específicos para poder renombrar los archivos tipeando poca información, estandarizando el nombre de los archivos para su fácil localización.

## Características
- Renombrado automático de PDFs escaneados
- Vista previa de secciones específicas del documento
- Estandarización de nombres de archivo

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Windows Terminal o PowerShell 7+ (recomendado)

## Instalación

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
pip install -r requirements.txt
```

Las dependencias incluyen:
- **Pillow**: Para manipulación de imágenes
- **PyMuPDF (fitz)**: Para lectura y procesamiento de archivos PDF

## Uso de la Aplicación

### Ejecutar en modo desarrollo
```powershell
# Asegúrate de que el venv esté activado
.\.venv\Scripts\Activate.ps1

# Ejecutar la aplicación
python menu_principal.py
```

La interfaz principal te permitirá acceder a los diferentes tipos de renombradores (alistamientos, preparatorias, etc.).

## Generación del Distribuible

Para crear un ejecutable standalone de la aplicación:

### 1. Instalar PyInstaller
```powershell
# Si aún no está instalado
pip install pyinstaller
```

### 2. Generar el distribuible
```powershell
# Asegúrate de estar en la carpeta del proyecto
cd C:\Users\pablo.salamone\Programmes\RenombradorPDF

# Limpiar compilaciones previas (opcional pero recomendado)
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
La carpeta `dist/RenombradorUnificado/` contiene todos los archivos necesarios para ejecutar la aplicación. Puedes:
- Comprimirla como `.zip` para distribuir
- Crear un instalador con herramientas adicionales si es necesario
- Compartir la carpeta directamente

**Nota**: El usuario final solo necesita ejecutar `RenombradorUnificado.exe` sin tener Python instalado.

## Estructura del Proyecto
```
RenombradorPDF/
├── menu_principal.py              # Interfaz principal de la aplicación
├── renombrador_alistamientos.py   # Módulo para renombrado de alistamientos
├── renombrador_preparatorias.py   # Módulo para renombrado de preparatorias
├── RenombradorUnificado.spec      # Configuración de PyInstaller
├── requirements.txt               # Dependencias del proyecto
├── README.md                       # Este archivo
└── build/                          # Artefactos de compilación (generado)
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
