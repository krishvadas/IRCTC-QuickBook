import sysconfig
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

site_packages = sysconfig.get_paths()["purelib"]

ppocr_path = os.path.join(site_packages, "paddleocr", "ppocr")
tools_path = os.path.join(site_packages, "paddleocr", "tools")

hiddenimports = (
    collect_submodules("paddleocr")
    + collect_submodules("paddleocr.ppocr")
    + collect_submodules("paddleocr.tools")
    + ["Cython", "Cython.Compiler"]
)

datas = (
    collect_data_files("Cython")
    + collect_data_files("paddleocr.ppocr")
    + collect_data_files("paddleocr.tools")
    + [(ppocr_path, "paddleocr/ppocr"), (tools_path, "paddleocr/tools")]
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='IRCTC.Quickbook',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
