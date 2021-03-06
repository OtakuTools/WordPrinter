# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import threading
import pymysql
import json

from dataStruct import userInfo, Project, Organization
from databaseSetting import Ui_databaseSetting
from databaseTableConfig import databaseTableConfig

class DBSettingController(QDialog, Ui_databaseSetting):

    info =  { 'ip' : 'localhost', 'user' : 'root', 'pswd' : '1234', 'dbname' : 'wordStore', 'port': 3306}

    def __init__(self):
        QDialog.__init__(self)
        Ui_databaseSetting.__init__(self)
        self.setupUi(self)
        self.setConnection()
        self.initInfo()

    def setConnection(self):
        self.dbbuttonBox.accepted.connect(self.save)
        self.dbbuttonBox.rejected.connect(self.cancel)

    def save(self):
        self.upgradeConnection()
        with open("./config/dbConfig.json", "w") as f:
            json.dump(self.info, f, sort_keys=True, indent=4, separators=(',', ': '))
        self.accept()

    def cancel(self):
        self.reject()

    def initInfo(self):
        with open("./config/dbConfig.json", "r") as f:
            self.info = json.load(f)
        self.dbIP.setText(self.info["ip"])
        self.dbNAME.setText(self.info["dbname"])
        self.dbUSER.setText(self.info["user"])
        self.dbPSWD.setText(self.info["pswd"])

    def upgradeConnection(self):
        self.info["ip"] = self.dbIP.text()
        self.info["dbname"] = self.dbNAME.text()
        self.info["user"] = self.dbUSER.text()
        self.info["pswd"] = self.dbPSWD.text()

    def getInfo(self):
        return self.info

class DB:
    db = None
    dbException = "None"
    _conn_timeout = 3

    def __init__(self):
        self.initConnection()

    def __del__(self):
        if self.db:
            self.db.close()

    def setupConnectionThread_host(self):
        try:
            self.db = pymysql.connect(host=self.info['ip'], 
                                      user=self.info['user'], 
                                      password=self.info['pswd'], 
                                      port=self.info['port'], 
                                      connect_timeout=self._conn_timeout)
        except Exception as e:
            self.db = None
            self.dbException = str(e)
            return

    def setupConnectionThread_db(self):
        try:
            self.db = pymysql.connect(host=self.info['ip'], 
                                      user=self.info['user'], 
                                      password=self.info['pswd'], 
                                      port=self.info['port'], 
                                      database=self.info['dbname'],
                                      connect_timeout=self._conn_timeout)
        except Exception as e:
            self.db = None
            self.dbException = str(e)
            return

    def dbOperation_threading(self, sql):
        try:
            ptr = self.db.cursor()
            ptr.execute(sql)
        except Exception as e:
            self.dbException = str(e)
            self.db.rollback()
            return

    def initConnection(self):
        self.info = self.loadConfig()
        try:
            t = threading.Thread(target=self.setupConnectionThread_host)
            t.start()
            t.join(self._conn_timeout)
            if t.isAlive() or not self.checkConnection():
                raise Exception("连接超时")
        except Exception as e:
            self.dbException = str(e)
            self.db = None
            return

        self.createDB(self.info['dbname'])

    def checkConnection(self):
        return True if self.db else False
    
    def refreshConnection(self):
        self.initConnection()

    def createDB(self, dbName):
        sql = "CREATE DATABASE IF NOT EXISTS " + dbName + " DEFAULT CHARACTER SET utf8;"
        try:
            t = threading.Thread(target=self.dbOperation_threading, args=(sql,))
            t.start()
            t.join(self._conn_timeout)
            if t.isAlive() or not self.checkConnection():
                raise Exception("连接超时")
        except Exception as e:
            self.dbException = str(e)
            self.db = None
            return

        if self.db:
            self.db.close()
            try:
                t = threading.Thread(target=self.setupConnectionThread_db)
                t.start()
                t.join(self._conn_timeout)
                if t.isAlive() or not self.checkConnection():
                    raise Exception("连接超时")
            except Exception as e:
                self.dbException = str(e)
                self.db = None
                return
            self.initDB()

    def initDB(self):
        ptr = self.db.cursor()
        tableConfig = databaseTableConfig()
        sql = tableConfig.getTables()
        try:
            for sentence in sql:
                ptr.execute(sentence)
        except Exception as e:
            #print(e)
            self.dbException = str(e)
            self.db.rollback()

    def resetDB(self):
        try:
            ptr = self.db.cursor()
            sql = """
                    DROP DATABASE %s;
                  """ % (self.info["dbname"])
            ptr.execute(sql)
            self.createDB(self.info["dbname"])
        except Exception as e:
            self.db.rollback()
            print(e)
            return False
        return True

    def searchWithKeyword(self):
        companyList = []
        try:
            ptr = self.db.cursor()
            sql = "SELECT company FROM info order by company;"
            ptr.execute(sql)
            results = ptr.fetchall()
            for row in results:
                companyList.append(row[0])
        except Exception as e:
            #print(e)
            self.dbException = str(e)
        return companyList

    def searchById(self, id):
        id = id.replace("\\",'\\\\').replace("'","\\'").replace('"','\\"')
        ptr = self.db.cursor()
        sql0 = """
               SELECT *
               FROM info
               WHERE company = '%s';
               """ % (id)
        sql1 = """
               SELECT name, leader, operator, level, intro, func
               FROM department
               WHERE refId = '%s'
               ORDER BY seq;
               """ % (id)
        sql2 = """
               SELECT logopath
               FROM logoStore
               WHERE refId = '%s';
               """ % (id)
        sql3 = """
               SELECT projectInfo.*, serviceProcess.*
               FROM projectInfo left join serviceProcess on (projectInfo.AprojectName = serviceProcess.refAprojectName 
               and projectInfo.refId = serviceProcess.refId)
               WHERE projectInfo.refId = '%s'
               ORDER BY projectInfo.seq;
               """ % (id)
        sql4 = """
               SELECT *
               FROM organization
               WHERE organization.refId = '%s';
               """ % (id)

        info = userInfo()
        try:
            ptr.execute(sql0)
            results = ptr.fetchall()
            for row in results:
                info.fileName = row[0]
                info.company = row[1]
                info.address = row[2]
                info.introduction = row[3].split("#")
                info.coverField = row[4]
                info.corporateRepresentative = row[5]
                info.manager = row[6]
                info.guandai = row[7]
                info.compiler = row[8]
                info.approver = row[9]
                info.audit = row[10]
                info.announcer = row[11]
                info.releaseDate = row[12]
                info.auditDate = row[13]
                info.zip = row[14]
                info.phone = row[15]
                info.policy = row[16]
                info.picPath = row[17]
                info.depStruct = row[18]
                info.color = row[19]
        except Exception as e:
            print("Search Info Error:",e)
            self.dbException = str(e)
        try:
            ptr.execute(sql1)
            results = ptr.fetchall()
            info.departments = []
            for row in results:
                dep = {}
                dep["name"] = row[0]
                dep["leader"] = row[1]
                dep["operator"] = row[2]
                dep["level"] = int(row[3])
                dep["intro"] = row[4].split("#")
                dep["func"] = self.formatFunc(list(filter(lambda x: x != '', row[5].split("#"))), "int")
                dep["func"].sort()
                info.departments.append(dep)
        except Exception as e:
            print("Search Department Error:", e)
            self.dbException = str(e)
        try:
            ptr.execute(sql2)
            results = ptr.fetchall()
            for row in results:
                info.logoPath = row[0]
        except Exception as e:
            print("Search Logo Error:", e)
            self.dbException = str(e)

        try:
            ptr.execute(sql3)
            results = ptr.fetchall()
            for row in results:
                project = Project()
                firstIndex = 1
                try:
                    project.BasicInfo.PartyA.projectName = row[firstIndex + 0]
                    project.BasicInfo.PartyA.company = row[firstIndex + 1]
                    project.BasicInfo.PartyA.name = row[firstIndex + 2]
                    project.BasicInfo.PartyA.phone = row[firstIndex + 3]
                    project.BasicInfo.PartyA.address = row[firstIndex + 4]
                    project.BasicInfo.PartyB.contactName = row[firstIndex + 5]
                    project.BasicInfo.PartyB.serviceName = row[firstIndex + 6]
                    project.BasicInfo.PartyB.serviceMail = row[firstIndex + 7]
                    project.BasicInfo.PartyB.servicePhone = row[firstIndex + 8]
                    project.BasicInfo.PartyB.complainName = row[firstIndex + 9]
                    project.BasicInfo.PartyB.complainMail = row[firstIndex + 10]
                    project.BasicInfo.PartyB.complainPhone = row[firstIndex + 11]
                    project.BasicInfo.Detail.amount = row[firstIndex + 12]
                    project.BasicInfo.Detail.period = row[firstIndex + 13]
                    project.BasicInfo.Detail.config = row[firstIndex + 14].split("#")
                    project.BasicInfo.Detail.name = row[firstIndex + 15]
                    project.BasicInfo.Detail.level = row[firstIndex + 16]
                    project.BasicInfo.Detail.details = row[firstIndex + 17].split("#")
                    project.BasicInfo.Detail.demand = row[firstIndex + 18].split("#")
                    project.BasicInfo.Detail.ddl = row[firstIndex + 19]
                    project.BasicInfo.Team.startTime = row[firstIndex + 20]
                    project.BasicInfo.Team.require = row[firstIndex + 21]
                    project.BasicInfo.Team.PM = row[firstIndex + 22]
                    project.BasicInfo.Team.TM = row[firstIndex + 23]
                    # 24,25,26跳过
                    project.ServiceProcess.Report.time = row[firstIndex+27]
                    project.ServiceProcess.Report.keypoint = row[firstIndex+28]
                    project.ServiceProcess.Report.revisit = row[firstIndex+29]
                    project.ServiceProcess.Event.eventManager = row[firstIndex+30]
                    project.ServiceProcess.Event.issueManager = row[firstIndex+31]
                    project.ServiceProcess.Event.S1 = row[firstIndex+32]
                    project.ServiceProcess.Event.S2 = row[firstIndex + 33]
                    project.ServiceProcess.Event.S3 = row[firstIndex + 34]
                    project.ServiceProcess.Event.S4 = row[firstIndex + 35]
                    project.ServiceProcess.Event.closed = row[firstIndex+36]
                    project.ServiceProcess.Event.transformed = row[firstIndex+37]
                    project.ServiceProcess.Event.summarized = row[firstIndex+38]
                    project.ServiceProcess.Config.modifyManager = row[firstIndex+39]
                    project.ServiceProcess.Config.configManager = row[firstIndex+40]
                    project.ServiceProcess.Config.releaseManager = row[firstIndex+41]
                    project.ServiceProcess.Config.relatedManager = row[firstIndex+42]
                    project.ServiceProcess.Config.configVersion = row[firstIndex+43]
                    project.ServiceProcess.Config.configReleaseDate = row[firstIndex+44]
                    project.ServiceProcess.Config.changes = row[firstIndex+45]
                    project.ServiceProcess.Config.releases = row[firstIndex+46]
                    project.ServiceProcess.Config.releaseDate = row[firstIndex+47]
                    project.ServiceProcess.Config.preReleaseDate = row[firstIndex+48]
                    project.ServiceProcess.Config.applicationDate = row[firstIndex+49]
                    project.ServiceProcess.Config.SN = row[firstIndex+50]
                    project.ServiceProcess.Config.target = row[firstIndex+51]
                    project.ServiceProcess.Config.item = row[firstIndex+52]
                    project.ServiceProcess.Config.releaseVersion = row[firstIndex+53]
                    project.ServiceProcess.Config.subject = row[firstIndex + 54]
                    project.ServiceProcess.Continuity.process = row[firstIndex+55].split("#")
                    project.ServiceProcess.Continuity.result = row[firstIndex+56].split("#")
                    project.ServiceProcess.Continuity.date = row[firstIndex+57]
                    project.ServiceProcess.Continuity.technicist = row[firstIndex+58]
                    project.ServiceProcess.Continuity.approver = row[firstIndex+59]
                    project.ServiceProcess.Continuity.compileDate = row[firstIndex+60]
                    project.ServiceProcess.Continuity.auditDate = row[firstIndex+61]
                except Exception as e:
                    print("Get Project Error:",e)
                    continue
                info.projects.append(project)
        except Exception as e1:
            print("Search Project Error:", e1)
            self.dbException = str(e1)
        
        try:
            ptr.execute(sql4)
            results = ptr.fetchall()
            organization = Organization()
            firstIndex = 1
            for row in results:
                organization.Audit.planDate = row[firstIndex+0]
                organization.Audit.auditDate = row[firstIndex+1]
                organization.Audit.auditLeader = row[firstIndex+2]
                organization.Audit.audit1 = row[firstIndex+3]
                organization.Audit.audit2 = row[firstIndex+4]
                organization.Audit.audit3 = row[firstIndex+5]
                organization.Audit.reviewDate = row[firstIndex+6]
                organization.Audit.scheduleDate = row[firstIndex+7]
                organization.Audit.excuteDate = row[firstIndex+8]
                organization.Audit.reportDate = row[firstIndex+9]
                organization.Audit.compiler = row[firstIndex+10]
                organization.Audit.audit = row[firstIndex+11]
                organization.Audit.compileDate = row[firstIndex+12]
                organization.Audit.approveDate = row[firstIndex+13]
                organization.Record.target = row[firstIndex+14]
                organization.Record.time = row[firstIndex+15]
                organization.Record.staff = row[firstIndex+16]
                organization.Record.arrange = row[firstIndex+17].split("#")
                organization.Record.content = row[firstIndex+18].split("#")
                organization.Record.fileName = row[firstIndex+19]
                organization.Record.auditContent = row[firstIndex+20].split("#")
                organization.Record.auditProcess = row[firstIndex+21].split("#")
                organization.Record.audit = row[firstIndex+22]
                organization.Record.auditDate = row[firstIndex+23]
                organization.Record.approver = row[firstIndex+24]
                organization.Record.approveDate = row[firstIndex+25]
                organization.Record.provider= row[firstIndex+26]
            info.organization = organization
        except Exception as e:
            print("Search Organization Error:", e)
            self.dbException = str(e)
        # 测试语句
        # with open("projectOutTest.json", "w") as f:
        #     json.dump(info.projects[0].Info, f, indent=4)
        return info

    def insertData(self, user):
        #防注入
        data = userInfo()
        attrDict = vars( user )
        for attr in attrDict:
            setattr( data , attr , getattr(user,attr) )
        data.fileName = data.fileName.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.company = data.company.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.address = data.address.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.coverField = data.coverField.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.corporateRepresentative = data.corporateRepresentative.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.manager = data.manager.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.guandai = data.guandai.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.compiler = data.compiler.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.approver = data.approver.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.audit = data.audit.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.announcer = data.announcer.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.zip = data.zip.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.phone = data.phone.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
        data.policy = data.policy.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')

        # 公司基础信息
        ptr = self.db.cursor()
        sql0 =  """
                INSERT INTO info(
                    id, company, address, introduction, coverField,
                    corporate, manager, guanDai, compiler, approver,
                    audit, announcer, releaseDate, auditDate, zip,
                    phone, policy, picPath, depStruct, color
                )VALUES('%s', '%s', '%s', '%s', '%s', 
                        '%s', '%s', '%s', '%s', '%s', 
                        '%s', '%s', '%s', '%s', '%s', 
                        '%s', '%s', '%s', '%s', '%s');
                """ % (data.fileName, data.company, data.address,
                       "#".join(data.introduction).replace('\\','\\\\').replace("'","\\'").replace('"','\\"'), 
                       data.coverField, data.corporateRepresentative, data.manager,
                       data.guandai, data.compiler, data.approver,
                       data.audit, data.announcer, data.releaseDate, 
                       data.auditDate, data.zip, data.phone, data.policy,
                       data.picPath, data.depStruct, data.color)
        try:
           ptr.execute(sql0)
           self.db.commit()
        except Exception as e:
           self.db.rollback()
           print(e)
           self.dbException = str(e)
           return False

        try:
            ptr.execute("INSERT INTO logoStore(refId,logopath) VALUES('%s','%s');" % (data.company, data.logoPath))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.dbException = str(e)
            return False

        # 公司部门信息
        seq = 0
        sql1 = """
                INSERT INTO department(
                    refId, name, leader, operator, level,
                    intro, func, seq
                ) VALUES
               """
        depNum = len(data.departments)
        for department in data.departments:
            sql1 += "('%s', '%s', '%s', '%s', %s, '%s', '%s', %d)"\
                    % (data.company, department['name'],
                       department["leader"], department["operator"],
                       str(department["level"]), "#".join(department["intro"]),
                       "#".join(self.formatFunc(department["func"])), seq)
            if seq < depNum-1:
                sql1 += ","
            else:
                sql1 += ";"
            seq += 1

        try:
            ptr.execute(sql1)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.dbException = str(e)
            return False

        # 公司项目信息
        seq = 0
        for project in data.projects:
            sql2 = """
                INSERT INTO projectInfo(
                    refId, AprojectName, Acompany, Aname, Aphone, 
                    Aaddress, BcontactName, BserviceName, BserviceMail, BservicePhone, 
                    BcomplainName, BcomplainMail, BcomplainPhone, Damount, Dperiod, 
                    Dconfig, Dname, Dlevel, Ddetails, Ddemand,
                    Dddl, TstartTime, Trequire, TPM, TTM, seq
                ) VALUES (
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                  %d );
               """ % (data.company,
                      project.BasicInfo.PartyA.projectName, 
                      project.BasicInfo.PartyA.company,
                      project.BasicInfo.PartyA.name,
                      project.BasicInfo.PartyA.phone,
                      project.BasicInfo.PartyA.address,
                      project.BasicInfo.PartyB.contactName,
                      project.BasicInfo.PartyB.serviceName,
                      project.BasicInfo.PartyB.serviceMail,
                      project.BasicInfo.PartyB.servicePhone,
                      project.BasicInfo.PartyB.complainName,
                      project.BasicInfo.PartyB.complainMail,
                      project.BasicInfo.PartyB.complainPhone,
                      project.BasicInfo.Detail.amount,
                      project.BasicInfo.Detail.period,
                      "#".join(project.BasicInfo.Detail.config),
                      project.BasicInfo.Detail.name,
                      project.BasicInfo.Detail.level,
                      "#".join(project.BasicInfo.Detail.details),
                      "#".join(project.BasicInfo.Detail.demand),
                      project.BasicInfo.Detail.ddl,
                      project.BasicInfo.Team.startTime,
                      project.BasicInfo.Team.require,
                      project.BasicInfo.Team.PM,
                      project.BasicInfo.Team.TM,
                      seq)

            sql3 = """
                INSERT INTO serviceProcess(
                    refId, refAprojectName, RepTime, RepKeypoint, RepRevisit,
                    EveEventManager, EveIssueManager, EveS1, EveS2, EveS3, EveS4, EveClosed,
                    EveTransformed, EveSummarized, CofModifyManager, CofConfigManager, CofReleaseManager,
                    CofRelatedManager, CofConfigVersion, CofConfigReleaseDate, CofChanges, CofReleases,
                    CofReleaseDate, CofPreReleaseDate, CofApplicationDate, CofSN, CofTarget,
                    CofItem, CofReleaseVersion, CofSubject, CotProcess, CotResult, CotDate,
                    CotTechnicist, CotApprover, CotCompileDate, CotAuditDate
                ) VALUES (
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s',  %d ,  %d ,  %d , %d ,  %d ,
                  %d ,  %d , '%s', '%s', '%s',
                 '%s', '%s', '%s',  %d ,  %d ,
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s');
               """ % (data.company,
                      project.BasicInfo.PartyA.projectName, 
                      project.ServiceProcess.Report.time,
                      project.ServiceProcess.Report.keypoint,
                      project.ServiceProcess.Report.revisit,
                      project.ServiceProcess.Event.eventManager,
                      project.ServiceProcess.Event.issueManager,
                      project.ServiceProcess.Event.S1,
                      project.ServiceProcess.Event.S2,
                      project.ServiceProcess.Event.S3,
                      project.ServiceProcess.Event.S4,
                      project.ServiceProcess.Event.closed,
                      project.ServiceProcess.Event.transformed,
                      project.ServiceProcess.Event.summarized,
                      project.ServiceProcess.Config.modifyManager,
                      project.ServiceProcess.Config.configManager,
                      project.ServiceProcess.Config.releaseManager,
                      project.ServiceProcess.Config.relatedManager,
                      project.ServiceProcess.Config.configVersion,
                      project.ServiceProcess.Config.configReleaseDate,
                      project.ServiceProcess.Config.changes,
                      project.ServiceProcess.Config.releases,
                      project.ServiceProcess.Config.releaseDate,
                      project.ServiceProcess.Config.preReleaseDate,
                      project.ServiceProcess.Config.applicationDate,
                      project.ServiceProcess.Config.SN,
                      project.ServiceProcess.Config.target,
                      project.ServiceProcess.Config.item,
                      project.ServiceProcess.Config.releaseVersion,
                      project.ServiceProcess.Config.subject,
                      "#".join(project.ServiceProcess.Continuity.process),
                      "#".join(project.ServiceProcess.Continuity.result),
                      project.ServiceProcess.Continuity.date,
                      project.ServiceProcess.Continuity.technicist,
                      project.ServiceProcess.Continuity.approver,
                      project.ServiceProcess.Continuity.compileDate,
                      project.ServiceProcess.Continuity.auditDate)
            try:
                ptr.execute(sql2)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                self.dbException = str(e)
                return False
            try:
                ptr.execute(sql3)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                self.dbException = str(e)
                return False
            seq += 1
        
        sql4 = """
                INSERT INTO organization(
                    refId, AudPlanDate,
                    AudAuditDate, AudAuditLeader, AudAudit1, AudAudit2, AudAudit3,
                    AudReviewDate, AudScheduleDate, AudExcuteDate, AudReportDate, AudCompiler,
                    AudAudit, AudCompileDate, AudApproveDate, RecTarget, RecTime,
                    RecStaff, RecArrange, RecContent, RecFileName, RecAuditContent,
                    RecAuditProcess, RecAudit, RecAuditDate, RecApprover, RecApproveDate,
                    RecProvider
                ) VALUES (
                 '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s');
               """ % (data.company,
                      data.organization.Audit.planDate,
                      data.organization.Audit.auditDate,
                      data.organization.Audit.auditLeader,
                      data.organization.Audit.audit1,
                      data.organization.Audit.audit2,
                      data.organization.Audit.audit3,
                      data.organization.Audit.reviewDate,
                      data.organization.Audit.scheduleDate,
                      data.organization.Audit.excuteDate,
                      data.organization.Audit.reportDate,
                      data.organization.Audit.compiler,
                      data.organization.Audit.audit,
                      data.organization.Audit.compileDate,
                      data.organization.Audit.approveDate,
                      data.organization.Record.target,
                      data.organization.Record.time,
                      data.organization.Record.staff,
                      "#".join(data.organization.Record.arrange),
                      "#".join(data.organization.Record.content),
                      data.organization.Record.fileName,
                      "#".join(data.organization.Record.auditContent),
                      "#".join(data.organization.Record.auditProcess),
                      data.organization.Record.audit,
                      data.organization.Record.auditDate,
                      data.organization.Record.approver,
                      data.organization.Record.approveDate,
                      data.organization.Record.provider)
        try:
            ptr.execute(sql4)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.dbException = str(e)
            return False
        return True

    def update(self, table, option_data):
        if table not in ["info", "department"] or not option_data:
            return False
        if not option_data.__contains__("company") and not option_data.__contains__("refId"):
            return False
        if option_data.__contains__("refId") and not option_data.__contains__("name"):
            return False

        options = list(option_data.keys())
        #print(options)
        sql = "UPDATE " + table + " SET "
        
        if table == "info":
            # info表
            pos = "company = '%s'" % (option_data["company"])
            options.remove("company")
            for i in range(0, len(options)):
                if options[i] == "introduction":
                    sql = sql + options[i] + " = '%s'" % ("#".join(option_data[options[i]]))
                else:
                    sql = sql + options[i] + " = '%s'" % (option_data[options[i]])
                if i < len(options)-1:
                    sql = sql + ", "
            sql = sql + " WHERE " + pos
        else:
            # department表
            pos = "refId = '%s' and name = '%s'" % (option_data["refId"], option_data["name"])
            options.remove("refId")
            options.remove("name")
            for i in range(0, len(options)):
                if options[i] == "level":
                    sql = sql + options[i] + " = %s" % (option_data[options[i]])
                else:
                    sql = sql + options[i] + " = '%s'" % ("#".join(self.formatFunc(option_data[options[i]])))
                if i < len(options)-1:
                    sql = sql + ", "
            sql = sql + " WHERE " + pos
        
        print(sql)
        ptr = self.db.cursor()
        try:
            ptr.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            #print(e)
            self.dbException = str(e)
            return False
        return True

    def delete(self, table, id, option = None):
        ptr = self.db.cursor()
        if table not in ["info", "department", "projectInfo"]:
            return False
        sql = ""
        if table == "info":
            sql = "DELETE FROM %s WHERE company = '%s';" % (table, id)
        elif table == "department":
            if option:
                sql = "DELETE FROM %s WHERE refId = '%s' and name = '%s';" % (table, id, option)
        else:
            if option:
                sql = "DELETE FROM %s WHERE Acompany = '%s' and AprojectName = '%s';" % (table, id, option)
            else:
                sql = "DELETE FROM %s WHERE refId = '%s';" % (table, id)
        try:
            ptr.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            #print(e)
            self.dbException = str(e)
            return False
        return True

    def formatFunc(self, func, mode="str"):
        if not func or len(func) == 0:
            return func
        funcList = func[:]
        for i in range(len(funcList)):
            if mode == "str":
                funcList[i] = funcList[i] if type(funcList[i]) == "str" else str(funcList[i])
            else:
                funcList[i] = funcList[i] if type(funcList[i]) == "int" else int(funcList[i])
        return funcList

    def loadConfig(self):
        with open("./config/dbConfig.json", "r") as f:
            data = json.load(f)
        return data

    def writeConfig(self, input = None):
        data = input or { 'ip' : 'localhost', 'user' : 'root', 'pswd' : '1234', 'dbname' : 'wordStore', 'port': 3306}
        with open("./config/dbConfig.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
        return data

    def resetConfig(self):
        self.writeConfig()

