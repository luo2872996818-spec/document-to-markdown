# 测试 Word DOCX 转换器
from zipfile import ZIP_DEFLATED, ZipFile

from src.modules.conversion.word import convertWord


def createMinimalDocx(filePath, text: str) -> None:
    """创建一个只包含一段文字的最小 DOCX 测试文件。"""
    contentTypes = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
    relationships = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>{text}</w:t></w:r></w:p>
    <w:sectPr/>
  </w:body>
</w:document>"""

    with ZipFile(filePath, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", contentTypes)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("word/document.xml", document)


def test_convertWord(tmp_path) -> None:
    """验证 DOCX 正文可以转换为 Markdown。"""
    filePath = tmp_path / "测试文档.docx"
    createMinimalDocx(filePath, "阶段一 Word 测试")

    result = convertWord(filePath)

    assert result.converterName == "word"
    assert "阶段一 Word 测试" in result.markdownText
    assert result.metadata["characterCount"] > 0