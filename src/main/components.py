# 提供页面标题、结果卡片和统计区域等界面组件
import html
from pathlib import Path

import streamlit as st

from src.modules.batch import BatchItemResult
from src.modules.packaging.reporting import buildReportRows

STATUS_LABELS = {
    "success": "转换成功",
    "warning": "成功但有提示",
    "failed": "转换失败",
}

STATUS_ICONS = {
    "success": "✅",
    "warning": "⚠️",
    "failed": "❌",
}


def renderHeader() -> None:
    """显示产品标题、简介和支持格式。"""
    formatNames = ["PDF", "DOCX", "XLSX", "XLSM", "XLS", "CSV", "TSV"]
    formatChips = "".join(
        f'<span class="format-chip">{name}</span>'
        for name in formatNames
    )
    st.markdown(
        f"""
        <section class="app-header">
            <div class="eyebrow">LOCAL DOCUMENT CONVERTER</div>
            <h1>📄 文档批量转 Markdown</h1>
            <p>本地转换 · 安全 · 批量处理 · 自动生成报告</p>
            <div class="chip-row">{formatChips}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def renderEmptyState() -> None:
    """显示尚未转换时的引导状态。"""
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📂</div>
            <h3>还没有转换结果</h3>
            <p>
                在左侧上传 PDF、Word、Excel 或 CSV 文件，
                然后点击“开始批量转换”。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderSummary(results: list[BatchItemResult]) -> None:
    """显示批量转换统计卡片。"""
    successCount = sum(item.status == "success" for item in results)
    warningCount = sum(item.status == "warning" for item in results)
    failedCount = sum(item.status == "failed" for item in results)

    firstColumn, secondColumn, thirdColumn, fourthColumn = st.columns(4)
    firstColumn.metric("文件总数", len(results), border=True)
    secondColumn.metric("成功", successCount, border=True)
    thirdColumn.metric("有提示", warningCount, border=True)
    fourthColumn.metric("失败", failedCount, border=True)


def renderResultCard(item: BatchItemResult, index: int) -> None:
    """显示单个文件的转换状态、下载和预览。"""
    status = item.status if item.status in STATUS_LABELS else "success"
    statusLabel = STATUS_LABELS[status]
    icon = STATUS_ICONS.get(status, "ℹ️")
    sourceName = html.escape(item.sourceName)
    outputName = html.escape(item.outputName or "未生成文件")

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="result-heading">
                <span class="status-pill status-{status}">{statusLabel}</span>
                <strong>{sourceName}</strong>
            </div>
            <div class="output-caption">输出：{outputName}</div>
            """,
            unsafe_allow_html=True,
        )

        if item.status == "failed":
            st.error(item.message)
            return
        if item.warningMessage:
            st.warning(item.warningMessage)

        if item.outputName and item.markdownText:
            st.download_button(
                label=f"{icon} 单独下载此 Markdown",
                data=item.markdownText.encode("utf-8"),
                file_name=item.outputName,
                mime="text/markdown",
                key=f"downloadMarkdown-{index}",
                width="stretch",
            )

        previewTab, sourceTab = st.tabs(["渲染预览", "Markdown 源码"])
        with previewTab:
            st.markdown(item.markdownText or "")
        with sourceTab:
            st.code(item.markdownText or "", language="markdown")


def renderResultsPanel(
    results: list[BatchItemResult],
    archiveBytes: bytes,
    outputDirectory: Path,
) -> None:
    """显示统计、下载、报告和全部结果卡片。"""
    st.markdown('<div class="panel-title">转换结果</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-subtitle">预览转换内容，并下载单个文件或完整压缩包。</div>',
        unsafe_allow_html=True,
    )
    renderSummary(results)
    st.caption(f"文件已保存到：{outputDirectory}")

    st.download_button(
        label="下载全部 Markdown 和转换报告",
        data=archiveBytes,
        file_name="markdown-results.zip",
        mime="application/zip",
        type="primary",
        width="stretch",
    )

    with st.expander("查看转换报告", expanded=False):
        st.dataframe(
            buildReportRows(results),
            width="stretch",
            hide_index=True,
        )

    st.markdown("#### 文件结果")
    for index, item in enumerate(results):
        renderResultCard(item, index)