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

    def __init__(self):
        self.initConnection()

    def __del__(self):
        if self.db:
            self.db.close()

    def initConnection(self):
        self.info = self.loadConfig()
        try:
            self.db = pymysql.connect(host=self.info['ip'], user=self.info['user'], password=self.info['pswd'], port=self.info['port'])
        except Exception as e:
            self.db = None
            self.dbException = str(e)
        else:
            self.createDB(self.info['dbname'])

    def checkConnection(self):
        return True if self.db else False
    
    def refreshConnection(self):
        #if self.db:
        #    self.db.close()
        self.initConnection()

    def createDB(self, dbName):
        ptr = self.db.cursor()
        try:
            sql = "CREATE DATABASE IF NOT EXISTS " + dbName + " DEFAULT CHARACTER SET utf8;"
            ptr.execute(sql)
        except Exception as e:
            #print(e)
            self.dbException = str(e)
            self.db.rollback()
        self.db.close()
        try:
            self.db = pymysql.connect(host=self.info['ip'], user=self.info['user'], password=self.info['pswd'], database=self.info['dbname'], port=self.info['port'])
        except Exception as e:
            #print(e)
            self.dbException = str(e)
            self.db = None
        else:
            #print("SUCCESS: Create database -> " + dbName)
            self.initDB()

    def initDB(self):
        ptr = self.db.cursor()
        sql = ["""
               CREATE TABLE IF NOT EXISTS info( 
                   id NVARCHAR(20) NOT NULL, 
                   company NVARCHAR(100) NOT NULL,
                   address NVARCHAR(100) NOT NULL,
                   introduction NVARCHAR(1000) NOT NULL,
                   coverField NVARCHAR(1000) NOT NULL,
                   corporate NVARCHAR(20) NOT NULL,
                   manager NVARCHAR(20) NOT NULL,
                   guanDai NVARCHAR(20) NOT NULL,
                   compiler NVARCHAR(20) NOT NULL,
                   approver NVARCHAR(20) NOT NULL,
                   audit NVARCHAR(20) NOT NULL,
                   announcer NVARCHAR(20) NOT NULL,
                   releaseDate NVARCHAR(20) NOT NULL,
                   auditDate NVARCHAR(20) NOT NULL,
                   zip NVARCHAR(6) NOT NULL,
                   phone NVARCHAR(20) NOT NULL,
                   policy NVARCHAR(200) NOT NULL,
                   picPath NVARCHAR(200) NOT NULL,
                   depStruct NVARCHAR(1000) NOT NULL,
                   color NVARCHAR(1000) NOT NULL,
                   PRIMARY KEY (company)
               ) ENGINE=InnoDB;
               """,
               """
               CREATE TABLE IF NOT EXISTS department( 
                   refId NVARCHAR(100) NOT NULL,
                   level INT(1) NOT NULL DEFAULT 0,
                   name NVARCHAR(20) NOT NULL,
                   leader NVARCHAR(20) NOT NULL,
                   operator NVARCHAR(20) NOT NULL,
                   intro NVARCHAR(1500) NOT NULL,
                   func NVARCHAR(200) NOT NULL,
                   seq INT(5) NOT NULL,
                   PRIMARY KEY (refId, name),
                   FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
               ) ENGINE=InnoDB;
               """,
               """
               CREATE TABLE IF NOT EXISTS logoStore( 
                   refId NVARCHAR(100) NOT NULL,
                   logopath NVARCHAR(200),
                   photo MEDIUMBLOB DEFAULT NULL,
                   PRIMARY KEY (refId),
                   FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
               ) ENGINE=InnoDB;
               """]
        try:
            for sentence in sql:
                ptr.execute(sentence)
        except Exception as e:
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

        #
        ptr = self.db.cursor()
        sql0 =  """
                INSERT INTO info(
                    id, 
                    company,
                    address,
                    introduction,
                    coverField,
                    corporate,
                    manager,
                    guanDai,
                    compiler,
                    approver,
                    audit,
                    announcer,
                    releaseDate,
                    auditDate,
                    zip,
                    phone,
                    policy,
                    picPath,
                    depStruct,
                    color
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

        seq = 0
        for department in data.departments:
            seq += 1
            sql1 =  """
                    INSERT INTO department(
                        refId, 
                        name,
                        leader,
                        operator,
                        level,
                        intro,
                        func,
                        seq
                    )VALUES('%s', '%s', '%s', '%s', %s, '%s', '%s', %d);
                    """ % (data.company, department['name'], 
                           department["leader"], department["operator"],
                           str(department["level"]), "#".join(department["intro"]), 
                           "#".join(self.formatFunc(department["func"])), seq)
            
            try:
               ptr.execute(sql1)
               self.db.commit()
            except Exception as e:
               self.db.rollback()
               #print(e)
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

