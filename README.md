![Document to Markdown](assets/banner.svg)

# Document to Markdown

一个本地运行的批量文档转换工具，把电子版 PDF、Word、Excel 和 CSV 文件统一转换为 Markdown。

[下载 Windows 版本](../../releases/latest) · [查看文档](docs/README.md) · [测试报告](docs/test-report.md)

## 功能

- 批量上传和转换多个文档
- 支持电子版 PDF、DOCX、XLSX、XLSM、XLS、CSV、TSV
- 自动识别 CSV 的 UTF-8、BOM、GBK/GB18030 编码
- Excel 支持多工作表、公式回退、日期和数字格式化
- 自动生成 Markdown 渲染预览和源码预览
- 支持单独下载 `.md` 文件
- 支持打包下载 ZIP 和转换报告
- 单个文件失败不会中断整个批量任务
- 每次转换保存到独立的 `output/run-时间戳` 目录
- 程序运行时不调用在线 AI，文档只在本机处理

## Windows 独立版本

前往 [Releases](../../releases/latest) 下载：

```text
DocumentToMarkdown-Windows-x64.zip
```

解压后双击：

```text
DocumentToMarkdown.exe
```

浏览器会自动打开 `http://localhost:8501`。使用者不需要安装 Python。

> Windows 可能显示“未知发布者”，这是未签名程序的常见 SmartScreen 提示。

## 从源码运行

环境要求：

- Windows 10/11
- Python 3.13

安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

启动：

```powershell
.\.venv\Scripts\streamlit.exe run src\main\app.py
```

也可以双击项目根目录中的 `start.bat`。

## 使用方式

1. 在左侧上传一个或多个文件
2. 点击“开始批量转换”
3. 在右侧查看状态、预览和转换报告
4. 单独下载 Markdown 或下载完整 ZIP
5. 转换结果同时保存到 `output` 目录

## 支持格式

| 格式 | 支持情况 |
|---|---|
| 电子版 PDF | 支持 |
| 扫描版 PDF | 暂不支持 OCR |
| DOCX | 支持 |
| DOC 旧版 Word | 暂不支持 |
| XLSX、XLSM | 支持 |
| XLS | 支持 |
| CSV、TSV | 支持 |

## 已知限制

- 扫描版 PDF 不进行 OCR
- 复杂 PDF 表格质量取决于原始 PDF 结构
- 标准 Markdown 无法完整保存颜色、合并单元格和复杂版式
- Excel 公式没有缓存结果时保留公式文本，不进行计算
- 程序不调用在线 AI

## 构建独立发行包

安装构建依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
```

执行构建：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\build-package.ps1
```

输出：

```text
release/DocumentToMarkdown-Windows-x64.zip
```

详细说明见 [docs/release.md](docs/release.md)。

## 测试

运行全部自动化测试：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

当前结果：

```text
22 passed
```

打包程序自检：

```powershell
.\dist\DocumentToMarkdown\DocumentToMarkdown.exe --self-test
```

```text
[PASS] CSV
[PASS] Excel
[PASS] PDF
Self test finished: 3/3 passed
```

## 项目结构

```text
document-to-markdown/
├── assets/                  # 界面资源和横幅
├── docs/                    # 需求、设计、测试和总结
├── package-assets/          # 独立发行包附带说明
├── src/
│   ├── main/                # 网页入口、样式、组件和启动器
│   ├── modules/             # 转换、批量处理、报告和打包
│   └── utils/               # Markdown、文件类型和文档工具
├── tests/                   # 自动化测试
├── build-package.ps1        # Windows 打包脚本
├── DocumentToMarkdown.spec  # PyInstaller 配置
├── requirements.txt         # 运行和测试依赖
└── requirements-build.txt   # 构建依赖
```

## 技术栈

- Python 3.13
- Streamlit
- MarkItDown
- PyMuPDF4LLM / PyMuPDF
- openpyxl / xlrd
- charset-normalizer
- pytest
- PyInstaller

## 开发文档

- [项目说明](docs/README.md)
- [需求文档](docs/requirements.md)
- [设计文档](docs/design.md)
- [测试报告](docs/test-report.md)
- [发行包说明](docs/release.md)
- [开发笔记](docs/notes.md)
- [项目总结](docs/summary.md)

## License

[MIT](LICENSE)