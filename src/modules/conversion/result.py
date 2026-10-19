# 定义转换过程使用的统一数据结构和异常类型
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConversionError(RuntimeError):
    """表示文档无法按照当前支持范围完成转换。"""


@dataclass(slots=True)
class ConversionResult:
    """保存一次文档转换的结果和附加信息。"""

    sourcePath: Path
    markdownText: str
    converterName: str
    warningMessage: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)