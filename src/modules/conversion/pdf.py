# 实现电子版 PDF 到 Markdown 的转换
from pathlib import Path

import pymupdf4llm

from src.modules.conversion.result import ConversionError, ConversionResult
from src.utils.document import convertWithMarkItDown
from src.utils.markdown import normalizeMarkdownText


def extractPdfText(filePath: Path) -> str:
    """使用 PyMuPDF4LLM 提取 PDF 文字，并关闭 OCR。"""
    return pymupdf4llm.to_markdown(
        str(filePath),
        use_ocr=False,
        force_ocr=False,
    ).strip()


def convertPdf(filePath: str | Path) -> ConversionResult:
    """把电子版 PDF 转换为 Markdown。"""
    sourcePath = Path(filePath)
    if not sourcePath.is_file():
        raise ConversionError(f"文件不存在：{sourcePath}")

    try:
        extractedText = extractPdfText(sourcePath)
    except Exception as error:
        raise ConversionError(
            f"无法读取 PDF 文件 {sourcePath.name}：{error}"
        ) from error

    # PyMuPDF4LLM 无法提取文字时，尝试 MarkItDown 作为备用解析器
    if not extractedText:
        try:
            extractedText = convertWithMarkItDown(sourcePath)
        except Exception:
            extractedText = ""

    if not extractedText:
        raise ConversionError(
            f"PDF 中没有可提取文字，可能是扫描版文件：{sourcePath.name}"
        )

    documentMarkdown = f"# {sourcePath.stem}\n\n{extractedText}"
    return ConversionResult(
        sourcePath=sourcePath,
        markdownText=normalizeMarkdownText(documentMarkdown),
        converterName="pdf",
        metadata={"characterCount": len(extractedText)},
    )