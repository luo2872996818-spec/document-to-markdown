# 创建不会互相覆盖的转换结果目录
from datetime import datetime
from pathlib import Path


def createRunDirectory(
    outputRoot: str | Path,
    timestamp: str | None = None,
) -> Path:
    """创建按时间命名的输出目录，目录重名时自动增加序号。"""
    rootPath = Path(outputRoot)
    timeLabel = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = rootPath / f"run-{timeLabel}"
    counter = 2

    while candidate.exists():
        candidate = rootPath / f"run-{timeLabel}-{counter}"
        counter += 1

    candidate.mkdir(parents=True, exist_ok=False)
    return candidate