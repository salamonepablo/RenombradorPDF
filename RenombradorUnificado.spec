# RenombradorUnificado.spec (Añadiendo fitz)
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['menu_principal.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('renombrador_alistamientos.py', '.'),
        ('renombrador_preparatorias.py', '.')
    ],
    hiddenimports=[
        'renombrador_alistamientos',
        'renombrador_preparatorias',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'fitz'  # <-- AÑADIDO PARA LA LIBRERÍA DE PDF (PyMuPDF)
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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