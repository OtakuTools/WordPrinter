from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from pictureIns import pictureIns
from dataStruct import userInfo
from docx.enum.text import WD_COLOR_INDEX
import json

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
                if str(r.font.color.rgb) == 'FF00FF':
                    p.clear()
                    for d in user.departments:
                        p.insert_paragraph_before( d['name'] + ':' , 'Heading 3' )
                        for i in d['intro']:
                            p.insert_paragraph_before( i , 'Heading 4' )
    
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
            r.text = '\n'.join(user.introduction)
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == 'FFFF00':
            r.text = '\n'.join(user.coverField)
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
            r.text = user.approver
            r.font.highlight_color = None
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if str(r.font.color.rgb) == '7F7F00':
            r.text = user.releaseDate
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
    with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
    for dict in data:
        for key in dict.keys():
            setattr( user , key , dict[key] )
        replace('sample.docx',user.fileName+'-20000-SM-M-01.docx' , user )