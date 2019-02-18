from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from dataStruct import userInfo

class Controller(QMainWindow, Ui_MainWindow):
    user = userInfo()

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

        #
        self.AddDep.clicked.connect( lambda: self.addDepartment() )

        #preview
        self.createBotton.clicked.connect(lambda: self.depIntro.setPlainText(str(vars(self.user))))

    def connectList(self):
        self.departmentList.currentItemChanged.connect( lambda: self.showDepartmentDetail( self.departmentList.currentItem().text() ) )

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

    def addDepartment(self,departmentName="部门名称"):
        self.departmentList.addItem(departmentName)
        self.user.departments.append({"name":departmentName})

    def showDepartmentDetail(self,departmentName):
        for department in self.user.departments:
            if department['name'] == departmentName:
                self.depName.setText( departmentName )
                #self.depIntro.setPlainText( department["intro"] )
                #self.depLevel.setValue( department["level"] )
                self.depIntro.setPlainText( getattr(department,"intro","") )
                self.depLevel.setValue( getattr(department,"intro",1) )
                


