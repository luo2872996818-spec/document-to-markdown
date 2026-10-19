# 根据文件扩展名把转换任务分派给对应模块
from collections.abc import Callable
from pathlib import Path

from src.modules.conversion.excel import convertExcel
from src.modules.conversion.pdf import convertPdf
from src.modules.conversion.result import ConversionError, ConversionResult
from src.modules.conversion.text import convertText
from src.modules.conversion.word import convertWord

ConverterFunction = Callable[[Path], ConversionResult]

CONVERTERS: dict[str, ConverterFunction] = {
    ".pdf": convertPdf,
    ".docx": convertWord,
    ".xlsx": convertExcel,
    ".xlsm": convertExcel,
    ".xls": convertExcel,
    ".csv": convertText,
    ".tsv": convertText,
}


def getConverter(filePath: str | Path) -> ConverterFunction:
    """返回扩展名对应的转换函数，不支持时抛出异常。"""
    suffix = Path(filePath).suffix.lower()
    converter = CONVERTERS.get(suffix)
    if converter is None:
        raise ConversionError(f"暂不支持该文件类型：{suffix or '无扩展名'}")
    return converter


def convertDocument(filePath: str | Path) -> ConversionResult:
    """把单个文档转换为 Markdown。"""
    sourcePath = Path(filePath)
    if not sourcePath.exists():
        raise ConversionError(f"文件不存在：{sourcePath}")
    if not sourcePath.is_file():
        raise ConversionError(f"路径不是文件：{sourcePath}")

    return getConverter(sourcePath)(sourcePath)