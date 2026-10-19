# 测试 ZIP 打包模块
from zipfile import ZipFile

from src.modules.packaging.archive import createArchive


def test_createArchive(tmp_path) -> None:
    """验证 ZIP 会保留 converted 目录结构。"""
    sourceDirectory = tmp_path / "output"
    convertedDirectory = sourceDirectory / "converted"
    convertedDirectory.mkdir(parents=True)
    (convertedDirectory / "文档.md").write_text(
        "# 文档\n",
        encoding="utf-8",
    )
    (sourceDirectory / "report.csv").write_text(
        "源文件,状态\n文档.csv,成功\n",
        encoding="utf-8-sig",
    )

    archivePath = createArchive(sourceDirectory, tmp_path / "结果.zip")

    assert archivePath.is_file()
    with ZipFile(archivePath) as archive:
        names = set(archive.namelist())
    assert "converted/文档.md" in names
    assert "report.csv" in names