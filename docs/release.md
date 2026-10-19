# Windows 发行包说明

## 最终文件

```text
release/DocumentToMarkdown-Windows-x64.zip
```

压缩包大小约 185 MB。解压后约 380 MB，包含 3500 多个依赖文件，这是 Streamlit、PDF、Excel 和 Word 解析库共同造成的结果。

## 用户使用方法

1. 解压整个 `DocumentToMarkdown` 文件夹。
2. 双击 `DocumentToMarkdown.exe`。
3. 等待浏览器自动打开。
4. 如果浏览器没有自动打开，访问 `http://localhost:8501`。
5. 转换结果保存在程序目录的 `output` 文件夹中。
6. 关闭命令窗口即可停止工具。

用户不需要安装 Python，也不需要项目源码。

## SHA256

```text
FDEE6D1225138B19331A3C2AEF82D8024C575868636E5535C05795C144795C6A
```

该值对应当前生成的文件。重新打包后需要更新。

## 重新构建

安装构建依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
```

执行打包：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\build-package.ps1
```

构建脚本会：

1. 调用 PyInstaller。
2. 生成 `dist/DocumentToMarkdown`。
3. 复制用户使用说明。
4. 创建 Windows x64 ZIP。
5. 生成 SHA256 校验文件。

## 打包自检

可以运行：

```powershell
.\dist\DocumentToMarkdown\DocumentToMarkdown.exe --self-test
```

该命令会创建临时 CSV、Excel 和 PDF 文件，验证打包程序中的转换依赖是否完整。

预期结果：

```text
[PASS] CSV
[PASS] Excel
[PASS] PDF
Self test finished: 3/3 passed
```

## 注意事项

- 程序未购买代码签名证书，Windows SmartScreen 可能提示“未知发布者”。
- 不要把单个 `DocumentToMarkdown.exe` 单独复制出去，必须携带 `_internal` 文件夹。
- 项目目录移动后，桌面开发快捷方式需要重新创建，但不影响该发行包。
- 扫描版 PDF OCR 和 DOC 旧版 Word 仍不在当前支持范围内。