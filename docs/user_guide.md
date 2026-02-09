# Guía de Usuario - RenombradorPDF

## Introducción

RenombradorPDF es una aplicación de escritorio diseñada para facilitar el renombrado estandarizado de archivos PDF escaneados. Permite visualizar previsualizaciones de los documentos y aplicar formatos de nombre consistentes según el tipo de documento.

## Inicio Rápido

### Ejecutar la aplicación

1. Abra PowerShell o Terminal
2. Active el entorno virtual:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. Ejecute la aplicación:
   ```powershell
   python src\main.py
   ```

### Seleccionar herramienta

Al iniciar, verá un menú con tres opciones:

1. **Renombrador de ALs / CheckLists LOCs**
2. **Renombrador de PREPARATORIA CCEE**
3. **Renombrador de Viajes LD**

Seleccione la herramienta apropiada según el tipo de documento.

## Renombrador de ALs / CheckLists LOCs

### Uso

1. **Navegue** a la carpeta que contiene los PDFs
2. **Seleccione** un archivo PDF de la lista
3. **Ingrese los datos**:
   - **Fecha**: Ingrese DDMM (ej: 0502). Se formateará automáticamente a DD-MM
   - **N° Locomotora**: Ingrese el número de 2 o 3 dígitos
4. **Seleccione el formato**:
   - **Checklist**: Para documentos de checklist
   - **Alistamientos**: Para documentos de alistamiento
5. Presione **Renombrar** o Enter

### Formatos de salida

- **Checklist**: `05-02 CHECKLIST G-012.pdf`
- **Alistamientos**: `05-02 AL A904.pdf`

### Reglas de formato de locomotoras

- **2 dígitos p/Locs CNR** (ej: 13): Se convierte a `G-0XX` → `G-013`
- **3 dígitos p/Locs GM** (ej: 922): Se convierte a `AXXX` → `A922`
- **Excepciones p/CMN**: 105 y 106 no llevan prefijo → `105`, `106`

## Renombrador de PREPARATORIA CCEE

### Uso

1. **Navegue** a la carpeta del lugar (Ezeiza, Llavallol, etc.)
2. **Seleccione** un archivo PDF
3. **Ingrese los datos**:
   - **N° Formación**: Número de formación (obligatorio)
   - **Día**: Día del mes (opcional, usa hoy si no se especifica)
4. Presione **Renombrar** o Enter

### Formato de salida

`DD-MM PREP LUGAR FXX.pdf`

Ejemplo: `05-02 PREP LLV F123.pdf`

### Códigos de lugares

- Ezeiza → ZZ
- F. Varela - DOA - La Plata → LP
- Glew → GW
- Kilo 5 → K5
- Llavallol → LLV
- P. Constitución → PC
- Temperley → TY

### Detección automática de mes

La aplicación intenta detectar el mes desde el nombre de la carpeta padre con formato `[XX] NombreMes`. Si no lo encuentra, usa el mes actual.

## Renombrador de Viajes LD

### Uso

1. **Navegue** a la carpeta que contiene los PDFs
2. **Seleccione** un archivo PDF
3. **Ingrese los datos**:
   - **Fecha**: Ingrese DDMM (opcional, usa hoy si no se especifica)
   - **Nro. Tren**: Número entre 301 y 310
4. Presione **Renombrar** o Enter

### Formato de salida

`DD-MM MPN TREN.pdf`

Ejemplo: `05-02 MPN 305.pdf`

### Números de tren válidos

Solo se aceptan números de tren del **301 al 310** inclusive.

## Características Comunes

### Vista Previa

- Al seleccionar un PDF, se muestra una previsualización del primer tercio de la primera página
- Facilita identificar el documento correcto antes de renombrar

### Navegación

- **Selector de unidad**: Cambie rápidamente entre unidades de disco
- **Botón Navegar**: Abra un explorador de carpetas para navegar manualmente
- **Árbol de archivos**: 
  - `..` para subir un nivel
  - Carpetas listadas primero
  - Archivos PDF listados después

### Manejo de conflictos

Si ya existe un archivo con el mismo nombre, se agrega un contador:
- `05-02 AL G-022.pdf`
- `05-02 AL G-022_1.pdf`
- `05-02 AL G-022_2.pdf`

### Atajos de teclado

- **Enter** en cualquier campo: Mueve al siguiente campo o ejecuta renombrar
- **Tab**: Navega entre campos
- **Botón Limpiar**: Limpia todos los campos y la vista previa

## Solución de Problemas

### No se muestra vista previa

- Verifique que el archivo sea un PDF válido
- Algunos PDFs protegidos pueden no generar vista previa

### Error al renombrar

- Verifique que tenga permisos de escritura en la carpeta
- Asegúrese de que el archivo no esté abierto en otro programa

### La aplicación se cierra inesperadamente

- Verifique que el entorno virtual esté activado
- Revise que todas las dependencias estén instaladas

## Consejos y Mejores Prácticas

1. **Organización de carpetas**: Mantenga los documentos organizados por fecha/mes
2. **Nombres consistentes**: Use siempre el mismo formato para facilitar búsquedas
3. **Verificar antes de renombrar**: Revise la vista previa para confirmar el documento
4. **Uso del campo fecha**: Si no ingresa fecha, se usa la fecha actual automáticamente
