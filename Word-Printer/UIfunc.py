from MainUI import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from databaseSetting import Ui_databaseSetting
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QColorDialog, QMessageBox, QCompleter, QProgressDialog 
from PyQt5.QtCore import *
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
    
    currentSelectedFile = set()

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
        self.setupLevel2FileList()

    def init_Samples(self):
        self.pathSelector = pathSelection()
        #self.pathSelector.autoRefresh()

    def initToolBar(self):
        self.tabWidget_2.setStyleSheet("QTabBar::tab { height: 30px; min-width: 70px; }")
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 25px !important; min-width: 70px !important; }")

        tool = self.addToolBar("设置")
        edit0 = QAction(QIcon(""),"数据库配置",self)
        tool.addAction(edit0)
        edit1 = QAction(QIcon(""),"更新模板文件",self)
        tool.addAction(edit1)
        tool.actionTriggered.connect(self.toolBtnPressed)

    def connectText(self):
        self.Page_level1_ConnectText()
        self.Page_level2_ConnectText()

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
                self.msgDialog.showWarningDialogWithMethod("警告","发现同名文件，是否进行替换", lambda: shutil.move(path, tarDir), lambda: print("calcel"))
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
                else:
                    self.msgDialog.showErrorDialog("初始化数据库出错","数据库无法连接，请检查相应配置！\n异常信息为：" 
                                                   + self.db.dbException 
                                                   + "\n您做的任何变动将无法存入数据库!" )
        elif qaction.text() == "更新模板文件":
            self.updateLevel2FileList()

    def resetDB(self):
        dbSettingCtrl = DBSettingController()
        dbSettingCtrl.show()
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
            self.updateLevel2FileList()

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
        genDocCtrl = WriteDocController(self.user.fileName, self.currentSelectedFile)
        genDocCtrl.show()
        if genDocCtrl.exec_() == QDialog.Accepted:
            validMsg = self.user.validChecker()
            files = genDocCtrl.getAllSelectedFile()
            self.currentSelectedFile = genDocCtrl.getAllSelectedFile()
            self.updateLevel2FileList()
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

                total = len(files)
                count = 0
            
                for file in files:
                    # 线程优化
                    count += 1
                    wrt_thread = WrtDocThread(self.user, self.pathSelector.getFilePath(file), self.graphStyle, self.pathSelector.getFilePath(file,self.user.fileName))
                    wrt_thread.start()
                    wrt_thread.wait()
                    progress.setValue(int((float(count) / total) * 100))
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

    # level 2 file list
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

    def setupLevel2FileList(self):
        self.level2_fileList.takeTopLevelItem(0)
        root = QTreeWidgetItem(self.level2_fileList)
        root.setText(0, '二层文件模板目录')  # 设置根节点的名称
        self.level2_fileList.addTopLevelItem(root)
        self.level2_fileList.reset()

        temp = self.currentSelectedFile
        self.currentSelectedFile = set()

        tree = self.getLevelFiles("Level2")

        for key, value in tree.items():
            for val in value:
                child = QTreeWidgetItem(root)
                child.setText(0, os.path.split(self.pathSelector.getFilePath(val, self.user.fileName, False))[1])
                if val in temp:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
        self.level2_fileList.sortItems(0, Qt.AscendingOrder)
        self.level2_fileList.expandAll()

    def updateLevel2FileList(self):
        self.setupLevel2FileList()

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