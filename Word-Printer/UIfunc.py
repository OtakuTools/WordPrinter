from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from dataStruct import userInfo

class Controller(QMainWindow, Ui_MainWindow):
    user = userInfo()
    
    graphStyle = [{ 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'white',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#ffff00',
                    },
                    'lineLen' : 4},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'white',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#00ff00',
                    },
                    'lineLen' : 6},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'white',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#00ff00',
                    },
                    'lineLen' : 3},
                  { 'nodes': {
                        'fontname': 'KaiTi',
                        'shape': 'box',
                        'fontcolor': 'white',
                        'color': 'white',
                        'style': 'filled',
                        'fillcolor': '#00ff00',
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
      
    def showDialog(self, tar): 
        col = QColorDialog.getColor() 
        print(col.name(),"\n")
        if col.isValid(): 
            tar.setStyleSheet('QWidget {background-color:%s}' % col.name())

    def getInfo():
        return user

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
        #self.fileNameText.textChanged.connect( lambda : self.setUser() )

        self.releaseDateText.dateChanged.connect( lambda : self.setUser() )
        self.auditDateText.dateChanged.connect( lambda : self.setUser() )

    def connectButton(self):

        #deStructBorderColor
        self.level1Border.clicked.connect(lambda: self.showDialog(self.level1Border))
        self.level2Border.clicked.connect(lambda: self.showDialog(self.level2Border))
        self.level3Border.clicked.connect(lambda: self.showDialog(self.level3Border))
        self.level4Border.clicked.connect(lambda: self.showDialog(self.level4Border))

        #deStructFontColor
        self.level1Font.clicked.connect(lambda: self.showDialog(self.level1Font))
        self.level2Font.clicked.connect(lambda: self.showDialog(self.level2Font))
        self.level3Font.clicked.connect(lambda: self.showDialog(self.level3Font))
        self.level4Font.clicked.connect(lambda: self.showDialog(self.level4Font))

        #preview
        self.createBotton.clicked.connect(lambda: self.depIntro.setPlainText(str(vars(self.user))))

    def connectList(self):
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))#可能没选中，故用getattr确认
        # button
        self.AddDep.clicked.connect( lambda: self.addDepartment() )
        self.DeleteDep.clicked.connect( lambda: self.removeDepartment(getattr( self.departmentList.currentItem(),'text',str)() ) )#可能没选中，故用getattr确认
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
            for department in self.user.departments:
                if department['name'] == departmentName:
                    self.departmentList.currentItem().setText(self.depName.text())
                    department['name'] = self.depName.text()
                    department['level'] = self.depLevel.value()
                    department['intro'] = str(self.depIntro.toPlainText()).split('\n')
                    department['func'] = []
                    for i in range(1,43):
                        if getattr(self,'duty_'+str(i)).checkState():
                            department['func'].append(i)
                    break#可能有bug在这里诞生
        self.setDepStruct()

    def setDepStruct(self):
        if not self.user.departments or len(self.user.departments) == 0:
            self.user.depStruct = ""
        else:
            levelDict = {}
            try:
                print(len(self.user.departments))
                for dep in self.user.departments:
                    if not levelDict.__contains__(dep['level']):
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

    def addDepartment(self,departmentName="部门名称"):
        self.departmentList.addItem(departmentName)
        self.user.departments.append({"name":departmentName})
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
            for department in self.user.departments:
                if department['name'] == departmentName:
                    self.depName.setText( departmentName )
                    self.depIntro.setPlainText( '\n'.join(department['intro']) if 'intro' in department else "" )
                    self.depLevel.setValue( department['level'] if 'level' in department else 1 )
                    for i in range(1,43): #clear all
                        getattr(self,'duty_'+str(i)).setCheckState(0)
                    for i in ( department['func'] if 'func' in department else [] ):
                        getattr(self,'duty_'+str(i)).setCheckState(2)
                    break #可能有bug在这里诞生
    
    def removeDepartment(self,departmentName):
        print( "dep:"+departmentName )
        print( len(self.user.departments) )
        for department in self.user.departments:
            if department['name'] == departmentName:
                self.user.departments.remove(department)
                break #可能有bug在这里诞生
        self.departmentList.takeItem( self.departmentList.row(self.departmentList.selectedItems()[0] if len( self.departmentList.selectedItems() ) else None ) )
