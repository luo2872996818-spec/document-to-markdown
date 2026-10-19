# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

from PyInstaller.utils.hooks import collect_all, copy_metadata

projectRoot = Path(SPECPATH).resolve()

datas = [
    (str(projectRoot / "src" / "main" / "app.py"), "app/main"),
    (str(projectRoot / "src"), "src"),
]
binaries = []
hiddenimports = [
    "streamlit.web.cli",
    "streamlit.runtime.scriptrunner.magic_funcs",
]

# 只收集需要额外数据或动态库的包，pandas、numpy、pyarrow 由标准 hooks 处理
packageNames = [
    "streamlit",
    "markitdown",
    "pymupdf4llm",
    "pymupdf",
    "openpyxl",
    "xlrd",
    "charset_normalizer",
    "markdownify",
    "mammoth",
    "pdfminer",
    "pdfplumber",
    "magika",
    "onnxruntime",
]

for packageName in packageNames:
    try:
        packageDatas, packageBinaries, packageHiddenimports = collect_all(packageName)
        datas += packageDatas
        binaries += packageBinaries
        hiddenimports += packageHiddenimports
    except Exception as error:
        print(f"collect_all skipped: {packageName}: {error}")

# 去除测试示例，避免发行包无意义增大
hiddenimports = [
    moduleName
    for moduleName in hiddenimports
    if ".tests" not in moduleName
    and ".test" not in moduleName
    and not moduleName.startswith("streamlit.hello")
]

for metadataName in [
    "streamlit",
    "markitdown",
    "pymupdf4llm",
    "openpyxl",
    "xlrd",
    "charset-normalizer",
]:
    try:
        datas += copy_metadata(metadataName)
    except Exception as error:
        print(f"copy_metadata skipped: {metadataName}: {error}")

analysis = Analysis(
    [str(projectRoot / "src" / "main" / "launcher.py")],
    pathex=[str(projectRoot)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "xlwt", "jupyter", "IPython", "matplotlib"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(analysis.pure)

executable = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="DocumentToMarkdown",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(projectRoot / ".venv" / "Scripts" / "python.exe"),
)

collection = COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="DocumentToMarkdown",
)