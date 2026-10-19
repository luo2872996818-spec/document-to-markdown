# 生成批量转换报告
import csv
from collections.abc import Sequence
from pathlib import Path

from src.modules.batch import BatchItemResult

STATUS_LABELS = {
    "success": "成功",
    "warning": "成功但有提示",
    "failed": "失败",
}


def buildReportRows(results: Sequence[BatchItemResult]) -> list[dict[str, str]]:
    """把批量结果转换成适合页面和 CSV 使用的行数据。"""
    return [
        {
            "源文件": result.sourceName,
            "输出文件": result.outputName or "",
            "状态": STATUS_LABELS.get(result.status, result.status),
            "说明": result.message,
        }
        for result in results
    ]


def writeReportCsv(
    results: Sequence[BatchItemResult],
    outputPath: str | Path,
) -> Path:
    """把批量转换报告写入 UTF-8 CSV 文件。"""
    targetPath = Path(outputPath)
    targetPath.parent.mkdir(parents=True, exist_ok=True)
    rows = buildReportRows(results)

    with targetPath.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["源文件", "输出文件", "状态", "说明"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return targetPath