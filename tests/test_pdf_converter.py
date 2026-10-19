# 测试电子版 PDF 转换器
import pymupdf
import pytest

from src.modules.conversion.pdf import convertPdf
from src.modules.conversion.result import ConversionError


def test_convertDigitalPdf(tmp_path) -> None:
    """验证多页电子版 PDF 可以完整转换为 Markdown。"""
    filePath = tmp_path / "sample.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Phase one PDF test", fontsize=12)
    secondPage = document.new_page()
    secondPage.insert_text((72, 72), "Second page content", fontsize=12)
    document.save(filePath)
    document.close()

    result = convertPdf(filePath)

    assert result.converterName == "pdf"
    assert "Phase one PDF test" in result.markdownText
    assert "Second page content" in result.markdownText
    assert result.metadata["characterCount"] > 0


def test_rejectEmptyPdf(tmp_path) -> None:
    """验证没有文字层的 PDF 会返回扫描版提示。"""
    filePath = tmp_path / "empty.pdf"
    document = pymupdf.open()
    document.new_page()
    document.save(filePath)
    document.close()

    with pytest.raises(ConversionError, match="扫描版"):
        convertPdf(filePath)


def test_rejectCorruptPdf(tmp_path) -> None:
    """验证损坏的 PDF 会返回明确错误。"""
    filePath = tmp_path / "corrupt.pdf"
    filePath.write_bytes(b"not a real pdf")

    with pytest.raises(ConversionError, match="无法读取 PDF"):
        convertPdf(filePath)