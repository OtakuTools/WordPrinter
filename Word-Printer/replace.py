from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from pictureIns import pictureIns
from dataStruct import userInfo
from docx.enum.text import WD_COLOR_INDEX

def replace( src , dst , user ):
    document = Document(src)
    todo = []

    #页眉页脚
    for s in document.sections:
        for p in s.footer.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    todo.append(r)
        for p in s.header.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    todo.append(r)

    #表格
    for t in document.tables:
        for c in t.columns:
            for cc in c.cells:
                for p in cc.paragraphs:
                    for r in p.runs:
                        if r.font.highlight_color == WD_COLOR_INDEX.YELLOW :
                            todo.append(r)
    
    #正文
    for p in document.paragraphs:
        for r in p.runs:
            if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                todo.append(r)
    
    #替换
    for r in todo:
        if str(r.font.color.rgb) == 'FFF000':
            r.text = user.fileName
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == 'FF0000':
            r.text = user.company
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '00FF00':
            r.text = user.address
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '0000FF':
            r.text = user.introduction
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == 'FFFF00':
            r.text = user.coverField
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '00FFFF':
            r.text = user.manager
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '7F0000':
            r.text = user.guandai
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '007F00':
            r.text = user.employees
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '000080':
            r.text = user.allower
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '7F7F00':
            r.text = user.announceDate
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '007F7F':
            r.text = user.auditDate
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    document.save(dst)

    #插入图片
    pictureIns(dst,dst,user.picPath)

    print('成功')
    pass

if __name__ == '__main__':
    user = userInfo();
    user.fileName = 'ABMM'
    user.company = '黄铸韬无限公司'
    user.address = '广州市最高的那栋楼'
    user.introduction = 'abm御用公司，简介还用写？？？'
    user.coverField = '美利坚合众国的一切'
    user.manager = '狗腿1号郑经理'
    user.guandai = '狗腿2号黄管代'
    user.employees = '编制人员旭某人'
    user.allower = '批准人东某人'
    user.announceDate = '8102年3月22日'
    user.auditDate = '9102年5月8日'
    user.picPath = 'result.gv.png'

    replace('sample.docx',user.fileName+'-20000-SM-M-01.docx' , user )