from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json, time, lxml, threading
import re, os
from getTime import getTime

class Replace:
    lock = threading.RLock()

    def __init__(self):
        self.timeCount = 0

    def __del__(self):
        pass

    def replaceRules(self, r):
        #替换规则
        r.font.highlight_color = None
        if str(r.font.color.rgb) == 'FF0000':
            r.text = self.user.fileName
        elif str(r.font.color.rgb) == 'FE0000':
            r.text = self.user.company
        elif str(r.font.color.rgb) == 'FD0000':
            pass#简介
        elif str(r.font.color.rgb) == 'FC0000':
            r.text = self.user.address
        elif str(r.font.color.rgb) == 'FB0000':
            r.text = self.user.coverField
        elif str(r.font.color.rgb) == 'FA0000':
            r.text = self.user.manager
        elif str(r.font.color.rgb) == 'F90000':
            r.text = self.user.guandai
        elif str(r.font.color.rgb) == 'F80000':
            r.text = self.user.compiler
        elif str(r.font.color.rgb) == 'F70000':
            r.text = self.user.approver
        elif str(r.font.color.rgb) == 'F60000':
            r.text = self.user.releaseDate
        elif str(r.font.color.rgb) == 'F50000':
            r.text = self.user.modifyDate[ self.timeCount%5 ]
            self.timeCount+=1
        elif str(r.font.color.rgb) >= 'F50001' and str(r.font.color.rgb) <= 'F50005':
            r.text = self.user.modifyDate[ r.font.color.rgb[2]-1 ]
        elif str(r.font.color.rgb) == 'F40000':
            r.text = self.user.zip
        elif str(r.font.color.rgb) == 'F30000':
            r.text = self.user.phone
        elif str(r.font.color.rgb) == 'F20000':
            r.text = self.user.policy
        elif str(r.font.color.rgb) == 'F10000':
            r.text = self.user.audit
        elif str(r.font.color.rgb) == 'F00000':
            r.text = self.user.announcer
        elif str(r.font.color.rgb) == 'EF0000':
            pass#logo
        elif str(r.font.color.rgb) == 'ED0000':
            pass#pic
        elif str(r.font.color.rgb) == 'EC0000':
            r.text = self.user.corporateRepresentative
        elif str(r.font.color.rgb) == 'EB0000':
            r.text = self.user.organization.Audit.auditLeader
        elif str(r.font.color.rgb) == 'EA0000':
            r.text = self.user.organization.Audit.audit1
        elif str(r.font.color.rgb) == 'E90000':
            r.text = self.user.organization.Audit.audit2
        elif str(r.font.color.rgb) == 'E80000':
            r.text = self.user.organization.Audit.audit3
        elif str(r.font.color.rgb) == 'E70000':
            r.text = self.user.organization.Audit.planDate
        elif str(r.font.color.rgb) == 'E60000':
            r.text = self.user.organization.Audit.auditDate
        elif str(r.font.color.rgb) == 'E50000':
            r.text = self.user.organization.Audit.scheduleDate
        elif str(r.font.color.rgb) == 'E40000':
            r.text = self.user.organization.Audit.compiler
        elif str(r.font.color.rgb) == 'E30000':
            r.text = self.user.organization.Audit.compileDate
        elif str(r.font.color.rgb) == 'E20000':
            r.text = self.user.organization.Audit.audit
        elif str(r.font.color.rgb) == 'E10000':
            r.text = self.user.organization.Audit.approveDate
        elif str(r.font.color.rgb) == 'E00000':
            r.text = self.user.organization.Audit.reviewDate
        elif str(r.font.color.rgb) == 'DF0000':
            r.text = self.user.organization.Audit.excuteDate
        elif str(r.font.color.rgb) == 'DE0000':
            r.text = self.user.organization.Audit.reportDate
        elif str(r.font.color.rgb) == 'DD0000':
            r.text = self.user.organization.Record.fileName
        elif str(r.font.color.rgb) == 'DC0000':
            r.text = '\n'.join(self.user.organization.Record.auditContent)
        elif str(r.font.color.rgb) == 'DB0000':
            r.text = '\n'.join(self.user.organization.Record.auditProcess)
        elif str(r.font.color.rgb) == 'DA0000':
            r.text = self.user.organization.Record.audit
        elif str(r.font.color.rgb) == 'D90000':
            r.text = self.user.organization.Record.auditDate
        elif str(r.font.color.rgb) == 'D80000':
            r.text = self.user.organization.Record.approver
        elif str(r.font.color.rgb) == 'D70000':
            r.text = self.user.organization.Record.approveDate
        elif str(r.font.color.rgb) == 'D60000':
            r.text = self.user.organization.Record.provider
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

    def replaceDepartmentTable(self):
        #服务管理职责分配表
        table = self.document.tables[-1]
        table_row_len = len(table.rows)
        #s = time.time()
        for d in self.user.departments:
            #特殊情况
            if d["name"] == "管理者代表":
                continue
            # 表头
            column = table.add_column( Cm(3) )
            cell = column.cells[0]
            #特别情况
            if d["name"] == "总经理":
                cell.text = "管理层"
            else:
                cell.text = d["name"]
            cell.paragraphs[0].style = "表格标记"
            # 内容
            # 优化替换速度，用set取代list，平均速度提高可达10%
            funcSet = set(d["func"])
            for i in range(1, table_row_len):
                cell = column.cells[i]
                if i in funcSet:
                    cell.text = "▲"
                else:
                    cell.text = "△"
                cell.paragraphs[0].style = "表格标记"
        table.style = 'Table Theme'
        table.autofit = True

    def findAndReplaceParagraphs(self):
        #正文
        for p in self.document.paragraphs:
            for r in p.runs:
                if r.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    # 部门介绍
                    if str(r.font.color.rgb) == 'EE0000':
                        p.clear()
                        for d in self.user.departments:
                            p.insert_paragraph_before( d['name'] + ':' , '部门名称' )
                            for i in d['intro']:
                                p.insert_paragraph_before( i , '部门职责' )
                    # 公司简介
                    if str(r.font.color.rgb) == 'FD0000':
                        p.clear()
                        for intro in self.user.introduction:
                            p.insert_paragraph_before( intro , '简介' )
                    # 插入图片
                    if str(r.font.color.rgb) == 'ED0000':
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

                    # 插入logo
                    if str(r.font.color.rgb) == 'EF0000':
                        #insert logo
                        if(self.user.logoPath != '' and os.path.exists(self.user.logoPath)):
                            pp = p.insert_paragraph_before()
                            pp.add_run().add_picture( self.user.logoPath , height=Cm(4.5) )
                            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        #clear text
                        p.clear()

                    #todo.append(r)
                    self.lock.acquire()
                    self.replaceRules(r)
                    self.lock.release()

    def run(self, src , dst , user):
        self.document = Document(src)
        user = getTime(user)
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

        if re.search( "(.*)-SM-(.*)" , src ):
            self.replaceDepartmentTable()

        for t in threadList:
            t.start()
        for t in threadList:
            t.join()

        #e = time.time()
        #print(e-s)

        print('成功生成 '+dst )
        return self.document
