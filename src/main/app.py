# 创建文档批量转 Markdown 的 Streamlit 网页入口
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

# 资源目录用于查找代码；APP_HOME 用于保存输出和报告
RESOURCE_ROOT = Path(__file__).resolve().parents[2]
APP_HOME = Path(
    os.environ.get("DOCUMENT_TO_MARKDOWN_HOME", str(RESOURCE_ROOT))
).resolve()
if str(RESOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(RESOURCE_ROOT))

import streamlit as st

from src.main.components import (
    renderEmptyState,
    renderHeader,
    renderResultsPanel,
)
from src.main.styles import applyStyles
from src.modules.batch import BatchItemResult, processBatch, sanitizeFileName
from src.modules.packaging.archive import createArchive
from src.modules.packaging.persistence import createRunDirectory
from src.modules.packaging.reporting import writeReportCsv
from src.utils.filetypes import SUPPORTED_EXTENSIONS

UPLOAD_TYPES = sorted(extension[1:] for extension in SUPPORTED_EXTENSIONS)


def buildUploadName(fileName: str, usedNames: set[str]) -> str:
    """为上传文件生成合法且唯一的临时文件名。"""
    originalPath = Path(fileName)
    safeStem = sanitizeFileName(originalPath.stem)
    suffix = originalPath.suffix.lower()
    candidate = f"{safeStem}{suffix}"
    counter = 2

    while candidate.casefold() in usedNames:
        candidate = f"{safeStem}_{counter}{suffix}"
        counter += 1

    usedNames.add(candidate.casefold())
    return candidate


def saveUploadedFiles(
    uploadedFiles: list[Any],
    inputDirectory: Path,
) -> list[Path]:
    """把浏览器上传的文件保存到临时输入目录。"""
    inputDirectory.mkdir(parents=True, exist_ok=True)
    savedPaths: list[Path] = []
    usedNames: set[str] = set()

    for uploadedFile in uploadedFiles:
        uploadName = buildUploadName(uploadedFile.name, usedNames)
        filePath = inputDirectory / uploadName
        filePath.write_bytes(uploadedFile.getvalue())
        savedPaths.append(filePath)

    return savedPaths


def processUploadedFiles(
    uploadedFiles: list[Any],
) -> tuple[list[BatchItemResult], bytes, Path]:
    """执行批量任务，返回结果、ZIP 内容和固定输出目录。"""
    runDirectory = createRunDirectory(APP_HOME / "output")

    with tempfile.TemporaryDirectory(prefix="document-to-markdown-") as tempRoot:
        tempDirectory = Path(tempRoot)
        inputDirectory = tempDirectory / "input"
        archivePath = tempDirectory / "markdown-results.zip"
        sourcePaths = saveUploadedFiles(uploadedFiles, inputDirectory)
        progressBar = st.progress(0, text="准备开始转换……")

        def updateProgress(current: int, total: int, item: BatchItemResult) -> None:
            # 每处理完一个文件就更新页面进度
            progressBar.progress(
                current / total,
                text=f"正在处理 {current}/{total}：{item.sourceName}",
            )

        results = processBatch(
            sourcePaths,
            runDirectory,
            progressCallback=updateProgress,
        )
        writeReportCsv(results, runDirectory / "report.csv")
        createArchive(runDirectory, archivePath)
        return results, archivePath.read_bytes(), runDirectory


def renderControlPanel() -> tuple[list[Any], bool, bool]:
    """显示左侧上传、操作说明和转换按钮。"""
    with st.container(border=True):
        st.markdown('<div class="panel-title">操作面板</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-subtitle">按顺序完成上传、转换和下载。</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="step-label">① 上传文档</div>', unsafe_allow_html=True)

        uploadedFiles = st.file_uploader(
            "选择待转换文件",
            type=UPLOAD_TYPES,
            accept_multiple_files=True,
            help="可以一次选择多个文件；单个文件失败不会影响其他文件。",
            label_visibility="collapsed",
        )

        if uploadedFiles:
            totalBytes = sum(len(item.getvalue()) for item in uploadedFiles)
            st.caption(
                f"已选择 {len(uploadedFiles)} 个文件，共 {totalBytes / 1024 / 1024:.2f} MB"
            )

        st.markdown('<div class="step-label">② 开始转换</div>', unsafe_allow_html=True)
        startConversion = st.button(
            "开始批量转换",
            type="primary",
            width="stretch",
            disabled=not uploadedFiles,
        )
        clearResults = st.button("清空结果", width="stretch")

        chips = "".join(
            f'<span class="format-chip">{extension[1:].upper()}</span>'
            for extension in sorted(SUPPORTED_EXTENSIONS)
        )
        st.markdown(
            f'<div class="chip-row light-chips">{chips}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="tip-card">扫描版 PDF 暂不支持 OCR；'
            '复杂排版无法完整保留。</div>',
            unsafe_allow_html=True,
        )

    return uploadedFiles, startConversion, clearResults


def main() -> None:
    """组织页面布局和处理 Streamlit 页面状态。"""
    st.set_page_config(
        page_title="文档批量转 Markdown",
        page_icon="📄",
        layout="wide",
    )
    applyStyles()
    renderHeader()

    leftColumn, rightColumn = st.columns([0.36, 0.64], gap="large")
    with leftColumn:
        uploadedFiles, startConversion, clearResults = renderControlPanel()

    if clearResults:
        st.session_state.pop("batchResults", None)
        st.session_state.pop("archiveBytes", None)
        st.session_state.pop("outputDirectory", None)

    if startConversion and uploadedFiles:
        try:
            with st.spinner("正在批量转换，请稍候……"):
                results, archiveBytes, outputDirectory = processUploadedFiles(
                    uploadedFiles
                )
            st.session_state["batchResults"] = results
            st.session_state["archiveBytes"] = archiveBytes
            st.session_state["outputDirectory"] = str(outputDirectory)
        except Exception as error:
            st.error(f"批量任务执行失败：{error}")

    with rightColumn:
        if (
            "batchResults" in st.session_state
            and "archiveBytes" in st.session_state
            and "outputDirectory" in st.session_state
        ):
            renderResultsPanel(
                st.session_state["batchResults"],
                st.session_state["archiveBytes"],
                Path(st.session_state["outputDirectory"]),
            )
        else:
            renderEmptyState()


main()