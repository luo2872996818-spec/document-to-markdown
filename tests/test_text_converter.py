# 测试 CSV 和 TSV 转换器
from pathlib import Path

from src.modules.conversion.text import convertText

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_convertCsv() -> None:
    """验证 UTF-8 CSV 可以转换为 Markdown 表格。"""
    filePath = FIXTURE_DIR / "sample.csv"

    result = convertText(filePath)

    assert result.converterName == "text"
    assert "| 姓名 | 说明 |" in result.markdownText
    assert "包含\\|竖线" in result.markdownText
    assert result.metadata["encoding"].lower().replace("_", "-") in {
        "utf-8",
        "utf-8-sig",
        "ascii",
    }


def test_convertTsv() -> None:
    """验证 TSV 可以使用制表符作为表格分隔符。"""
    filePath = FIXTURE_DIR / "sample.tsv"

    result = convertText(filePath)

    assert "| 产品 | 数量 |" in result.markdownText
    assert "| 钢笔 | 3 |" in result.markdownText

def test_convertUtf8BomCsv(tmp_path) -> None:
    """验证 UTF-8 BOM 不会残留在第一个表头中。"""
    filePath = tmp_path / "bom.csv"
    filePath.write_bytes("姓名,学院\n小红,经贸学院\n".encode("utf-8-sig"))

    result = convertText(filePath)

    assert "| 姓名 | 学院 |" in result.markdownText
    assert "\ufeff姓名" not in result.markdownText