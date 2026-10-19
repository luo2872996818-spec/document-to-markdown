# 把转换结果和报告打包为 ZIP 文件
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def createArchive(
    sourceDirectory: str | Path,
    archivePath: str | Path,
) -> Path:
    """把目录中的全部文件打包为 ZIP，保留目录结构。"""
    sourceRoot = Path(sourceDirectory)
    targetPath = Path(archivePath)
    if not sourceRoot.is_dir():
        raise FileNotFoundError(f"待打包目录不存在：{sourceRoot}")

    targetPath.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(targetPath, "w", ZIP_DEFLATED) as archive:
        for filePath in sorted(sourceRoot.rglob("*")):
            if not filePath.is_file():
                continue
            if filePath.resolve() == targetPath.resolve():
                continue
            archive.write(
                filePath,
                filePath.relative_to(sourceRoot).as_posix(),
            )

    return targetPath