from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json, time, lxml, threading

class Replace:
    lock = threading.RLock()

    def __init__(self):
        pass

    def __del__(self):
        pass

    def replaceRules(self, r):
        #替换规则
        r.font.highlight_color = None
        if str(r.font.color.rgb) == 'FFF000':
            r.text = self.user.fileName
        elif str(r.font.color.rgb) == 'FF0000':
            r.text = self.user.company
        elif str(r.font.color.rgb) == '00FF00':
            r.text = self.user.address
        elif str(r.font.color.rgb) == 'FFFF00':
            r.text = self.user.coverField
        elif str(r.font.color.rgb) == '00FFFF':
            r.text = self.user.manager
        elif str(r.font.color.rgb) == '7F0000':
            r.text = self.user.guandai
        elif str(r.font.color.rgb) == '007F00':
            r.text = self.user.compiler
        elif str(r.font.color.rgb) == '000080':
            r.text = self.user.approver
        elif str(r.font.color.rgb) == '7F7F00':
            r.text = self.user.releaseDate
        elif str(r.font.color.rgb) == '007F7F':
            r.text = self.user.auditDate
        elif str(r.font.color.rgb) == '7F007F':
            r.text = self.user.zip
        elif str(r.font.color.rgb) == 'FFFFF0':
            r.text = self.user.phone
        elif str(r.font.color.rgb) == '0FFFFF':
            r.text = self.user.policy
        elif str(r.font.color.rgb) == '000FFF':
            pass
        elif str(r.font.color.rgb) == 'FFF0FF':
            r.text = self.user.audit
        elif str(r.font.color.rgb) == 'FF0FFF':
            r.text = self.user.announcer
        elif str(r.font.color.rgb) == 'F0FFFF':
            r.text = self.user.modifyDate.pop(0)
            
        else:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    def findAndReplaceFootAndHead(self):
        #页眉页脚
        self.lock.acquire()
        for s in self.document.sections:
            for p in s.footer.paragraphs:
                for r in p.runs:
                    if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                        r.text = self.user.company
                        r.font.highlight_color = None
                        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            for p in s.header.paragraphs:
                for r in p.runs:
                    if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                        r.text = self.user.fileName
                        r.font.highlight_color = None
                        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        self.lock.release()

    def findAndReplaceTables(self):
        #表格
        for t in self.document.tables:
            for c in t.columns:
                for cc in c.cells:
                    for p in cc.paragraphs:
                        for r in p.runs:
                            if r.font.highlight_color == WD_COLOR_INDEX.YELLOW :
                                #todo.append(r)
                                self.lock.acquire()
                                self.replaceRules(r)
                                self.lock.release()

    def findAndReplaceParagraphs(self):
        #正文
        for p in self.document.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    # 部门介绍
                    if str(r.font.color.rgb) == 'FF00FF':
                        p.clear()
                        for d in self.user.departments:
                            p.insert_paragraph_before( d['name'] + ':' , '样式1' )
                            for i in d['intro']:
                                p.insert_paragraph_before( i , 'No Spacing' )
                    # 公司简介
                    if str(r.font.color.rgb) == '0000FF':
                        p.clear()
                        for intro in self.user.introduction:
                            p.insert_paragraph_before( intro , 'Quote' )
                    # 插入图片
                    if str(r.font.color.rgb) == '000FFF':
                        pp = p.insert_paragraph_before()
                        #检查宽高
                        levelDict = {}
                        for dep in self.user.departments:
                            if not levelDict.__contains__(dep['level']):
                                levelDict[dep['level']] = 1
                            else:
                                levelDict[dep['level']] = levelDict[dep['level']] + 1
                        height = len( levelDict )
                        width = max(levelDict.values())
                        pp.add_run().add_picture( self.user.picPath ,height=Cm(10)) if width < 2*height else pp.add_run().add_picture( self.user.picPath ,width=Cm(16))
                        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    #todo.append(r)
                    self.lock.acquire()
                    self.replaceRules(r)
                    self.lock.release()

    def run(self, src , dst , user):
        self.document = Document(src)
        self.user = user
        #todo = []

        #更新目录
        element_updatefields = lxml.etree.SubElement(
            self.document.settings.element, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"+"updateFields"
        )
        element_updatefields.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"+"val", "true")

        threadList = []
        threadList.append(threading.Thread(target=self.findAndReplaceFootAndHead))
        threadList.append(threading.Thread(target=self.findAndReplaceTables))
        threadList.append(threading.Thread(target=self.findAndReplaceParagraphs))

        for t in threadList:
            t.start()
        for t in threadList:
            t.join()

        #服务管理职责分配表
        table = self.document.tables[-1]
        table_row_len = len(table.rows)
        #s = time.time()
        for d in self.user.departments:
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
            # 优化替换速度，用set取代list，平均速度提高可达10%
            funcSet = set(d["func"])
            for i in range(1, table_row_len):
                cell = column.cells[i]
                if i in funcSet:
                    cell.text = "▲"
                else:
                    cell.text = "△"
                cell.paragraphs[0].style = "Intense Quote"
        #e = time.time()
        #print(e-s)
        table.style = 'Table Theme'
        table.autofit = True

        print('成功生成 '+dst )
        return self.document
