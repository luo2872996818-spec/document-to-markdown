# Document to Markdown

## 项目简介

本项目是一个本地运行的批量文档转换工具，用于把电子版 PDF、Word、Excel、CSV 和 TSV 文件统一转换为 Markdown。

## 当前状态

阶段 3：稳定性、边界处理和真实文件验证已完成。

## 使用方式

1. 在浏览器中打开本地网页。
2. 一次选择多个待转换文件。
3. 点击“开始批量转换”。
4. 查看转换状态、统计、报告和 Markdown 预览。
5. 下载全部 Markdown 结果和转换报告压缩包。

## 支持范围

- 电子版 PDF
- DOCX
- XLSX、XLSM
- XLS
- CSV、TSV

## 暂不支持

- 扫描版 PDF 和图片 OCR
- DOC 旧版 Word 文件
- 完整保留字体、颜色、页眉页脚和复杂版式
- 运行时调用在线 AI

## 环境要求

- Windows
- Python 3.13
- 项目独立虚拟环境 `.venv`

## 项目结构

```text
document-to-markdown/
├── docs/
├── src/
│   ├── main/
│   ├── modules/
│   └── utils/
├── tests/
├── assets/
├── requirements.txt
├── .gitignore
└── .venv/
```

## 本地启动

在项目目录打开 PowerShell，然后执行：

```powershell
.\.venv\Scripts\streamlit.exe run src\main\app.py
```

浏览器默认访问地址为 `http://localhost:8501`。

## 输出结构

下载的 ZIP 中包含：

```text
converted/
├── 文档1.md
└── 文档2.md
report.csv
```
## 固定输出目录

每次转换会保存到：

```text
output/run-日期-时间/
├── converted/
└── report.csv
```

网页中也支持单独下载每个 `.md` 文件。
## 一键启动

可以直接双击项目根目录中的：

```text
start.bat
```

启动后访问 `http://localhost:8501`。关闭命令行窗口即可停止服务。
## Windows 桌面快捷方式

项目已支持桌面点击启动。快捷方式实际指向项目根目录中的 `start.bat`。

如果移动了项目目录，需要重新创建快捷方式或修改快捷方式目标。双击后会自动启动本地服务并打开浏览器。
## Windows 独立发行包

可以发给其他 Windows 10/11 64 位用户：

```text
release\DocumentToMarkdown-Windows-x64.zip
```

对方解压后双击 `DocumentToMarkdown.exe` 即可使用，不需要安装 Python。

详细的打包和校验说明见 `docs/release.md`。