from test import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from databaseSetting import Ui_databaseSetting
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QColorDialog, QMessageBox, QCompleter, QProgressDialog 
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

from dataStruct import userInfo
from generateGraph import drawGraph
from database import DB, DBSettingController
from messageDialog import MessageDialog
from pathSelection import pathSelection
from WriteDocController import WriteDocController, WrtDocThread

class Controller(QMainWindow, Ui_MainWindow):

    sampleDir = "./samples/"
    
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
        Ui_GenerateDocConfirm.__init__(self)
        Ui_databaseSetting.__init__(self)
        self.setupUi(self)

        #connect
        self.initToolBar()
        self.connectButton()
        self.connectText()
        self.connectList()
        
        #message dialog
        self.msgDialog = MessageDialog()

        #sample dir
        self.init_Samples()

    def init_DB_user(self):
        #database
        self.db = DB()
        if not self.db.checkConnection():
            self.msgDialog.showErrorDialog("初始化数据库出错","数据库无法连接，请检查相应配置！\n异常信息为：" + self.db.dbException + "\n您做的任何变动将无法存入数据库!" )

        # search content completer
        self.getCompanyInfo()

        #userInit
        self.user = userInfo()
        self.user.resetDepartment()
        self.refreshDepartmentList()
        if self.user.color == "":
            self.user.color = json.dumps(self.graphStyle)

    def init_Samples(self):
        self.pathSelection = pathSelection()
        self.pathSelection.autoRefresh()

    def initToolBar(self):
        tool = self.addToolBar("设置")
        edit = QAction(QIcon(""),"数据库配置",self)
        tool.addAction(edit) 
        tool.actionTriggered.connect(self.toolBtnPressed)

    def connectText(self):
        self.fileNameText.textChanged.connect(lambda : self.setUser())
        self.companyText.textChanged.connect(lambda : self.setUser())
        self.addressText.textChanged.connect(lambda : self.setUser())
        self.coverFieldText.textChanged.connect(lambda : self.setUser())
        self.managerText.textChanged.connect(lambda : self.setUser())
        self.guandaiText.textChanged.connect(lambda : self.setUser())
        self.compilerText.textChanged.connect(lambda : self.setUser())
        self.approverText.textChanged.connect(lambda : self.setUser())
        self.auditText.textChanged.connect(lambda : self.setUser())
        self.announcerText.textChanged.connect(lambda : self.setUser())
        self.zipText.textChanged.connect(lambda : self.setUser())
        self.phoneText.textChanged.connect(lambda : self.setUser())
        self.policyText.textChanged.connect(lambda : self.setUser())
        self.introductionText.textChanged.connect(lambda : self.setUser())

        self.releaseDateText.dateChanged.connect( lambda : self.setUser() )
        self.auditDateText.dateChanged.connect( lambda : self.setUser() )
        # logo
        self.Logo.textChanged.connect(lambda : self.showLogo())

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

        #DateChoose
        self.auditDateText.setCalendarPopup(True)
        self.releaseDateText.setCalendarPopup(True)
        
        #LogoChoose
        self.logoChooseButton.clicked.connect(lambda: self.chooseLogo())

        #previewButton
        self.previewButton.clicked.connect(lambda: self.showPreviewGraph())

        #generateDoc
        self.createBotton.clicked.connect(lambda: self.generateDoc())
        self.cancelButton.clicked.connect(lambda: self.discard() )
        self.saveButton.clicked.connect(lambda: self.saveInfoButNotGen())

        #search
        self.searchButton.clicked.connect(lambda: self.search())


    def connectList(self):
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))#可能没选中，故用getattr确认
        # button
        self.AddDep.clicked.connect( lambda: self.addDepartment() )
        self.DeleteDep.clicked.connect( lambda: self.removeDepartment( getattr( self.departmentList.currentItem(),'text',str)() ) )#可能没选中，故用getattr确认
        self.cancelDep.clicked.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))
        self.addOrModifyDep.clicked.connect( lambda: self.setDepartments(getattr( self.departmentList.currentItem(),'text',str)() ) )

    def chooseLogo(self):
        fileName1, filetype = QFileDialog().getOpenFileName(self, "选取图标",".//","Images(*.png *.jpg *.jpeg *.bmp)")
        self.Logo.setPlainText(fileName1)

    def showLogo(self):
        logoPath = self.Logo.toPlainText()
        reg = "(file:///)?(.*)"
        path = re.search(reg, logoPath, re.M|re.I).group(2)
        image = QImage()
        print(path)
        if path and path != "" and image.load(path):
            filepath, filename = os.path.split(path)
            if not os.path.exists("./logoData"):
                os.makedirs("./logoData")
            shutil.copy(path, "./logoData/%s" %(filename))
            image = image.scaledToHeight(self.logoView.height())
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap.fromImage(image))
            self.logoView.setScene(scene)
            self.logoView.show()
    
    def toolBtnPressed(self, qaction):
        if qaction.text() == "数据库配置":
            self.resetDB()
            if not self.db.checkConnection():
                self.msgDialog.showErrorDialog("初始化数据库出错","数据库无法连接，请检查相应配置！\n异常信息为：" + self.db.dbException + "\n您做的任何变动将无法存入数据库!" )
            else:
                self.msgDialog.showInformationDialog("提示", "数据库配置更改成功！")

    def resetDB(self):
        dbSettingCtrl = DBSettingController()
        dbSettingCtrl.show()
        dbSettingCtrl.exec_()
        self.db.refreshConnection()

    def setGraphColor(self, tar, pos, option): 
        col = QColorDialog.getColor() 
        if col.isValid(): 
            tar.setStyleSheet('QWidget {background-color:%s}' % col.name())
            self.graphStyle[pos]["nodes"][option] = col.name()
        self.refreshUserColor()

    def setLineWidth(self, tar, pos):
        self.graphStyle[pos]["lineLen"] = tar.value()
        self.refreshUserColor()

    def showPreviewGraph(self):
        graph = drawGraph()
        graph.draw("preview", self.user, self.graphStyle)

    def getCompanyInfo(self):
        if self.db.checkConnection():
            companyList = self.db.searchWithKeyword()
            self.completer = QCompleter(companyList)
            self.searchContent.setCompleter(self.completer)

    def search(self):
        searchContent = self.searchContent.text()
        try:
            user = self.db.searchById(searchContent)
        except Exception as e:
            self.msgDialog.showErrorDialog("数据库错误","数据库发生错误！\n异常信息为：" + self.db.dbException + "\n您做的任何变动将无法存入数据库!" )
        else:
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
        self.compilerText.setText(user.compiler)
        self.approverText.setText(user.approver)
        self.auditText.setText(user.audit)
        self.announcerText.setText(user.announcer)
        self.zipText.setText(user.zip)
        self.phoneText.setText(user.phone)
        self.policyText.setText(user.policy)
        #
        dateReg = re.compile(r"^(?P<year>\d{4})[\u4e00-\u9fa5](?P<month>\d{2})[\u4e00-\u9fa5](?P<day>\d{2})[\u4e00-\u9fa5]$")
        date = dateReg.match(user.releaseDate)
        self.releaseDateText.setDate(QDate(int(date.group("year")), int(date.group("month")), int(date.group("day"))))
        date = dateReg.match(user.auditDate)
        self.auditDateText.setDate(QDate(int(date.group("year")), int(date.group("month")), int(date.group("day"))))
        
        #
        self.introductionText.setPlainText("\n".join(user.introduction))

        #数据库中有总经理等项，不需要reset
        self.user.departments = []
        for dep in user.departments:
            self.departmentList.addItem(dep["name"])
            self.user.departments.append(dep)
        self.setDepStruct()

        colors = json.loads(user.color)
        for i in range(len(colors)):
            getattr(self, "level"+str(i+1)+"Border").setStyleSheet('QWidget {background-color:%s}' % colors[i]["nodes"]["fillcolor"])
            getattr(self, "level"+str(i+1)+"Font").setStyleSheet('QWidget {background-color:%s}' % colors[i]["nodes"]["fontcolor"])
            getattr(self, "level"+str(i+1)+"Width").setValue(colors[i]["lineLen"])
        self.graphStyle = colors

        #清空第二页右
        self.depName.setText("")
        self.depLevel.setValue(1)
        self.depIntro.setPlainText("")
        for i in range(1,43):
            getattr(self,'duty_'+str(i)).setCheckState(0)

    def setUser(self):
        #
        self.user.fileName = self.fileNameText.text()
        self.user.company = self.companyText.text()
        self.user.address = self.addressText.text()
        self.user.coverField = self.coverFieldText.text()
        self.user.manager = self.managerText.text()
        self.user.guandai = self.guandaiText.text()
        self.user.compiler = self.compilerText.text()
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
        elif self.depName.text() == "":
            self.msgDialog.showErrorDialog("录入信息错误", "部门名称不能为空")
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
        #clear
        c = self.previewPic.count()
        for i in range(self.previewPic.count()):
            self.previewPic.takeItem(0)
        #add
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
        genDocCtrl = WriteDocController(self.user.fileName)
        genDocCtrl.show()
        genDocCtrl.exec_()
        
        validMsg = self.user.validChecker()
        if validMsg[0]:
            self.refreshDatabase()
            self.msgDialog.showInformationDialog("生成信息", "文档已准备就绪！请点击“OK”开始生成。")
            progress = QProgressDialog(self)
            progress.setWindowTitle("请稍等")  
            progress.setLabelText("正在生成...")
            progress.setCancelButtonText("取消")
            progress.setWindowModality(Qt.WindowModal);
            progress.setRange(0,100)
            progress.setMinimumDuration(2000)
            progress.setValue(0)

            files = genDocCtrl.getAllSelectedFile()
            total = len(files)
            count = 0
            
            for file in files:
                # 线程优化
                count += 1
                wrt_thread = WrtDocThread(self.user, self.pathSelection.getFilePath(file), self.graphStyle, self.pathSelection.getFilePath(file,self.user.fileName))
                wrt_thread.start()
                wrt_thread.wait()
                progress.setValue(int((float(count) / total) * 100))
            '''
            for i in range(31):
                progress.setValue(i)
                time.sleep(0.03)
            '''
            '''
            for i in range(31,101):
                progress.setValue(i)
                time.sleep(0.05)
            '''
            progress.setValue(100)
            self.msgDialog.showInformationDialog("生成信息", "文档成功生成！")
        else:
            self.msgDialog.showErrorDialog("录入信息错误" ,validMsg[1])

    def saveInfoButNotGen(self):
        self.refreshDatabase()

    def refreshDatabase(self):
        try:
            #print("正在更新数据库...")
            self.db.delete("info", self.user.company)
            self.db.insertData(self.user)
        except Exception as e:
            print(e)
            self.msgDialog.showErrorDialog("连接数据库出错","数据库无法连接，更新数据库失败，请检查相应配置！\n异常信息为：" + self.db.dbException + "\n您做的任何变动将无法存入数据库!")
            #print("更新数据库失败")
        else:
            #print("更新数据库成功")
            self.getCompanyInfo()

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
        self.compilerText.setText("")
        self.approverText.setText("")
        self.auditText.setText("")
        self.announcerText.setText("")
        self.zipText.setText("")
        self.phoneText.setText("")
        #日期
        pass
        #部门结构
        #self.user.departments = []
        self.user.resetDepartment()
        self.refreshDepartmentList()
        #第二页右
        self.depName.setText("")
        self.depLevel.setValue(1)
        self.depIntro.setPlainText("")
        for i in range(1,43):
            getattr(self,'duty_'+str(i)).setCheckState(0)

    def refreshUserColor(self):
        self.user.color = json.dumps(self.graphStyle)

    def refreshDepartmentList(self):
        #clear list
        c = self.departmentList.count()
        for i in range(c):
            self.departmentList.takeItem(0)
        c = self.previewPic.count()
        for i in range(c):
            self.previewPic.takeItem(0)

        #add
        for d in self.user.departments:
            self.departmentList.addItem(d["name"])
            self.setDepStruct()
