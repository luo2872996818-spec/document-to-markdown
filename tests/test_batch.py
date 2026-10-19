# 测试批量转换、重名处理和错误隔离
from src.modules.batch import processBatch
from src.modules.packaging.reporting import buildReportRows, writeReportCsv


def test_processBatchAndReport(tmp_path) -> None:
    """验证重复文件名会重命名，失败文件不会中断任务。"""
    firstDirectory = tmp_path / "first"
    secondDirectory = tmp_path / "second"
    firstDirectory.mkdir()
    secondDirectory.mkdir()

    firstFile = firstDirectory / "数据.csv"
    secondFile = secondDirectory / "数据.csv"
    unsupportedFile = tmp_path / "说明.txt"
    firstFile.write_text("名称,数量\n铅笔,5\n", encoding="utf-8")
    secondFile.write_text("名称,数量\n钢笔,8\n", encoding="utf-8")
    unsupportedFile.write_text("不支持", encoding="utf-8")

    progressItems: list[tuple[int, int, str]] = []
    results = processBatch(
        [firstFile, secondFile, unsupportedFile],
        tmp_path / "output",
        lambda current, total, item: progressItems.append(
            (current, total, item.status)
        ),
    )

    assert [item.status for item in results] == [
        "success",
        "success",
        "failed",
    ]
    assert [item.outputName for item in results] == [
        "数据.md",
        "数据-2.md",
        None,
    ]
    assert (tmp_path / "output" / "converted" / "数据.md").is_file()
    assert (tmp_path / "output" / "converted" / "数据-2.md").is_file()
    assert progressItems == [
        (1, 3, "success"),
        (2, 3, "success"),
        (3, 3, "failed"),
    ]

    reportPath = writeReportCsv(results, tmp_path / "output" / "report.csv")
    reportText = reportPath.read_text(encoding="utf-8-sig")
    assert "成功" in reportText
    assert "失败" in reportText
    assert buildReportRows(results)[2]["输出文件"] == ""