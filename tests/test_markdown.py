# 测试 Markdown 表格的转义和生成
from datetime import datetime

from src.utils.markdown import escapeMarkdownCell, formatCellValue, rowsToMarkdown


def test_escapeMarkdownCell() -> None:
    """验证竖线、换行和普通文本能够正确转换。"""
    result = escapeMarkdownCell("A|B\nC")
    assert result == "A\\|B<br>C"


def test_rowsToMarkdown() -> None:
    """验证二维数据能够生成标准 Markdown 表格。"""
    result = rowsToMarkdown([
        ["姓名", "分数"],
        ["小明", 95],
    ])
    expected = "\n".join([
        "| 姓名 | 分数 |",
        "| --- | --- |",
        "| 小明 | 95 |",
    ])
    assert result == expected

def test_formatCellValue() -> None:
    """验证整数和日期会转换成易读文本。"""
    assert formatCellValue(12.0) == "12"
    assert formatCellValue(12.5) == "12.5"
    assert (
        formatCellValue(datetime(2026, 9, 14, 11, 14, 57))
        == "2026-09-14 11:14:57"
    )