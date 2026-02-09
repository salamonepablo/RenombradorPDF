# RenombradorUnificado.spec - v2.0
# Configuración para PyInstaller con la nueva estructura modular
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/main.py'],  # Punto de entrada actualizado a nueva estructura
    pathex=[],
    binaries=[],
    datas=[
        # No es necesario agregar archivos individuales, todo está en src/
    ],
    hiddenimports=[
        'src.ui.menu_principal',
        'src.ui.base_renamer',
        'src.renamers.alistamientos',
        'src.renamers.preparatorias',
        'src.renamers.viajes_ld',
        'src.utils.validators',
        'src.utils.formatters',
        'src.utils.pdf_handler',
        'src.config.settings',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'fitz',  # PyMuPDF para lectura de PDFs
        'tkinter',  # Interfaz gráfica
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RenombradorUnificado',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RenombradorUnificado',
)