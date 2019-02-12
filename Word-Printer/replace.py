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
    user.fileName = 'SAMP'
    user.company = '很有钱有限公司'
    user.address = '广州市某区某街道某楼某层某号'
    user.introduction = ['这里是简介','最多只有800字','简介简介简介简介简介简介简介简介简介简介']
    user.coverField = ['这里是管理经营范围','最多不知道多少字','也不知道能不能换行','经营范围经营范围经营范围经营范围']
    user.manager = '经理名字某某某'
    user.guandai = '管代名字某某某'
    user.employees = '编制人员姓名某某人'
    user.approver = '批准发布人某某人'
    user.releaseDate = '8102年1月31日'
    user.auditDate = '9102年2月28日'
    user.picPath = 'Graph.gv.png'
    user.departments = [{'name':'很有钱的软件开发部','intro':['开','发','软','件']},{'name':'很有钱的客服','intro':['聊','天','系统集成中心是公司的直接创利部门之一，进行系统集成方面的业务开拓，实现公司要求的年度经营目标；']}]

    replace('sample.docx',user.fileName+'-20000-SM-M-01.docx' , user )