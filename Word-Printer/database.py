# -*- coding: utf-8 -*-
from MainUI import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

import pymysql
import json
import sys

from dataStruct import userInfo
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

    def initConnection(self):
        self.info = self.loadConfig()
        try:
            t = threading.Thread(target=self.setupConnectionThread_host)
            t.start()
            t.join(5)
            if t.isAlive() or not self.checkConnection():
                raise Exception(self.dbException)
        except Exception as e:
            self.db = None
            return

        self.createDB(self.info['dbname'])

    def checkConnection(self):
        return True if self.db else False
    
    def refreshConnection(self):
        self.initConnection()

    def createDB(self, dbName):
        try:
            ptr = self.db.cursor()
            sql = "CREATE DATABASE IF NOT EXISTS " + dbName + " DEFAULT CHARACTER SET utf8;"
            ptr.execute(sql)
        except Exception as e:
            print(e)
            self.dbException = str(e)
            self.db.rollback()
        self.db.close()
        try:
            t = threading.Thread(target=self.setupConnectionThread_db)
            t.start()
            t.join(5)
            if t.isAlive() or not self.checkConnection():
                raise Exception(self.dbException)
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

    def searchWithKeyword(self):
        try:
            ptr = self.db.cursor()
            sql = "SELECT company FROM info order by company;"
            companyList = []
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
        info = userInfo();
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
            sql1 += "('%s', '%s', '%s', '%s', %s, '%s', '%s', %d)" \
                    % (data.company, department['name'], \
                       department["leader"], department["operator"],\
                       str(department["level"]), "#".join(department["intro"]),\
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
                    AprojectName, Acompany, Aname, Aphone, Aaddress,
                    BcontactName, BserviceName, BserviceMail, BservicePhone, BcomplainName,
                    BcomplainMail, BcomplainPhone, Damount, Dperiod, Dconfig,
                    Dname, Dlevel, Ddetails, Ddemand, Dddl,
                    TstartTime, Trequire, TPM, TTM, seq
                ) VALUES (
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s',  %d);
               """ % (project.BasicInfo.PartyA.projectName, 
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
                      project.BasicInfo.Detail.config,
                      project.BasicInfo.Detail.name,
                      project.BasicInfo.Detail.level,
                      project.BasicInfo.Detail.details,
                      project.BasicInfo.Detail.demand,
                      project.BasicInfo.Detail.ddl,
                      project.BasicInfo.Team.startTime,
                      project.BasicInfo.Team.require,
                      project.BasicInfo.Team.PM,
                      project.BasicInfo.Team.TM,
                      seq)

            sql3 = """
                INSERT INTO projectInfo(
                    refAprojectName, refAcompany, RepTime, RepKeypoint, RepRevisit,
                    EveEventManager, EveIssueManager, EveLevel, EveAccepted, EveClosed,
                    EveTransformed, EveSummarized, CofModifyManager, CofConfigManager, CofReleaseManager,
                    CofRelatedManager, CofConfigVersion, CofConfigReleaseDate, CofChanges, CofReleases,
                    CofReleaseDate, CofPreReleaseDate, CofApplicationDate, CofSN, CofTarget,
                    CofItem, CofReleaseVersion, CotProcess, CotResult, CotDate,
                    CotTechnicist, CotApprover, CotCompileDate, CotAuditDate, AudPlanDate,
                    AudAuditDate, AudAuditLeader, AudAudit1, AudAudit2, AudAudit3,
                    AudReviewDate, AudScheduleDate, AudExcuteDate, AudReportDate, AudCompiler,
                    AudAudit, AudCompileDate, AudApproveDate, RecTarget, RecTime,
                    RecStaff, RecArrange, RecContent, RecFileName, RecAuditContent,
                    RecAuditProcess, RecAudit, RecAuditDate, RecApprover, RecApproveDate,
                    RecProvider
                ) VALUES (
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s',  %d ,  %d ,
                  %d ,  %d , '%s', '%s', '%s',
                 '%s', '%s', '%s',  %d ,  %d ,
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s', '%s', '%s', '%s', '%s',
                 '%s');
               """ % (project.BasicInfo.PartyA.projectName, 
                      project.BasicInfo.PartyA.company,
                      project.ServiceProcess.Report.time,
                      project.ServiceProcess.Report.keypoint,
                      project.ServiceProcess.Report.revisit,
                      project.ServiceProcess.Event.eventManager,
                      project.ServiceProcess.Event.issueManager,
                      project.ServiceProcess.Event.level,
                      project.ServiceProcess.Event.accepted,
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
                      project.ServiceProcess.Continuity.process,
                      project.ServiceProcess.Continuity.result,
                      project.ServiceProcess.Continuity.date,
                      project.ServiceProcess.Continuity.technicist,
                      project.ServiceProcess.Continuity.approver,
                      project.ServiceProcess.Continuity.compileDate,
                      project.ServiceProcess.Continuity.auditDate,
                      project.ServiceProcess.Audit.planDate,
                      project.ServiceProcess.Audit.auditDate,
                      project.ServiceProcess.Audit.auditLeader,
                      project.ServiceProcess.Audit.audit1,
                      project.ServiceProcess.Audit.audit2,
                      project.ServiceProcess.Audit.audit3,
                      project.ServiceProcess.Audit.reviewDate,
                      project.ServiceProcess.Audit.scheduleDate,
                      project.ServiceProcess.Audit.excuteDate,
                      project.ServiceProcess.Audit.reportDate,
                      project.ServiceProcess.Audit.compiler,
                      project.ServiceProcess.Audit.audit,
                      project.ServiceProcess.Audit.compileDate,
                      project.ServiceProcess.Audit.approveDate,
                      project.ServiceProcess.Record.target,
                      project.ServiceProcess.Record.time,
                      project.ServiceProcess.Record.staff,
                      project.ServiceProcess.Record.arrange,
                      project.ServiceProcess.Record.content,
                      project.ServiceProcess.Record.fileName,
                      project.ServiceProcess.Record.auditContent,
                      project.ServiceProcess.Record.auditProcess,
                      project.ServiceProcess.Record.audit,
                      project.ServiceProcess.Record.auditDate,
                      project.ServiceProcess.Record.approver,
                      project.ServiceProcess.Record.approveDate,
                      project.ServiceProcess.Record.provider)
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

    def delete(self, table, id, department = ""):
        ptr = self.db.cursor()
        if table not in ["info", "department"]:
            return False
        sql = ""
        if table == "info":
            sql = "DELETE FROM %s WHERE company = '%s';" % (table, id)
        else:
            sql = "DELETE FROM %s WHERE refId = '%s' and name = '%s';" % (table, id, department)
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

    def writeConfig(self, input = {}):
        data = input or { 'ip' : 'localhost', 'user' : 'root', 'pswd' : '1234', 'dbname' : 'wordStore', 'port': 3306}
        with open("./config/dbConfig.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
        return data

    def resetConfig(self):
        self.writeConfig()

