# 封装 MarkItDown，供多种文档格式复用
from pathlib import Path

from markitdown import MarkItDown


def convertWithMarkItDown(filePath: Path) -> str:
    """使用 MarkItDown 把支持的文件转换为 Markdown 文本。"""
    converter = MarkItDown(enable_plugins=False)
    result = converter.convert(str(filePath))
    return result.text_content.strip()