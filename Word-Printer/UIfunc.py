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

        # 右键写字板
        editSearch = QAction(QIcon(""), "打开写字板", self)
        editSearch.triggered.connect(lambda: self.openWordPad("searchContent"))
        self.searchContent.addAction(editSearch)
        self.searchContent.setContextMenuPolicy(Qt.ActionsContextMenu)

        editIntro = QAction(QIcon(""), "打开写字板", self)
        editIntro.triggered.connect(lambda: self.openWordPad("introductionText"))
        self.introductionText.addAction(editIntro)
        self.introductionText.setContextMenuPolicy(Qt.ActionsContextMenu)

    def connectList(self):
        #可能没选中，故用getattr确认
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))
        # button
        self.AddDep.clicked.connect( lambda: self.addDepartment() )
        #可能没选中，故用getattr确认
        self.DeleteDep.clicked.connect( lambda: self.removeDepartment( getattr( self.departmentList.currentItem(),'text',str)() ) )
        self.cancelDep.clicked.connect( lambda: self.showDepartmentDetail( getattr( self.departmentList.currentItem(),'text',str)() ))
        self.addOrModifyDep.clicked.connect( lambda: self.setDepartments(getattr( self.departmentList.currentItem(),'text',str)() ) )

        #
        self.connectProjectList()

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

    def addProject( self , projectName="项目名称" ):
        self.projectList.addItem( projectName )
        self.user.projects.append( Project(projectName) )
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
            self.msgDialog,showErrorDialog("录入信息错误","项目名称不能为空")
        else:
            project = self.user.projects[self.projectList.row( self.projectList.currentItem() ) ]
            self.projectList.currentItem().setText( self.AprojectNameText.text() )
            self.setA(project)
            '''
            self.setB(project)
            self.setDetail(project)
            self.setReport(project)
            self.setTeam(project)
            self.setEvent(project)
            self.setConfig(project)
            self.setContinuity(project)
            self.setAudit(project)
            self.setRecord(project)
            '''

    def showProjectDetail( self, projectName ):
        if projectName == "":
            self.showA()
        else:
            project = self.user.projects[self.projectList.row( self.projectList.currentItem() ) ]
            self.showA(project)
        '''
        self.showB()
        self.showDetail()
        self.showReport()
        self.showTeam()
        self.showProjectEvent()
        self.showConfig()
        self.showContinuity()
        self.showAudit()
        self.showRecord()
        '''

    def setA(self,project):
        project.BasicInfo.PartyA.projectName = self.AprojectNameText.text()
        project.BasicInfo.PartyA.company = self.AcompanyText.text()
        project.BasicInfo.PartyA.name = self.AnameText.text()
        project.BasicInfo.PartyA.phone = self.AphoneText.text()
        project.BasicInfo.PartyA.address = self.AaddressText.text()

    def setB(self,project):
        project.BasicInfo.PratyB.contactName = self.BcontactNameText.text()
        project.BasicInfo.PratyB.serviceName = self.BserviceNameText.text()
        project.BasicInfo.PratyB.serviceMail = self.BserviceMailText.text()
        project.BasicInfo.PratyB.servicePhone = self.BservicePhoneText.text()
        project.BasicInfo.PratyB.complainName = self.BcomplainNameText.text()
        project.BasicInfo.PratyB.complainMail = self.BcomplainMailText.text()
        project.BasicInfo.PratyB.complainPhone = self.BcomplainPhoneText.text()

    def setDetail(self,project):
        pass
    def setTeam(self,project):
        pass
    def setReport(self,project):
        pass
    def setEvent(self,project):
        pass
    def setConfig(self,project):
        pass
    def setContinuity(self,project):
        pass
    def setAudit(self,project):
        pass
    def setRecord(self,project):
        pass

    def showA(self,project=""):
        if project == "":
            project = Project("")
        self.AprojectNameText.setText(project.BasicInfo.PartyA.projectName)
        self.AcompanyText.setText(project.BasicInfo.PartyA.company)
        self.AnameText.setText(project.BasicInfo.PartyA.name)
        self.AphoneText.setText(project.BasicInfo.PartyA.phone)
        self.AaddressText.setText(project.BasicInfo.PartyA.address)
    def showB(self,project):
        pass
    def showDetail(self,project):
        pass
    def showTeam(self,project):
        pass
    def showReport(self,project):
        pass
    def showProjectEvent(self):
        pass
    def showConfig(self,project):
        pass
    def showContinuity(self,project):
        pass
    def showAudit(self,project):
        pass
    def showRecord(self,project):
        pass
