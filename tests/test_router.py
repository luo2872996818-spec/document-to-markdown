# 测试文件分类、转换路由和 Markdown 写出
import pytest

from src.modules.conversion.result import ConversionError
from src.modules.packaging.writer import writeMarkdown
from src.modules.conversion.router import convertDocument
from src.utils.filetypes import getFileCategory, isSupportedFile


def test_fileTypeDetection(tmp_path) -> None:
    """验证常见扩展名能够被正确分类。"""
    assert getFileCategory(tmp_path / "sample.xlsx") == "excel"
    assert getFileCategory(tmp_path / "sample.pdf") == "pdf"
    assert isSupportedFile(tmp_path / "sample.docx")
    assert not isSupportedFile(tmp_path / "sample.txt")


def test_convertDocumentAndWrite(tmp_path) -> None:
    """验证路由入口能够转换 CSV 并写出 Markdown 文件。"""
    sourcePath = tmp_path / "数据.csv"
    sourcePath.write_text("名称,数量\n铅笔,5\n", encoding="utf-8")
    outputPath = tmp_path / "output" / "数据.md"

    result = convertDocument(sourcePath)
    writtenPath = writeMarkdown(result, outputPath)

    assert writtenPath == outputPath
    assert outputPath.read_text(encoding="utf-8").endswith("\n")
    assert "| 名称 | 数量 |" in outputPath.read_text(encoding="utf-8")


def test_rejectUnsupportedFile(tmp_path) -> None:
    """验证不支持的文件类型会返回明确错误。"""
    sourcePath = tmp_path / "说明.txt"
    sourcePath.write_text("测试", encoding="utf-8")

    with pytest.raises(ConversionError, match="暂不支持"):
        convertDocument(sourcePath)