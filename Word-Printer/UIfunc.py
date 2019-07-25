from MainUI import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from databaseSetting import Ui_databaseSetting
from WordPad import Ui_WordPad
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

from dataStruct import userInfo,Project
from generateGraph import drawGraph
from database import DB, DBSettingController
from messageDialog import MessageDialog
from pathSelection import pathSelection
from WriteDocController import WriteDocController, WrtDocThread
from WordPadController import WordPadController
from presetData import *

class Controller(QMainWindow, Ui_MainWindow):

    def __init__(self):
        #init
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        Ui_GenerateDocConfirm.__init__(self)
        Ui_databaseSetting.__init__(self)
        Ui_WordPad.__init__(self)
        self.setupUi(self)

        #connect
        self.initToolBar()
        self.connectButton()
        self.connectText()
        self.connectList()
        
        #message dialog
        self.msgDialog = MessageDialog()

        #graph style
        self.setupVars()

        # use wordPad
        self.connectWordPad()

        #sample dir
        self.init_Samples()

    def setupVars(self):
        self.writeDocLock = threading.RLock()
        self.currentSelectedFile = set()
        self.currentSelectedFile_temp = set()
        self.graphStyle = getGraphStyle()
        self.wpc = None

    def init_DB_user(self):
        #database
        self.db = DB()
        if not self.db.checkConnection():
            self.msgDialog.showErrorDialog("初始化数据库出错","数据库无法连接，请检查相应配置！\n异常信息为：" 
                                           + self.db.dbException 
                                           + "\n您做的任何变动将无法存入数据库!" )

        # search content completer
        self.getCompanyInfo()

        #userInit
        self.user = userInfo()
        self.user.resetDepartment()
        self.refreshDepartmentList()
        if self.user.color == "":
            self.user.color = json.dumps(self.graphStyle)
        self.setupLevelFileList()

    def init_Samples(self):
        self.pathSelector = pathSelection()

    def initToolBar(self):
        self.tabWidget_2.setStyleSheet("QTabBar::tab { height: 50px; width: 120px; font-size: 9pt;}")
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 28px !important; width: 110px !important; }")
        self.tabWidget_3.setStyleSheet("QTabBar::tab { height: 28px !important; width: 110px !important; }")
        self.tabWidget_4.setStyleSheet("QTabBar::tab { height: 28px !important; width: 150px !important; }")

        tool = self.addToolBar("设置")
        edit0 = QAction(QIcon(""),"数据库配置",self)
        tool.addAction(edit0)
        edit1 = QAction(QIcon(""),"更新模板文件",self)
        tool.addAction(edit1)
        tool.actionTriggered.connect(self.toolBtnPressed)

    def connectText(self):
        self.Page_level1_ConnectText()
        self.Page_level2_ConnectText()
        self.Page_level3_ConnectText()

    def Page_level1_ConnectText(self):
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
        self.corporateText.textChanged.connect( lambda : self.setUser() )

        self.releaseDateText.dateChanged.connect( lambda : self.setUser() )
        self.auditDateText.dateChanged.connect( lambda : self.setUser() )
        # logo
        self.Logo.textChanged.connect(lambda : self.showLogo())

        # style
        self.level1Width.valueChanged.connect(lambda: self.setLineWidth(self.level1Width, 0))
        self.level2Width.valueChanged.connect(lambda: self.setLineWidth(self.level2Width, 1))
        self.level3Width.valueChanged.connect(lambda: self.setLineWidth(self.level3Width, 2))
        self.level4Width.valueChanged.connect(lambda: self.setLineWidth(self.level4Width, 3))

    def Page_level2_ConnectText(self):
        self.level2_fileList.setAnimated(True)
        self.level2_fileList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.level2_fileList.itemChanged.connect(self.level2FileChangeHandler)

    def Page_level3_ConnectText(self):
        self.level3_fileList.setAnimated(True)
        self.level3_fileList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.level3_fileList.itemChanged.connect(self.level3FileChangeHandler)

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

    def openPadAction(self, name):
        wordpad = QAction(QIcon(""), "打开写字板", self)
        wordpad.triggered.connect(lambda: self.openWordPad(name))
        ctrlC = QAction(QIcon(""), "复制", self)
        ctrlC.setShortcut("Ctrl+C")
        ctrlC.triggered.connect(self.__dict__[name].copy)
        ctrlV = QAction(QIcon(""), "粘贴", self)
        ctrlV.setShortcut("Ctrl+V")
        ctrlV.triggered.connect(self.__dict__[name].paste)
        ctrlX = QAction(QIcon(""), "剪切", self)
        ctrlX.setShortcut("Ctrl+X")
        ctrlX.triggered.connect(self.__dict__[name].cut)
        ctrlA = QAction(QIcon(""), "全选", self)
        ctrlA.setShortcut("Ctrl+A")
        ctrlA.triggered.connect(self.__dict__[name].selectAll)
        return [wordpad, ctrlC, ctrlV, ctrlX,ctrlA]

    def connectWordPad(self):
        for k,v in self.__dict__.items():
            if isinstance(v, QLineEdit) or isinstance(v, QPlainTextEdit):
                actionList = self.openPadAction(k)
                for act in actionList:
                    self.__dict__[k].addAction(act)
                self.__dict__[k].setContextMenuPolicy(Qt.ActionsContextMenu)

    def connectList(self):
        #连接一层department列表
        self.connectDepartmentList()

        #连接四层project列表
        self.connectProjectList()

    def connectDepartmentList(self):
        #可能没选中，故用getattr确认
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))
        # button
        self.AddDep.clicked.connect( lambda: self.addDepartment() )
        #可能没选中，故用getattr确认
        self.DeleteDep.clicked.connect( lambda: self.removeDepartment( getattr( self.departmentList.currentItem(),'text',str)() ) )
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
        #print(path)
        if path and path != "" and image.load(path):
            filepath, filename = os.path.split(path)
            if not os.path.exists("./logoData"):
                os.makedirs("./logoData")
            tarDir = "./logoData/" + filename
            if not os.path.exists(tarDir):
                tarDir = "./logoData/%s_%s" %(self.user.company, filename)
            try:
                shutil.copy(path, tarDir)
            except Exception as e:
                shutil.move(path, tarDir)
            image = image.scaledToHeight(self.logoView.height())
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap.fromImage(image))
            self.logoView.setScene(scene)
            self.logoView.show()
            #save
            self.user.logoPath = tarDir
    
    def toolBtnPressed(self, qaction):
        if qaction.text() == "数据库配置":
            if self.resetDB():
                self.db.refreshConnection()
                if self.db.checkConnection():
                    self.msgDialog.showInformationDialog("提示", "数据库配置更改成功！")
                    self.getCompanyInfo()
                else:
                    self.msgDialog.showErrorDialog("初始化数据库出错","数据库无法连接，请检查相应配置！\n异常信息为：" 
                                                   + self.db.dbException 
                                                   + "\n您做的任何变动将无法存入数据库!" )
        elif qaction.text() == "更新模板文件":
            self.updateLevelFileList()

    def openWordPad(self, objName):
        self.wpc = WordPadController() if self.wpc is None else self.wpc
        #print(objName)
        if isinstance(self.__dict__[objName], QLineEdit):
            self.wpc.initInfo(self.__dict__[objName].text())
        elif isinstance(self.__dict__[objName], QPlainTextEdit):
            self.wpc.initInfo(self.__dict__[objName].toPlainText())
        else:
            self.msgDialog.showErrorDialog("出错", "该项暂不支持写字板输入")
            return
        if self.wpc.exec_() == QDialog.Accepted:
            if isinstance(self.__dict__[objName], QLineEdit):
                self.__dict__[objName].setText(self.wpc.getInfo())
            elif isinstance(self.__dict__[objName], QPlainTextEdit):
                self.__dict__[objName].setPlainText(self.wpc.getInfo())


    def resetDB(self):
        dbSettingCtrl = DBSettingController()
        #dbSettingCtrl.show()
        return dbSettingCtrl.exec_() == QDialog.Accepted

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
            self.msgDialog.showErrorDialog("数据库错误","数据库发生错误！\n异常信息为：" 
                                           + self.db.dbException 
                                           + "\n您做的任何变动将无法存入数据库!" )
        else:
            if user.company != "":
                self.setInput(user)
            self.searchContent.setText("")
            self.currentSelectedFile = set()
            self.updateLevelFileList()

    def setInput(self, user):
        #clear
        c = self.departmentList.count()
        for i in range(c):
            self.departmentList.takeItem(0)
        c = self.previewPic.count()
        for i in range(c):
            self.previewPic.takeItem(0)
        c = self.projectList.count()
        for i in range(c):
            self.projectList.takeItem(0)

        #
        self.fileNameText.setText(user.fileName)
        self.companyText.setText(user.company)
        self.addressText.setText(user.address)
        self.coverFieldText.setText(user.coverField)
        self.corporateText.setText(user.corporateRepresentative)
        self.managerText.setText(user.manager)
        self.guandaiText.setText(user.guandai)
        self.compilerText.setText(user.compiler)
        self.approverText.setText(user.approver)
        self.auditText.setText(user.audit)
        self.announcerText.setText(user.announcer)
        self.zipText.setText(user.zip)
        self.phoneText.setText(user.phone)
        self.policyText.setText(user.policy)
        self.Logo.setPlainText(user.logoPath)
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

        #四层项目
        self.user.projects = []
        for proj in user.projects:
            self.projectList.addItem( proj.BasicInfo.PartyA.projectName )
            self.user.projects.append( proj )
        #四层组织
        self.user.organization = user.organization
        self.showOrganization()

    def setUser(self):
        #
        self.user.fileName = self.fileNameText.text()
        self.user.company = self.companyText.text()
        self.user.address = self.addressText.text()
        self.user.coverField = self.coverFieldText.text()
        self.user.corporateRepresentative = self.corporateText.text()
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
            department['leader'] = self.leader.text()
            department['operator'] = self.Operator.text()
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

    def showDepartmentDetail(self,departmentName):
        if departmentName == "":
            self.depName.setText( "" )
            self.depIntro.setPlainText( "" )
            self.depLevel.setValue( 0 )
            self.leader.setText("")
            self.Operator.setText("")
            for i in range(1,43):
                getattr(self,'duty_'+str(i)).setCheckState(0)
        else:
            department = self.user.departments[ self.departmentList.row( self.departmentList.currentItem() ) ]
            self.depName.setText( departmentName )
            self.depIntro.setPlainText( '\n'.join(department['intro']) if 'intro' in department else "" )
            self.depLevel.setValue( department['level'] if 'level' in department else 1 )
            self.leader.setText( department['leader'] if 'leader' in department else "" )
            self.Operator.setText( department['operator'] if 'operator' in department else "" )

            #特别情况
            if departmentName == "总经理" or departmentName == "管理者代表":
                self.leader.setEnabled(False)
                self.Operator.setEnabled(False)
            else:
                self.leader.setEnabled(True)
                self.Operator.setEnabled(True)
            
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
        genDocCtrl = WriteDocController(self.user.fileName, self.currentSelectedFile)
        #genDocCtrl.show()
        if genDocCtrl.exec_() == QDialog.Accepted:
            validMsg = self.user.validChecker()
            files = genDocCtrl.getAllSelectedFile()
            self.currentSelectedFile = genDocCtrl.getAllSelectedFile()
            self.updateLevelFileList()
            if validMsg[0]:
                self.refreshDatabase()
                self.msgDialog.showInformationDialog("生成信息", "文档已准备就绪！共有%d份文档，请点击“OK”开始生成。" % len(files))
                progress = QProgressDialog(self)
                progress.setWindowTitle("请稍等")  
                progress.setLabelText("正在生成...")
                progress.setCancelButtonText("取消")
                progress.setWindowModality(Qt.WindowModal);
                progress.setRange(0,100)
                progress.setMinimumDuration(2000)
                progress.setValue(0)

                total = len(files)
                count = 0

                #生成并保存部门结构图
                graph = drawGraph()
                self.user = graph.draw("save", self.user, self.graphStyle)
            
                for file in files:
                    # 线程优化
                    self.writeDocLock.acquire()
                    count += 1
                    wrt_thread = WrtDocThread(self.user, self.pathSelector.getFilePath(file),
                                              self.graphStyle, self.pathSelector.getFilePath(file,self.user.fileName))
                    wrt_thread.start()
                    wrt_thread.wait()
                    progress.setValue(int((float(count) / total) * 100))
                    self.writeDocLock.release()
                progress.setValue(100)
                self.msgDialog.showInformationDialog("生成信息", "文档成功生成！")
            else:
                self.msgDialog.showErrorDialog("录入信息错误" ,validMsg[1])

    def saveInfoButNotGen(self):
        self.refreshDatabase(True)

    def refreshDatabase(self, isSave = False):
        try:
            #print("正在更新数据库...")
            self.db.delete("info", self.user.company)
            self.db.insertData(self.user)
            if(isSave):
                self.msgDialog.showInformationDialog("提示","文档信息已保存到数据库")
        except Exception as e:
            #print("更新数据库失败")
            print(e)
            self.msgDialog.showErrorDialog("连接数据库出错","数据库无法连接，更新数据库失败，请检查相应配置！\n异常信息为：" 
                                           + self.db.dbException
                                           + "\n您做的任何变动将无法存入数据库!")
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

    # level 2 / 3 file list
    def getLevelFiles(self, LEVEL_NAME):
        self.pathSelector.autoRefresh()
        level = self.pathSelector.getLevelDir()
        tree = {}
        for key,value in level.items():
            if value in tree:
                tree[value].append(key)
            else:
                tree[value] = [key]

        for key in list(tree.keys()):
            if key != LEVEL_NAME:
                tree.pop(key)
        return tree

    def setupLevelFileList(self):
        self.currentSelectedFile_temp = self.currentSelectedFile
        self.currentSelectedFile = set()
        self.setupLevelFileList_level(self.level2_fileList, "Level2", '二层文件模板目录')
        self.setupLevelFileList_level(self.level3_fileList, "Level3", '三层文件模板目录')

    def setupLevelFileList_level(self, fileList_item, levelstr, rootname):
        fileList_item.takeTopLevelItem(0)
        root = QTreeWidgetItem(fileList_item)
        root.setText(0,  rootname) # 设置根节点的名称
        fileList_item.addTopLevelItem(root)
        fileList_item.reset()

        tree = self.getLevelFiles(levelstr)

        for key, value in tree.items():
            for val in value:
                child = QTreeWidgetItem(root)
                child.setText(0, os.path.split(self.pathSelector.getFilePath(val, self.user.fileName, False))[1])
                if val in self.currentSelectedFile_temp:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
        fileList_item.sortItems(0, Qt.AscendingOrder)
        fileList_item.expandAll()

    def updateLevelFileList(self):
        self.setupLevelFileList()

    def getLable(self, name):
        reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
        prefix = re.search(reg, name, re.M|re.I)
        label = []
        if(prefix):
            label = prefix.group(1).split("-")
            label = label[-3:len(label)]
        return "-".join(label)

    def level2FileChangeHandler(self, item, column):
        if item.checkState(column) == Qt.Checked:
            self.currentSelectedFile.add(self.getLable(item.text(column)))
        elif item.checkState(column) == Qt.Unchecked:
            self.currentSelectedFile.discard(self.getLable(item.text(column)))

    def level3FileChangeHandler(self, item, column):
        if item.checkState(column) == Qt.Checked:
            self.currentSelectedFile.add(self.getLable(item.text(column)))
        elif item.checkState(column) == Qt.Unchecked:
            self.currentSelectedFile.discard(self.getLable(item.text(column)))

    #四层页面
    def connectProjectList( self ):
        #可能没选中，用attr确认
        #选中时为 projectList.currentItem().text() ,否则为 str()
        self.projectList.currentItemChanged.connect( lambda: self.showProjectDetail( getattr(self.projectList.currentItem(),'text',str)() ) )
        self.AddProject.clicked.connect( lambda: self.addProject() )
        self.DeleteProject.clicked.connect( lambda: self.removeProject( getattr(self.projectList.currentItem(),'text',str)() ) )
        self.cancelProject.clicked.connect( lambda: self.showProjectDetail( getattr(self.projectList.currentItem(),'text',str)() ) )
        self.saveProject.clicked.connect( lambda: self.setProject( getattr(self.projectList.currentItem(),'text',str)() ) )
        #四层组织
        self.saveOrgan.clicked.connect( lambda: self.setOrganization() )
        self.discardOrgan.clicked.connect( lambda: self.showOrganization() )

    def addProject( self , projectName="项目名称" ):
        self.projectList.addItem( projectName )
        new = Project(projectName)
        self.user.projects.append( new )
        self.projectList.setCurrentItem( self.projectList.item( self.projectList.count()-1 )  )

    def removeProject( self , projectName="" ):
        if( projectName == "" ):
            return
        else:
            ### critical ###
            index = self.projectList.row( self.projectList.currentItem() )
            self.projectList.takeItem( index )
            del self.user.projects[ index ]
            ### end Critical ###

    def setProject( self , projectName ):
        if projectName == "":
            pass
        elif self.AprojectNameText.text() == "":
            self.msgDialog.showErrorDialog("录入信息错误","项目名称不能为空")
        else:
            project = self.user.projects[self.projectList.row( self.projectList.currentItem() ) ]
            self.projectList.currentItem().setText( self.AprojectNameText.text() )
            self.setA(project)
            self.setB(project)
            self.setDetail(project)
            self.setTeam(project)
            self.setReport(project)
            self.setProjectEvent(project)
            self.setConfig(project)
            self.setContinuity(project)
            #self.setAudit(project)
            #self.setRecord(project)

    def showProjectDetail( self, projectName ):
        if projectName == "":
            self.showA()
            self.showB()
            self.showDetail()
            self.showTeam()
            self.showReport()
            self.showProjectEvent()
            self.showConfig()
            self.showContinuity()
            #self.showAudit()
            #self.showRecord()
        else:
            project = self.user.projects[self.projectList.row( self.projectList.currentItem() ) ]
            self.showA(project)
            self.showB(project)
            self.showDetail(project)
            self.showTeam(project)
            self.showReport(project)
            self.showProjectEvent(project)
            self.showConfig(project)
            self.showContinuity(project)
            #self.showAudit(project)
            #self.showRecord(project)

    def setOrganization(self):
        self.setAudit()
        self.setRecord()
        #
        self.showOrganization()

    def showOrganization(self):
        self.showAudit()
        self.showRecord()

    def setA(self,project):
        project.BasicInfo.PartyA.projectName = self.AprojectNameText.text()
        project.BasicInfo.PartyA.company = self.AcompanyText.text()
        project.BasicInfo.PartyA.name = self.AnameText.text()
        project.BasicInfo.PartyA.phone = self.AphoneText.text()
        project.BasicInfo.PartyA.address = self.AaddressText.text()

    def setB(self,project):
        project.BasicInfo.PartyB.contactName = self.BcontactNameText.text()
        project.BasicInfo.PartyB.serviceName = self.BserviceNameText.text()
        project.BasicInfo.PartyB.serviceMail = self.BserviceMailText.text()
        project.BasicInfo.PartyB.servicePhone = self.BservicePhoneText.text()
        project.BasicInfo.PartyB.complainName = self.BcomplainNameText.text()
        project.BasicInfo.PartyB.complainMail = self.BcomplainMailText.text()
        project.BasicInfo.PartyB.complainPhone = self.BcomplainPhoneText.text()

    def setDetail(self,project):
         project.BasicInfo.Detail.amount = self.amountText.text()
         project.BasicInfo.Detail.period = self.periodText.text()
         project.BasicInfo.Detail.config = self.configText.text()
         project.BasicInfo.Detail.name = self.detailNameText.text()
         project.BasicInfo.Detail.level = self.detailLevelText.text()
         project.BasicInfo.Detail.details = self.detailsText.text()
         project.BasicInfo.Detail.demand = self.demandText.text()
         project.BasicInfo.Detail.ddl = self.ddlText.text()

    def setTeam(self,project):
        project.BasicInfo.Team.startTime = self.startTimeText.text()
        project.BasicInfo.Team.require = self.requireText.text()
        project.BasicInfo.Team.PM = self.PMText.text()
        project.BasicInfo.Team.TM = self.TMText.text()

    def setReport(self,project):
        project.ServiceProcess.Report.time = str(self.reportTimeText.toPlainText()).split('\n')
        project.ServiceProcess.Report.keypoint = str(self.keypointText.toPlainText()).split('\n')
        project.ServiceProcess.Report.revisit = self.revisitText.text()

    def setProjectEvent(self,project):
        project.ServiceProcess.Event.eventManager = self.eventManagerText.text()
        project.ServiceProcess.Event.issueManager = self.issueManagerText.text()
        project.ServiceProcess.Event.level = self.eventLevelText.currentText()
        project.ServiceProcess.Event.accepted = self.acceptedText.value()
        project.ServiceProcess.Event.closed = self.closedText.value()
        project.ServiceProcess.Event.transformed = self.transformedText.value()
        project.ServiceProcess.Event.summarized = self.summarizedText.value()

    def setConfig(self,project):
        project.ServiceProcess.Config.modifyManager = self.modifyManagerText.text()
        project.ServiceProcess.Config.configManager = self.configManagerText.text()
        project.ServiceProcess.Config.releaseManager = self.releaseManagerText.text()
        project.ServiceProcess.Config.relatedManager = self.relatedManagerText.text()
        project.ServiceProcess.Config.configVersion = self.configVersionText.text()
        project.ServiceProcess.Config.configReleaseDate = self.configReleaseDateText.text()
        project.ServiceProcess.Config.changes = int(self.changesText.text())
        project.ServiceProcess.Config.releases = int(self.releasesText.text())
        project.ServiceProcess.Config.releaseDate = self.ConfigReleaseDateText.text()
        project.ServiceProcess.Config.preReleaseDate = self.ConfigPreReleaseDateText.text()
        project.ServiceProcess.Config.applicationDate = self.applicationDateText.text()
        project.ServiceProcess.Config.SN = self.SNText.text()
        project.ServiceProcess.Config.target = self.targetText.text()
        project.ServiceProcess.Config.item = self.itemText.text()
        project.ServiceProcess.Config.releaseVersion = self.releaseVersionText.text()

    def setContinuity(self,project):
        project.ServiceProcess.Continuity.process = str(self.processText.toPlainText()).split('\n')
        project.ServiceProcess.Continuity.result = str(self.resultText.toPlainText()).split('\n')
        project.ServiceProcess.Continuity.date = self.ContinuityDateText.text()
        project.ServiceProcess.Continuity.technicist = self.technicistText.text()
        project.ServiceProcess.Continuity.approver = self.ContinuityApproverText.text()
        project.ServiceProcess.Continuity.compileDate = self.ContinuityCompileDateText.text()
        project.ServiceProcess.Continuity.auditDate = self.ContinuityAuditDateText.text()

    def setAudit(self):
        self.user.organization.Audit.planDate = self.planDateText.text()
        self.user.organization.Audit.auditDate = self.AuditAuditDateText.text()
        self.user.organization.Audit.auditLeader = self.auditLeaderText.text()
        self.user.organization.Audit.audit1 = self.audit1Text.text()
        self.user.organization.Audit.audit2 = self.audit2Text.text()
        self.user.organization.Audit.audit3 = self.audit3Text.text()
        self.user.organization.Audit.reviewDate = self.reviewDateText.text()
        self.user.organization.Audit.scheduleDate = self.scheduleDateText.text()
        self.user.organization.Audit.excuteDate = self.excuteDateText.text()
        self.user.organization.Audit.reportDate = self.reportDateText.text()
        self.user.organization.Audit.compiler = self.AuditCompilerText.text()
        self.user.organization.Audit.audit = self.AuditAuditText.text()
        self.user.organization.Audit.compileDate = self.AuditCompileDateText.text()
        self.user.organization.Audit.approveDate = self.AuditApproveDateText.text()
    
    def setRecord(self):
        self.user.organization.Record.target = self.RecordTargetText.text()
        self.user.organization.Record.time = self.RecordTimeText.text()
        self.user.organization.Record.staff = self.RecordStaffText.text()
        self.user.organization.Record.arrange = self.RecordArrangeText.text()
        self.user.organization.Record.content = str(self.RecordContentText.toPlainText()).split('\n')
        self.user.organization.Record.fileName = self.RecordFileNameText.text()
        self.user.organization.Record.auditContent = str(self.auditContentText.toPlainText()).split('\n')
        self.user.organization.Record.auditProcess = str(self.auditProcessText.toPlainText()).split('\n')
        self.user.organization.Record.audit = self.RecordAuditText.text()
        self.user.organization.Record.auditDate = self.RecordAuditDateText.text()
        self.user.organization.Record.approver = self.RecordApproverText.text()
        self.user.organization.Record.approveDate = self.RecordApproveDateText.text()
        self.user.organization.Record.provider = self.providerText.text()

    def showA(self,project=""):
        if project == "":
            project = Project("")
        self.AprojectNameText.setText(project.BasicInfo.PartyA.projectName)
        self.AcompanyText.setText(project.BasicInfo.PartyA.company)
        self.AnameText.setText(project.BasicInfo.PartyA.name)
        self.AphoneText.setText(project.BasicInfo.PartyA.phone)
        self.AaddressText.setText(project.BasicInfo.PartyA.address)
    
    def showB(self,project=""):
        if project == "":
            project = Project("")
        self.BcontactNameText.setText(project.BasicInfo.PartyB.contactName)
        self.BserviceNameText.setText(project.BasicInfo.PartyB.serviceName)
        self.BserviceMailText.setText(project.BasicInfo.PartyB.serviceMail)
        self.BservicePhoneText.setText(project.BasicInfo.PartyB.servicePhone)
        self.BcomplainNameText.setText(project.BasicInfo.PartyB.complainName)
        self.BcomplainMailText.setText(project.BasicInfo.PartyB.complainMail)
        self.BcomplainPhoneText.setText(project.BasicInfo.PartyB.complainPhone)
    
    def showDetail(self,project=""):
        if project == "":
            project = Project("")
        self.amountText.setText(project.BasicInfo.Detail.amount)
        self.periodText.setText(project.BasicInfo.Detail.period)
        self.configText.setText(project.BasicInfo.Detail.config)
        self.detailNameText.setText(project.BasicInfo.Detail.name)
        self.detailLevelText.setText(project.BasicInfo.Detail.level)
        self.detailsText.setText(project.BasicInfo.Detail.details)
        self.demandText.setText(project.BasicInfo.Detail.demand)
        self.ddlText.setText(project.BasicInfo.Detail.ddl)
    
    def showTeam(self,project=""):
        if project == "":
            project = Project("")
        self.startTimeText.setText(project.BasicInfo.Team.startTime)
        self.requireText.setText(project.BasicInfo.Team.require)
        self.PMText.setText(project.BasicInfo.Team.PM)
        self.TMText.setText(project.BasicInfo.Team.TM)
    
    def showReport(self,project=""):
        if project == "":
            project = Project("")
        self.reportTimeText.setPlainText( "\n".join(project.ServiceProcess.Report.time) )
        self.keypointText.setPlainText( "\n".join(project.ServiceProcess.Report.keypoint) )
        self.revisitText.setText(project.ServiceProcess.Report.revisit)
    
    def showProjectEvent(self,project=""):
        if project == "":
            project = Project("")
        self.eventManagerText.setText(project.ServiceProcess.Event.eventManager)
        self.issueManagerText.setText(project.ServiceProcess.Event.issueManager)
        self.eventLevelText.setCurrentText(project.ServiceProcess.Event.level)
        self.acceptedText.setValue(project.ServiceProcess.Event.accepted)
        self.closedText.setValue(project.ServiceProcess.Event.closed)
        self.transformedText.setValue(project.ServiceProcess.Event.transformed)
        self.summarizedText.setValue(project.ServiceProcess.Event.summarized)
    
    def showConfig(self,project=""):
        if project == "":
            project = Project("")
        self.modifyManagerText.setText(project.ServiceProcess.Config.modifyManager)
        self.configManagerText.setText(project.ServiceProcess.Config.configManager)
        self.releaseManagerText.setText(project.ServiceProcess.Config.releaseManager)
        self.relatedManagerText.setText(project.ServiceProcess.Config.relatedManager)
        self.configVersionText.setText(project.ServiceProcess.Config.configVersion)
        self.configReleaseDateText.setText(project.ServiceProcess.Config.configReleaseDate)
        self.changesText.setText(str(project.ServiceProcess.Config.changes))
        self.releasesText.setText(str(project.ServiceProcess.Config.releases))
        self.ConfigReleaseDateText.setText(project.ServiceProcess.Config.releaseDate)
        self.ConfigPreReleaseDateText.setText(project.ServiceProcess.Config.preReleaseDate)
        self.applicationDateText.setText(project.ServiceProcess.Config.applicationDate)
        self.SNText.setText(project.ServiceProcess.Config.SN)
        self.targetText.setText(project.ServiceProcess.Config.target)
        self.itemText.setText(project.ServiceProcess.Config.item)
        self.releaseVersionText.setText(project.ServiceProcess.Config.releaseVersion)
    
    def showContinuity(self,project=""):
        if project == "":
            project = Project("")
        self.processText.setPlainText("\n".join(project.ServiceProcess.Continuity.process))
        self.resultText.setPlainText("\n".join(project.ServiceProcess.Continuity.result))
        self.ContinuityDateText.setText(project.ServiceProcess.Continuity.date)
        self.technicistText.setText(project.ServiceProcess.Continuity.technicist)
        self.ContinuityApproverText.setText(project.ServiceProcess.Continuity.approver)
        self.ContinuityCompileDateText.setText(project.ServiceProcess.Continuity.compileDate)
        self.ContinuityAuditDateText.setText(project.ServiceProcess.Continuity.auditDate)
    
    def showAudit(self):
        self.planDateText.setText(self.user.organization.Audit.planDate)
        self.AuditAuditDateText.setText(self.user.organization.Audit.auditDate)
        self.auditLeaderText.setText(self.user.organization.Audit.auditLeader)
        self.audit1Text.setText(self.user.organization.Audit.audit1)
        self.audit2Text.setText(self.user.organization.Audit.audit2)
        self.audit3Text.setText(self.user.organization.Audit.audit3)
        self.reviewDateText.setText(self.user.organization.Audit.reviewDate)
        self.scheduleDateText.setText(self.user.organization.Audit.scheduleDate)
        self.excuteDateText.setText(self.user.organization.Audit.excuteDate)
        self.reportDateText.setText(self.user.organization.Audit.reportDate)
        self.AuditCompilerText.setText(self.user.organization.Audit.compiler)
        self.AuditAuditText.setText(self.user.organization.Audit.audit)
        self.AuditCompileDateText.setText(self.user.organization.Audit.compileDate)
        self.AuditApproveDateText.setText(self.user.organization.Audit.approveDate)
    
    def showRecord(self):
        self.RecordTargetText.setText(self.user.organization.Record.target)
        self.RecordTimeText.setText(self.user.organization.Record.time)
        self.RecordStaffText.setText(self.user.organization.Record.staff)
        self.RecordArrangeText.setText(self.user.organization.Record.arrange)
        self.RecordContentText.setPlainText("\n".join(self.user.organization.Record.content))
        self.RecordFileNameText.setText(self.user.organization.Record.fileName)
        self.auditContentText.setPlainText("\n".join(self.user.organization.Record.auditContent))
        self.auditProcessText.setPlainText("\n".join(self.user.organization.Record.auditProcess))
        self.RecordAuditText.setText(self.user.organization.Record.audit)
        self.RecordAuditDateText.setText(self.user.organization.Record.auditDate)
        self.RecordApproverText.setText(self.user.organization.Record.approver)
        self.RecordApproveDateText.setText(self.user.organization.Record.approveDate)
        self.providerText.setText(self.user.organization.Record.provider)