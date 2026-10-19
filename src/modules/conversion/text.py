# 实现 CSV 和 TSV 文件的 Markdown 转换
import csv
from pathlib import Path

from charset_normalizer import from_path

from src.modules.conversion.result import ConversionError, ConversionResult
from src.utils.markdown import normalizeMarkdownText, rowsToMarkdown


def hasUtf8Bom(filePath: Path) -> bool:
    """判断文件是否以 UTF-8 BOM 开头。"""
    with filePath.open("rb") as file:
        return file.read(3) == b"\xef\xbb\xbf"


def detectEncoding(filePath: Path) -> str:
    """检测文本文件编码，检测失败时回退到 UTF-8。"""
    # BOM 必须优先识别，否则 BOM 会残留在第一个表头单元格中
    if hasUtf8Bom(filePath):
        return "utf-8-sig"

    matches = from_path(filePath)
    bestMatch = matches.best()
    if bestMatch and bestMatch.encoding:
        return bestMatch.encoding
    return "utf-8"


def detectDelimiter(sample: str, suffix: str) -> str:
    """根据文件扩展名和内容判断 CSV 或 TSV 分隔符。"""
    defaultDelimiter = "\t" if suffix.lower() == ".tsv" else ","

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        return dialect.delimiter
    except csv.Error:
        # 内容太短或格式特殊时，使用扩展名对应的默认分隔符
        return defaultDelimiter


def readTableRows(filePath: Path) -> tuple[list[list[str]], str, str]:
    """读取表格文件，返回数据行、编码和分隔符。"""
    encoding = detectEncoding(filePath)

    with filePath.open("r", encoding=encoding, newline="", errors="replace") as file:
        sample = file.read(4096)
        file.seek(0)
        delimiter = detectDelimiter(sample, filePath.suffix)
        rows = list(csv.reader(file, delimiter=delimiter))

    return rows, encoding, delimiter


def convertText(filePath: str | Path) -> ConversionResult:
    """把 CSV 或 TSV 文件转换为 Markdown。"""
    sourcePath = Path(filePath)
    if not sourcePath.is_file():
        raise ConversionError(f"文件不存在：{sourcePath}")

    rows, encoding, delimiter = readTableRows(sourcePath)
    tableMarkdown = rowsToMarkdown(rows)
    if not tableMarkdown:
        raise ConversionError(f"表格中没有可转换的内容：{sourcePath.name}")

    # 使用文件名作为一级标题，确保文档具有明确主题
    documentMarkdown = f"# {sourcePath.stem}\n\n{tableMarkdown}"
    return ConversionResult(
        sourcePath=sourcePath,
        markdownText=normalizeMarkdownText(documentMarkdown),
        converterName="text",
        metadata={
            "encoding": encoding,
            "delimiter": delimiter,
            "rowCount": len(rows),
        },
    )