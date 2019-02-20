from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt5.QtCore import QDate
from dataStruct import userInfo
from generateGraph import drawGraph
from Word_Printer import docWriter
from database import DB

class Controller(QMainWindow, Ui_MainWindow):
    user = userInfo()
    db = DB()
    
    graphStyle = [{ 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'black',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#008000',
                    },
                    'lineLen' : 3},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'black',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#800000',
                    },
                    'lineLen' : 3},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'black',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#000080',
                    },
                    'lineLen' : 3},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'black',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#ffff00',
                    },
                    'lineLen' : 3}]

    def __init__(self):
        #init
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #userInit
        self.user.departments = []

        #connect
        self.connectButton()
        self.connectText()
        self.connectList()
        #self.setUser()
      
    def setGraphColor(self, tar, pos, option): 
        col = QColorDialog.getColor() 
        if col.isValid(): 
            tar.setStyleSheet('QWidget {background-color:%s}' % col.name())
            self.graphStyle[pos]["nodes"][option] = col.name()

    def setLineWidth(self, tar, pos):
        self.graphStyle[pos]["lineLen"] = tar.value()

    def showPreviewGraph(self):
        graph = drawGraph()
        graph.draw("preview", self.user, self.graphStyle)

    def search(self):
        searchContent = self.searchContent.text()
        user = self.db.searchById(searchContent)
        if user.company != "":
            self.setInput(user)
        self.searchContent.setText("")

    def setInput(self, user):
        #clear
        c = self.departmentList.count()
        for i in range(c):
            self.departmentList.takeItem(0)
        c = self.previewPic.count()
        for i in range(c):
            self.previewPic.takeItem(0)

        #
        self.fileNameText.setText(user.fileName)
        self.companyText.setText(user.company)
        self.addressText.setText(user.address)
        self.coverFieldText.setText(user.coverField)
        self.managerText.setText(user.manager)
        self.guandaiText.setText(user.guandai)
        self.employeesText.setText(user.employees)
        self.approverText.setText(user.approver)
        self.auditText.setText(user.audit)
        self.announcerText.setText(user.announcer)
        self.zipText.setText(user.zip)
        self.phoneText.setText(user.phone)
        self.policyText.setText(user.policy)
        #
        date = user.releaseDate.replace("年", "-").replace("月", "-").replace("日", "")
        date_t = date.split("-")
        self.releaseDateText.setDate(QDate(int(date_t[0]), int(date_t[1]), int(date_t[2])))
        date = user.auditDate.replace("年", "-").replace("月", "-").replace("日", "")
        date_t = date.split("-")
        self.auditDateText.setDate(QDate(int(date_t[0]), int(date_t[1]), int(date_t[2])))
        #
        self.introductionText.setPlainText("\n".join(user.introduction))

        self.user.departments = []
        for dep in user.departments:
            self.departmentList.addItem(dep["name"])
            self.user.departments.append(dep)
        self.setDepStruct()
        #清空第二页右
        self.depName.setText("")
        self.depLevel.setValue(1)
        self.depIntro.setPlainText("")
        for i in range(1,43):
            getattr(self,'duty_'+str(i)).setCheckState(0)


    def connectText(self):
        self.fileNameText.textChanged.connect(lambda : self.setUser())
        self.companyText.textChanged.connect(lambda : self.setUser())
        self.addressText.textChanged.connect(lambda : self.setUser())
        self.coverFieldText.textChanged.connect(lambda : self.setUser())
        self.managerText.textChanged.connect(lambda : self.setUser())
        self.guandaiText.textChanged.connect(lambda : self.setUser())
        self.employeesText.textChanged.connect(lambda : self.setUser())
        self.approverText.textChanged.connect(lambda : self.setUser())
        self.auditText.textChanged.connect(lambda : self.setUser())
        self.announcerText.textChanged.connect(lambda : self.setUser())
        self.zipText.textChanged.connect(lambda : self.setUser())
        self.phoneText.textChanged.connect(lambda : self.setUser())
        self.policyText.textChanged.connect(lambda : self.setUser())
        self.introductionText.textChanged.connect(lambda : self.setUser())
        #self.fileNameText.textChanged.connect( lambda : self.setUser() )

        self.releaseDateText.dateChanged.connect( lambda : self.setUser() )
        self.auditDateText.dateChanged.connect( lambda : self.setUser() )

        # style
        self.level1Width.valueChanged.connect(lambda: self.setLineWidth(self.level1Width, 0))
        self.level2Width.valueChanged.connect(lambda: self.setLineWidth(self.level2Width, 1))
        self.level3Width.valueChanged.connect(lambda: self.setLineWidth(self.level3Width, 2))
        self.level4Width.valueChanged.connect(lambda: self.setLineWidth(self.level4Width, 3))

    def connectButton(self):

        #deStructBorderColor
        self.level1Border.clicked.connect(lambda: self.setGraphColor(self.level1Border, 0, "fillcolor"))
        self.level2Border.clicked.connect(lambda: self.setGraphColor(self.level2Border, 1, "fillcolor"))
        self.level3Border.clicked.connect(lambda: self.setGraphColor(self.level3Border, 2, "fillcolor"))
        self.level4Border.clicked.connect(lambda: self.setGraphColor(self.level4Border, 3, "fillcolor"))

        #deStructFontColor
        self.level1Font.clicked.connect(lambda: self.setGraphColor(self.level1Font, 0, "fontcolor"))
        self.level2Font.clicked.connect(lambda: self.setGraphColor(self.level2Font, 1, "fontcolor"))
        self.level3Font.clicked.connect(lambda: self.setGraphColor(self.level3Font, 2, "fontcolor"))
        self.level4Font.clicked.connect(lambda: self.setGraphColor(self.level4Font, 3, "fontcolor"))

        #previewButton
        self.previewButton.clicked.connect(lambda: self.showPreviewGraph())

        #generateDoc
        self.createBotton.clicked.connect(lambda: self.generateDoc())
        self.cancelButton.clicked.connect(lambda: self.discard() )

        #search
        self.searchButton.clicked.connect(lambda: self.search())

    def connectList(self):
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))#可能没选中，故用getattr确认
        # button
        self.AddDep.clicked.connect( lambda: self.addDepartment() )
        self.DeleteDep.clicked.connect( lambda: self.removeDepartment( getattr( self.departmentList.currentItem(),'text',str)() ) )#可能没选中，故用getattr确认
        self.cancelDep.clicked.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))
        self.addOrModifyDep.clicked.connect( lambda: self.setDepartments(getattr( self.departmentList.currentItem(),'text',str)() ) )

    def setUser(self):
        #
        self.user.fileName = self.fileNameText.text()
        self.user.company = self.companyText.text()
        self.user.address = self.addressText.text()
        self.user.coverField = self.coverFieldText.text()
        self.user.manager = self.managerText.text()
        self.user.guandai = self.guandaiText.text()
        self.user.employees = self.employeesText.text()
        self.user.approver = self.approverText.text()
        self.user.audit = self.auditText.text()
        self.user.announcer = self.announcerText.text()
        self.user.zip = self.zipText.text()
        self.user.phone = self.phoneText.text()
        self.user.policy = self.policyText.text()
        #
        self.user.releaseDate=self.releaseDateText.date().toString("yyyy年MM月dd日")
        self.user.auditDate=self.auditDateText.date().toString("yyyy年MM月dd日")
        #
        self.user.introduction = str(self.introductionText.toPlainText()).split('\n')

    def setDepartments(self,departmentName):
        if departmentName == "":
            pass
        else:
            department = self.user.departments[ self.departmentList.row( self.departmentList.currentItem() ) ]
            self.departmentList.currentItem().setText(self.depName.text())
            department['name'] = self.depName.text()
            department['level'] = self.depLevel.value()
            department['intro'] = str(self.depIntro.toPlainText()).split('\n')
            department['func'] = []
            for i in range(1,43):
                if getattr(self,'duty_'+str(i)).checkState():
                    department['func'].append(i)
        self.setDepStruct()
    
    def refreshGraph(self, keys, levelDict):
        c = self.previewPic.count()
        for i in range(self.previewPic.count()):
            self.previewPic.takeItem(0)
        for key in keys:
            deps = levelDict[key].split(",")
            for dep in deps:
                self.previewPic.addItem("级别：" + str(key) + " | 部门： " + dep)

    def setDepStruct(self):
        if not self.user.departments or len(self.user.departments) == 0:
            self.user.depStruct = ""
            self.refreshGraph([], {})
        else:
            levelDict = {}
            try:
                for dep in self.user.departments:
                    if not dep.__contains__('level'):
                        continue
                    elif not levelDict.__contains__(dep['level']):
                        levelDict[dep['level']] = dep['name']
                    else:
                        levelDict[dep['level']] = levelDict[dep['level']] + "," + dep['name']
            except Exception as e:
                print("Error:",e)
                self.user.depStruct = ""
            else:
                keys = list(levelDict.keys())
                keys.sort()
                gramma = [levelDict[key] for key in keys]
                self.user.depStruct = ";\n".join(gramma)
                self.user.depStruct = self.user.depStruct + ";"
                self.refreshGraph(keys, levelDict)

    def addDepartment(self,departmentName="部门名称"):
        self.departmentList.addItem(departmentName)
        self.user.departments.append({"name":departmentName})
        c = self.departmentList.count()
        self.departmentList.setCurrentItem(self.departmentList.item(c-1))
        '''
        self.user.departments.append({"name":departmentName,"level":1,"intro":[
          "负责公司的整体软件开发核心技术，组织制定和实施重大技术决策和技术方案；",
          "指导、审核、制定、开发软件项目，对各项结果做最终质量评估、归档；",
          "设计、开发、维护、管理软件项目及软件产品。",
          "完善部门发展规划，组织审定部门各项技术标准，编制完善软件开发流程；",
          "完善与其他部门的沟通与协作；",
          "协助参与公司项目的招投标软件接口等资料的编写和策划；",
          "制定技术方案，根据项目类型提成准确的需求，制定项目进度计划表，负责验收工作；",
          "填写测试报告，编写相关操作手册文档；",
          "关注最新技术动态，组织内部技术交流与技术传递。",
          "负责公司内外部软件开发项目的需求调查、方案制定、软件编程、成果申报等组织实施工作;",
          "负责对自行开发、合作开发以及外购软件的安装、测试、培训、系统维护和售后服务等工作。",
          "负责与开发部配合根据需求说明书制订《项目测试方案》，编写《测试用例》，建立测试环境；",
          "负责软件产品开发过程和投入运营之前的新增软件和修改升级软件的模块测试和系统测试；",
          "负责软件问题解决过程跟踪记录。",
          "负责对软件行业信息的收集、整理、研究及利用;",
          "负责自主开发软件产品的销售及售前技术支持;",
          "负责推广实施软件开发文档规范化工作，管理研发产品相关文档。"
        ],"func":[1,5,42]})
        '''

    def showDepartmentDetail(self,departmentName):
        if departmentName == "":
            self.depName.setText( "" )
            self.depIntro.setPlainText( "" )
            self.depLevel.setValue( 0 )
            for i in range(1,43):
                getattr(self,'duty_'+str(i)).setCheckState(0)
        else:
            department = self.user.departments[ self.departmentList.row( self.departmentList.currentItem() ) ]
            self.depName.setText( departmentName )
            self.depIntro.setPlainText( '\n'.join(department['intro']) if 'intro' in department else "" )
            self.depLevel.setValue( department['level'] if 'level' in department else 1 )
            for i in range(1,43): #clear all
                getattr(self,'duty_'+str(i)).setCheckState(0)
            for i in ( department['func'] if 'func' in department else [] ):
                getattr(self,'duty_'+str(i)).setCheckState(2)


    
    def removeDepartment(self,departmentName):
        if( departmentName == "" ):
            return
        ####请勿修改顺序，takeItem在移除item前会触发itemChanged，若已删除user则导致越界错误
        index =  self.departmentList.row( self.departmentList.currentItem() )
        self.departmentList.takeItem( index )
        del self.user.departments[ index ]
        ########
        self.setDepStruct()

    def generateDoc(self):
        docWrt = docWriter()
        print("正在更新数据库...")
        self.db.delete("info", self.user.company)
        self.db.insertData(self.user)
        print("更新数据库成功")
        print("正在生成文档...")
        docWrt.loadAndWrite(self.user, "sample.docx", self.graphStyle)
        self.depIntro.setPlainText(str(vars(self.user)))

    def discard(self):
        #第一页左
        self.fileNameText.setText("")
        self.companyText.setText("")
        self.addressText.setText("")
        self.coverFieldText.setText("")
        self.policyText.setText("")
        self.introductionText.setPlainText("")
        #第一页右
        self.managerText.setText("")
        self.guandaiText.setText("")
        self.employeesText.setText("")
        self.approverText.setText("")
        self.auditText.setText("")
        self.announcerText.setText("")
        self.zipText.setText("")
        self.phoneText.setText("")
        #日期
        pass
        #部门结构
        self.user.departments = []
        #
        c = self.departmentList.count()
        for i in range(c):
            self.departmentList.takeItem(0)
        c = self.previewPic.count()
        for i in range(c):
            self.previewPic.takeItem(0)
        #第二页右
        self.depName.setText("")
        self.depLevel.setValue(1)
        self.depIntro.setPlainText("")
        for i in range(1,43):
            getattr(self,'duty_'+str(i)).setCheckState(0)