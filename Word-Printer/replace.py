from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from pictureIns import pictureIns

fileName = 'ABMM'
company = '黄铸韬无限公司'
address = '广州市最高的那栋楼'
introduction = 'abm御用公司，简介还用写？？？'
coverField = '美利坚合众国的一切'
manager = '狗腿1号郑经理'
guandai = '狗腿2号黄管代'
employees = '编制人员旭某人'
allower = '批准人东某人'
announceDate = '8102年3月22日'
auditDate = '9102年5月8日'
picPath = 'result.gv.png'

def replace( src , dst ):
    document = Document(src)
    todo = []

    #页眉页脚
    for s in document.sections:
        for p in s.footer.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == 7:
                    todo.append(r)
        for p in s.header.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == 7:
                    todo.append(r)

    #表格
    for t in document.tables:
        for c in t.columns:
            for cc in c.cells:
                for p in cc.paragraphs:
                    for r in p.runs:
                        if r.font.highlight_color == 7 :
                            todo.append(r)
    
    #正文
    for p in document.paragraphs:
        for r in p.runs:
            if r.font.highlight_color == 7:
                todo.append(r)
    
    #替换
    for r in todo:
        if str(r.font.color.rgb) == 'FFF000':
            r.text = fileName
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == 'FF0000':
            r.text = company
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '00FF00':
            r.text = address
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '0000FF':
            r.text = introduction
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == 'FFFF00':
            r.text = coverField
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '00FFFF':
            r.text = manager
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '7F0000':
            r.text = guandai
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '007F00':
            r.text = employees
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '000080':
            r.text = allower
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '7F7F00':
            r.text = announceDate
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '007F7F':
            r.text = auditDate
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    document.save(dst)

    #插入图片
    pictureIns(dst,dst,picPath)

    print('成功')
    pass

if __name__ == '__main__':
    replace('sample.docx',fileName+'-20000-SM-M-01.docx')