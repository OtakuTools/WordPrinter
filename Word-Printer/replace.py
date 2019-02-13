from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from dataStruct import userInfo
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json

def replace( src , dst , user ):
    document = Document(src)
    todo = []

    #页眉页脚
    for s in document.sections:
        for p in s.footer.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    r.text = user.company
                    r.font.highlight_color = None
                    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        for p in s.header.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    r.text = user.fileName
                    r.font.highlight_color = None
                    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

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
                # 部门介绍
                if str(r.font.color.rgb) == 'FF00FF':
                    p.clear()
                    for d in user.departments:
                        p.insert_paragraph_before( d['name'] + ':' , 'Heading 3' )
                        for i in d['intro']:
                            p.insert_paragraph_before( i , 'Heading 4' )
                # 公司简介
                if str(r.font.color.rgb) == '0000FF':
                    p.clear()
                    for intro in user.introduction:
                        p.insert_paragraph_before( intro , 'Quote' )
                # 插入图片
                if str(r.font.color.rgb) == '000FFF':
                    pp = p.insert_paragraph_before()
                    pp.add_run().add_picture( user.picPath ,Cm(16))
                    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                todo.append(r)
    
    #替换
    for r in todo:
        r.font.highlight_color = None
        if str(r.font.color.rgb) == 'FFF000':
            r.text = user.fileName
        elif str(r.font.color.rgb) == 'FF0000':
            r.text = user.company
        elif str(r.font.color.rgb) == '00FF00':
            r.text = user.address
        elif str(r.font.color.rgb) == 'FFFF00':
            r.text = '\n'.join(user.coverField)
        elif str(r.font.color.rgb) == '00FFFF':
            r.text = user.manager
        elif str(r.font.color.rgb) == '7F0000':
            r.text = user.guandai
        elif str(r.font.color.rgb) == '007F00':
            r.text = user.employees
        elif str(r.font.color.rgb) == '000080':
            r.text = user.approver
        elif str(r.font.color.rgb) == '7F7F00':
            r.text = user.releaseDate
        elif str(r.font.color.rgb) == '007F7F':
            r.text = user.auditDate
        elif str(r.font.color.rgb) == '7F007F':
            r.text = user.zip
        elif str(r.font.color.rgb) == 'FFFFF0':
            r.text = user.phone
        elif str(r.font.color.rgb) == '0FFFFF':
            r.text = user.policy
        elif str(r.font.color.rgb) == '000FFF':
            pass
        else:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    document.save(dst)
    
    print('成功生成 '+dst )
    pass

if __name__ == '__main__':

    user = userInfo();
    with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
    for dict in data:
        for key in dict.keys():
            setattr( user , key , dict[key] )
        replace('sample.docx',user.fileName+'-20000-SM-M-01.docx' , user )