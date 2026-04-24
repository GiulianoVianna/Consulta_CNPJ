# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/media/giuliano/ADATA HD710 PRO1/Programação/Projetos_python/consulta_cnpj/consulta_cnpj.py'],
    pathex=[],
    binaries=[],
    datas=[('/media/giuliano/ADATA HD710 PRO1/Programação/Projetos_python/consulta_cnpj/consulta_cnpj.ui', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='consulta_cnpj',
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
    name='consulta_cnpj',
)
