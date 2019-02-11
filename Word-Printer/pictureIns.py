from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def pictureIns(src,dst,pic):
    document = Document(src)
    for p in document.paragraphs:
        for r in p.runs:
            if r.font.highlight_color == 7 and str(r.font.color.rgb) == '000FFF':
                r.font.highlight_color = None
                r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
                pp = p.insert_paragraph_before()
                pp.add_run().add_picture(pic)
                pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.save(dst)
    print('图片插入成功')
    pass
