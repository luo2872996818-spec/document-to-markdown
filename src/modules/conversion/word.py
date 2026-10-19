# 实现 Word DOCX 文档到 Markdown 的转换
from pathlib import Path

from src.modules.conversion.result import ConversionError, ConversionResult
from src.utils.document import convertWithMarkItDown
from src.utils.markdown import normalizeMarkdownText


def convertWord(filePath: str | Path) -> ConversionResult:
    """把 DOCX 文档转换为 Markdown。"""
    sourcePath = Path(filePath)
    if not sourcePath.is_file():
        raise ConversionError(f"文件不存在：{sourcePath}")

    try:
        extractedText = convertWithMarkItDown(sourcePath)
    except Exception as error:
        raise ConversionError(
            f"无法读取 Word 文件 {sourcePath.name}：{error}"
        ) from error

    if not extractedText:
        raise ConversionError(f"Word 文件中没有可转换内容：{sourcePath.name}")

    documentMarkdown = f"# {sourcePath.stem}\n\n{extractedText}"
    return ConversionResult(
        sourcePath=sourcePath,
        markdownText=normalizeMarkdownText(documentMarkdown),
        converterName="word",
        metadata={"characterCount": len(extractedText)},
    )