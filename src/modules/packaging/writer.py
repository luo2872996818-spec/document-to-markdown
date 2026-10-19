# 负责把转换结果写入 Markdown 文件
from pathlib import Path

from src.modules.conversion.result import ConversionResult
from src.utils.markdown import normalizeMarkdownText


def writeMarkdown(
    result: ConversionResult,
    outputPath: str | Path,
) -> Path:
    """把统一转换结果写入指定的 Markdown 文件。"""
    targetPath = Path(outputPath)
    targetPath.parent.mkdir(parents=True, exist_ok=True)
    targetPath.write_text(
        normalizeMarkdownText(result.markdownText),
        encoding="utf-8",
    )
    return targetPath