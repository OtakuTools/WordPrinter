from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from dataStruct import userInfo
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import time
import lxml
from getTime import getTime

def replace( src , dst , user ):
    document = Document(src)
    todo = []

    #更新目录
    element_updatefields = lxml.etree.SubElement(
        document.settings.element, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"+"updateFields"
    )
    element_updatefields.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"+"val", "true")

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
                        p.insert_paragraph_before( d['name'] + ':' , '样式1' )
                        for i in d['intro']:
                            p.insert_paragraph_before( i , 'No Spacing' )
                # 公司简介
                if str(r.font.color.rgb) == '0000FF':
                    p.clear()
                    for intro in user.introduction:
                        p.insert_paragraph_before( intro , 'Quote' )
                # 插入图片
                if str(r.font.color.rgb) == '000FFF':
                    pp = p.insert_paragraph_before()
                    #检查宽高
                    levelDict = {}
                    for dep in user.departments:
                        if not levelDict.__contains__(dep['level']):
                            levelDict[dep['level']] = 1
                        else:
                            levelDict[dep['level']] = levelDict[dep['level']] + 1
                    height = len( levelDict )
                    width = max(levelDict.values())
                    pp.add_run().add_picture( user.picPath ,height=Cm(10)) if width < 2*height else pp.add_run().add_picture( user.picPath ,width=Cm(16))
                    #picture = pp.add_run().add_picture( user.picPath ,height=Cm(10))
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
            r.text = user.coverField
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
        elif str(r.font.color.rgb) == 'FFF0FF':
            r.text = user.audit
        elif str(r.font.color.rgb) == 'FF0FFF':
            r.text = user.announcer
        elif str(r.font.color.rgb) == 'F0FFFF':
            r.text = user.modifyDate.pop(0)
            
        else:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    #服务管理职责分配表
    table = document.tables[-1]
    table_row_len = len(table.rows)
    for d in user.departments:
        #特殊情况
        if d["name"] == "管理者代表":
            continue
        # 表头
        column = table.add_column( Cm(1.5) )
        cell = column.cells[0]
        #特别情况
        if d["name"] == "总经理":
            cell.text = "管理层"
        else:
            cell.text = d["name"]
        cell.paragraphs[0].style = "Intense Quote"
        # 内容
        for i in range(1, table_row_len):
            cell = column.cells[i]
            if i in d["func"]:
                cell.text = "▲"
            else:
                cell.text = "△"
            cell.paragraphs[0].style = "Intense Quote"
    table.style = 'Table Theme'
    table.autofit = True
    
    #print("create table cost:", time_end-time_start)

    print('成功生成 '+dst )
    return document
