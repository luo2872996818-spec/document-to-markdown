# 定义项目支持的文件类型和分类规则
from pathlib import Path

SUPPORTED_EXTENSIONS = frozenset({
    ".pdf",
    ".docx",
    ".xlsx",
    ".xlsm",
    ".xls",
    ".csv",
    ".tsv",
})

TEXT_EXTENSIONS = frozenset({".csv", ".tsv"})
EXCEL_EXTENSIONS = frozenset({".xlsx", ".xlsm", ".xls"})


def getFileCategory(filePath: str | Path) -> str:
    """根据扩展名返回文件分类，不支持时返回 unsupported。"""
    suffix = Path(filePath).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".docx":
        return "word"
    if suffix in EXCEL_EXTENSIONS:
        return "excel"
    if suffix in TEXT_EXTENSIONS:
        return "text"
    return "unsupported"


def isSupportedFile(filePath: str | Path) -> bool:
    """判断文件扩展名是否在首版支持范围内。"""
    return Path(filePath).suffix.lower() in SUPPORTED_EXTENSIONS