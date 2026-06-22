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
    hooksconfig={'setuptools': {'vendor': False}},
    # <-- 2. Esclude moduli pesanti/test per evitare il blocco nella ricerca delle DLL
    #     setuptools NON in excludes: al suo posto usiamo hooksconfig per gestire i vendor
    # NOTA: distutils e pkg_resources NON in excludes: gli hook PyInstaller (hook-distutils, hook-setuptools)
    #       creano alias per questi moduli; escluderli causa ValueError: "already imported as ExcludedModule"
    excludes=['pip', 'pytest', 'test', 'unittest', 'tkinter.test', 'pygments', 'matplotlib', 'scipy', 'cv2'],
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