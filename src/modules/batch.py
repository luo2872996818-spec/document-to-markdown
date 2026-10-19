# 实现批量文档转换、重名处理和单文件错误隔离
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from src.modules.conversion.result import ConversionError
from src.modules.conversion.router import convertDocument
from src.modules.packaging.writer import writeMarkdown


@dataclass(slots=True)
class BatchItemResult:
    """保存批量任务中单个文件的处理结果。"""

    sourceName: str
    outputName: str | None
    status: str
    message: str
    markdownText: str | None = None
    warningMessage: str | None = None


ProgressCallback = Callable[[int, int, BatchItemResult], None]


def sanitizeFileName(fileName: str) -> str:
    """删除 Windows 文件名中的非法字符。"""
    safeName = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", fileName)
    safeName = safeName.strip(" .")
    return safeName or "document"


def createUniqueOutputName(filePath: Path, usedNames: set[str]) -> str:
    """生成不会在当前批次中重复的 Markdown 文件名。"""
    baseName = sanitizeFileName(filePath.stem)
    candidate = f"{baseName}.md"
    counter = 2

    while candidate.casefold() in usedNames:
        candidate = f"{baseName}-{counter}.md"
        counter += 1

    usedNames.add(candidate.casefold())
    return candidate


def convertBatchItem(
    sourcePath: Path,
    outputName: str,
    convertedDirectory: Path,
) -> BatchItemResult:
    """转换单个文件，并把异常转换成批量结果。"""
    try:
        conversionResult = convertDocument(sourcePath)
        writeMarkdown(
            conversionResult,
            convertedDirectory / outputName,
        )
    except ConversionError as error:
        return BatchItemResult(
            sourceName=sourcePath.name,
            outputName=None,
            status="failed",
            message=str(error),
        )
    except Exception as error:
        return BatchItemResult(
            sourceName=sourcePath.name,
            outputName=None,
            status="failed",
            message=f"未预期的转换错误：{error}",
        )

    status = "warning" if conversionResult.warningMessage else "success"
    return BatchItemResult(
        sourceName=sourcePath.name,
        outputName=outputName,
        status=status,
        message=conversionResult.warningMessage or "转换成功",
        markdownText=conversionResult.markdownText,
        warningMessage=conversionResult.warningMessage,
    )


def processBatch(
    filePaths: Sequence[str | Path],
    outputDirectory: str | Path,
    progressCallback: ProgressCallback | None = None,
) -> list[BatchItemResult]:
    """按顺序转换一批文件，单个文件失败不会中断任务。"""
    convertedDirectory = Path(outputDirectory) / "converted"
    convertedDirectory.mkdir(parents=True, exist_ok=True)

    usedNames: set[str] = set()
    results: list[BatchItemResult] = []
    totalCount = len(filePaths)

    for index, rawPath in enumerate(filePaths, start=1):
        sourcePath = Path(rawPath)
        outputName = createUniqueOutputName(sourcePath, usedNames)
        itemResult = convertBatchItem(
            sourcePath,
            outputName,
            convertedDirectory,
        )
        results.append(itemResult)

        if progressCallback:
            progressCallback(index, totalCount, itemResult)

    return results