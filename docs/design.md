# 项目设计文档

## 1. 架构概览

应用采用 Python 分层设计：

```text
Streamlit 网页界面
        ↓
批量任务管理
        ↓
文件类型检测与转换路由
        ↓
PDF / Word / Excel / 文本转换器
        ↓
Markdown 整理与文件输出
        ↓
预览、报告和 ZIP 打包
```

## 2. 模块划分

### 网页入口

负责上传文件、显示状态、预览 Markdown 和提供下载。

### 转换模块

- `router.py`：根据扩展名选择转换器。
- `pdf.py`：处理电子版 PDF。
- `word.py`：处理 DOCX。
- `excel.py`：处理多个工作表和 Excel 文件。
- `text.py`：处理 CSV 和 TSV。

### 输出模块

- `writer.py`：写入 Markdown 文件。
- `archive.py`：生成 ZIP 压缩包。
- `reporting.py`：生成转换报告。

### 工具模块

- `filetypes.py`：检测文件类型和扫描版 PDF。
- `markdown.py`：处理 Markdown 转义和内容整理。

## 3. 数据流

1. 浏览器把上传文件保存到临时工作目录。
2. 系统检测扩展名和文件有效性。
3. 转换路由把文件交给对应转换器。
4. 转换器返回统一的 Markdown 内容和错误状态。
5. 输出模块写入 Markdown 并生成报告。
6. 系统打包 ZIP 并返回浏览器。

## 4. 技术选型

- Python 3.13
- Streamlit
- MarkItDown
- PyMuPDF4LLM
- openpyxl
- xlrd
- charset-normalizer
- pytest

## 5. 关键设计决策

### 程序运行时不调用 AI

普通文档优先使用稳定的本地解析库，避免网络依赖、额外费用和内容幻觉。

### 先统一输出为 Markdown

Markdown 是纯文本，方便阅读、搜索、修改、版本管理和后续交给 AI 处理。

### 使用模块化转换器

不同格式的解析逻辑互相隔离，后续加入 OCR 或新格式时不需要重写整个应用。

## 6. 已知限制

标准 Markdown 无法完整保存合并单元格、颜色、字体、页眉页脚和复杂页面布局。扫描版 PDF 首版只检测并提示，不进行 OCR。
## 7. 阶段一实现情况

- `result.py`：定义统一转换结果和转换异常。
- `router.py`：根据扩展名分派转换器。
- `text.py`：转换 CSV 和 TSV。
- `excel.py`：转换 XLSX、XLSM 和 XLS。
- `word.py`：转换 DOCX。
- `pdf.py`：转换电子版 PDF，并关闭 OCR。
- `writer.py`：把转换结果写入 Markdown 文件。
- `document.py`：封装 MarkItDown 共享调用。
- `filetypes.py`：统一维护支持的文件类型。
## 8. 阶段二实现情况

- `app.py`：提供多文件上传、进度展示、结果预览和 ZIP 下载。
- `batch.py`：按顺序处理文件，隔离单个文件错误，并处理重名文件。
- `reporting.py`：生成页面报告和 `report.csv`。
- `archive.py`：把 Markdown 文件和报告打包为 ZIP。
- 转换过程使用临时目录，任务结束后自动清理。
- ZIP 结构包含 `converted/` 目录和 `report.csv`。
## 9. 阶段三实现情况

- 每次转换自动保存到 `output/run-时间戳`，避免覆盖历史结果。
- 网页增加每个 Markdown 文件的单独下载按钮。
- CSV 优先识别 UTF-8 BOM，并支持 GBK/GB18030 自动检测。
- Excel 增加公式文本回退、日期格式化、整数和小数格式化。
- 补充 XLS、XLSM、错误尺寸、损坏文件和空文件测试。
- 补充多页 PDF、空文字层 PDF 和损坏 PDF 测试。
- 已完成 7 个真实桌面文件批量转换，全部成功。
## 10. 界面视觉设计

- 采用专业清爽的浅色风格，主色为蓝色。
- 顶部使用品牌标题卡片，并展示支持格式标签。
- 主区域采用左侧操作栏、右侧结果区布局。
- 左侧包含上传、转换、清空、格式提示和限制说明。
- 右侧在未转换时显示空状态，转换后显示统计卡片。
- 每个结果使用独立卡片，支持单独下载和预览。
- 转换报告默认折叠，减少页面信息拥挤。
- 样式集中在 `src/main/styles.py`，组件集中在 `src/main/components.py`。