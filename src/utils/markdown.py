# 提供创建 Markdown 表格和整理文本的基础函数
from datetime import date, datetime, time
from typing import Any, Sequence


def isBlankValue(value: Any) -> bool:
    """判断单元格是否没有实际内容。"""
    if value is None:
        return True
    return str(value).strip() == ""


def formatCellValue(value: Any) -> str:
    """把任意单元格值转换成适合 Markdown 显示的文本。"""
    if value is None:
        return ""
    if isinstance(value, datetime):
        if value.time() == time(0, 0, 0):
            return value.strftime("%Y-%m-%d")
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def escapeMarkdownCell(value: Any) -> str:
    """转义可能破坏 Markdown 表格的单元格内容。"""
    text = formatCellValue(value)

    # 先转义反斜杠，再转义竖线，避免产生不完整的转义结果
    text = text.replace("\\", "\\\\")
    text = text.replace("|", "\\|")

    # Markdown 表格单元格不能跨行，因此把换行转换为 HTML 换行标签
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.replace("\n", "<br>")


def trimEmptyRows(rows: Sequence[Sequence[Any]]) -> list[list[Any]]:
    """删除末尾空行，并裁掉所有行末尾的空列。"""
    cleanedRows = [list(row) for row in rows]

    # 从最后一行开始删除完全空白的行
    while cleanedRows and all(isBlankValue(cell) for cell in cleanedRows[-1]):
        cleanedRows.pop()

    if not cleanedRows:
        return []

    # 找到最后一个存在非空值的列
    columnCount = 0
    for row in cleanedRows:
        for index, cell in enumerate(row):
            if not isBlankValue(cell):
                columnCount = max(columnCount, index + 1)

    return [row[:columnCount] for row in cleanedRows]


def rowsToMarkdown(rows: Sequence[Sequence[Any]]) -> str:
    """把二维数据转换为 GitHub 风格 Markdown 表格。"""
    cleanedRows = trimEmptyRows(rows)
    if not cleanedRows:
        return ""

    columnCount = max(len(row) for row in cleanedRows)
    if columnCount == 0:
        return ""

    normalizedRows = [
        list(row) + [""] * (columnCount - len(row))
        for row in cleanedRows
    ]

    header = [escapeMarkdownCell(cell) for cell in normalizedRows[0]]
    separator = ["---"] * columnCount
    body = [
        [escapeMarkdownCell(cell) for cell in row]
        for row in normalizedRows[1:]
    ]

    markdownLines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    markdownLines.extend(
        "| " + " | ".join(row) + " |"
        for row in body
    )
    return "\n".join(markdownLines)


def normalizeMarkdownText(text: str) -> str:
    """统一换行符，并保证文件以一个换行符结束。"""
    normalizedText = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalizedText.strip() + "\n"