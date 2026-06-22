# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main_ui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config.json', '.')  # <-- 1. Include config.json nella cartella radice dell'EXE
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={'setuptools': {'vendor': False}'setuptools': {'vendor': False}},
    # <-- 2. Esclude moduli pesanti/test per evitare il blocco nella ricerca delle DLL
    #     Aggiunti setuptools, pip, pkg_resources (causano hang in "Looking for dynamic libraries")
    excludes=['setuptools', 'pip', 'distutils', 'pkg_resources', 'pytest', 'test', 'unittest', 'tkinter.test', 'pygments', 'matplotlib', 'scipy', 'cv2', 'setuptools', 'pip', 'distutils', 'pkg_resources'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Eidolon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # <-- CAMBIATO DA TRUE A FALSE
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)