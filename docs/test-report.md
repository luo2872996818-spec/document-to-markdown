# 阶段 3 测试报告

## 测试日期

2026-09-25

## 自动化测试

执行命令：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

结果：

```text
22 passed
```

## 真实文件批量测试

使用用户桌面上的真实学习论坛样本，共 7 个文件：

- 5 个 DOCX
- 1 个电子版 PDF
- 1 个 XLSX

测试结果：

```text
文件总数：7
成功：7
失败：0
```

其中 Excel 文件完整读取了：

- 1 个工作表
- 151 行
- 7 列
- 150 行提交数据

## 已覆盖的边界情况

- UTF-8 CSV
- UTF-8 BOM CSV
- GBK/GB18030 CSV
- TSV
- XLSX 多工作表
- XLSX 错误尺寸元数据
- XLSX 无缓存结果的公式
- XLS 旧版文件
- XLSM 文件
- 损坏的 Excel
- DOCX 普通段落
- DOCX 表格
- 多页电子版 PDF
- 空文字层 PDF
- 损坏的 PDF
- 重复输出文件名
- 单个文件失败隔离
- ZIP 打包
- 单独 Markdown 下载
- 固定输出目录

## 当前已知限制

- 扫描版 PDF 不进行 OCR。
- DOC 旧版 Word 文件暂不支持。
- 标准 Markdown 不能完整表达合并单元格、颜色和复杂页面布局。
- 复杂 PDF 表格的转换质量取决于 PDF 内部结构。
- Excel 公式没有缓存结果时，当前输出公式文本而不是计算结果。