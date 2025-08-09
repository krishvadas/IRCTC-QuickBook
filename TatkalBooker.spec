# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

cython_utilities = collect_data_files("Cython", include_py_files=False)
paddleocr_utilities = collect_data_files("paddleocr", include_py_files=False)
paddle_utilities = collect_data_files("paddle", include_py_files=False)
utils_data = collect_data_files("utils", includes=["config.template.json", "cleaned_station_codes.json"])


datas = [
    *utils_data,
    *cython_utilities,
    *paddleocr_utilities,
    *paddle_utilities,
    ("icon.ico", "."),
    ("upx/upx.exe", "./upx"),
    ("utils/paddleocr_models", "./utils/paddleocr_models"),
    (".venv/lib/site-packages/paddleocr/ppocr", "ppocr"),
    (".venv/lib/site-packages/paddleocr/ppstructure", "ppstructure"),
    (".venv/lib/site-packages/paddleocr/tools", "tools"),
    (".venv/Lib/site-packages/paddle/libs/mklml.dll", "."),
    (r".venv\Lib\site-packages\paddleocr\ppocr\utils\en_dict.txt", "paddleocr/ppocr/utils"),
]

hiddenimports = [
    "paddleocr", "customtkinter", "playwright.sync_api",
    "cv2", "numpy", "yaml", "tkinter", "tkinter.ttk", "tkinter.messagebox",
    "ppocr",
    "ppocr.utils.logging",
    "ppocr.postprocess",
    "ppocr.data",
    "ppocr.modeling",
    "ppocr.metrics",
    "ppocr.arch",
    "ppocr.data.simple_dataset",
    "ppocr.postprocess.rec_postprocess",
    "ppocr.postprocess.cls_postprocess",
    "ppocr.postprocess.det_postprocess",
    "ppocr.modeling.architectures",
    "ppocr.modeling.backbones",
    "ppocr.modeling.necks",
    "ppocr.modeling.heads",
    "ppocr.modeling.losses",
    "ppocr.modeling.transforms",
    "tools",
    "tools.infer.predict_system",
    "tools.infer.predict_rec",
    "tools.infer.utility",
    "PIL.Image",
    "PIL.ImageDraw",
    "PIL.ImageFont",
    "PIL.ImageOps",
    "PIL.ImageFilter",
    "PIL.ImageEnhance",
    "PIL.ImageStat",
    "PIL.ImageChops",
    "shapely.geometry",
    "pyclipper",
    "imghdr",
    "skimage",
    "skimage.morphology",
    "imgaug",
    "scipy.io",
    "lmdb",
    "requests",
]

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
    name='IRCTC QuickBook',
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
    icon=['D:\\Projects\\VSCodeProjects\\TatkalBooking\\icon.ico'],
)

