# 测试固定输出目录的创建规则
from src.modules.packaging.persistence import createRunDirectory


def test_createRunDirectoryAvoidsOverwrite(tmp_path) -> None:
    """验证同一时间的转换任务不会覆盖旧目录。"""
    outputRoot = tmp_path / "output"

    firstPath = createRunDirectory(outputRoot, timestamp="20260925-120000")
    secondPath = createRunDirectory(outputRoot, timestamp="20260925-120000")

    assert firstPath.name == "run-20260925-120000"
    assert secondPath.name == "run-20260925-120000-2"
    assert firstPath.is_dir()
    assert secondPath.is_dir()