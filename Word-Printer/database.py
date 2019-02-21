# -*- coding: utf-8 -*-
import pymysql
import json
import sys

from dataStruct import userInfo

class DB:
    def __init__(self):
        self.info = self.loadConfig()
        #print(self.info)
        try:
            self.db = pymysql.connect(host=self.info['ip'], user=self.info['user'], password=self.info['pswd'], port=self.info['port'])
        except Exception as e:
            print(e)
        else:
            self.createDB(self.info['dbname'])

    def __del__(self):
        if self.db:
            self.db.close()

    def createDB(self, dbName):
        ptr = self.db.cursor()
        try:
            sql = "CREATE DATABASE IF NOT EXISTS " + dbName + " DEFAULT CHARACTER SET utf8;"
            ptr.execute(sql)
        except Exception as e:
            print(e)
            self.db.rollback()
        self.db.close()
        try:
            self.db = pymysql.connect(host=self.info['ip'], user=self.info['user'], password=self.info['pswd'], database=self.info['dbname'], port=self.info['port'])
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("SUCCESS: Create database -> " + dbName)
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
                   manager NVARCHAR(20) NOT NULL,
                   guanDai NVARCHAR(20) NOT NULL,
                   employees NVARCHAR(20) NOT NULL,
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
                   intro NVARCHAR(1500) NOT NULL,
                   func NVARCHAR(200) NOT NULL,
                   PRIMARY KEY (refId, name),
                   FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
               ) ENGINE=InnoDB;
               """]
        try:
            ptr.execute(sql[0])
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("SUCCESS: Create table -> info")
        try:
            ptr.execute(sql[1])
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("SUCCESS: Create table -> department")

    def search(self):
        ptr = self.db.cursor()
        sql = "SELECT * FROM client"
        try:
            ptr.execute(sql)
            results = ptr.fetchall()
            for row in results:
                print(row)
        except Exception as e:
            print(e)

    def searchById(self, id):
        ptr = self.db.cursor()
        sql0 = """
               SELECT *
               FROM info
               WHERE company = '%s';
               """ % (id)
        sql1 = """
               SELECT name, level, intro, func
               FROM department
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
                info.manager = row[5]
                info.guandai = row[6]
                info.employees = row[7]
                info.approver = row[8]
                info.audit = row[9]
                info.announcer = row[10]
                info.releaseDate = row[11]
                info.auditDate = row[12]
                info.zip = row[13]
                info.phone = row[14]
                info.policy = row[15]
                info.picPath = row[16]
                info.depStruct = row[17]
                info.color = row[18]
        except Exception as e:
            print("Search Info Error:",e)

        try:
            ptr.execute(sql1)
            results = ptr.fetchall()
            info.departments = []
            for row in results:
                dep = {}
                dep["name"] = row[0]
                dep["level"] = int(row[1])
                dep["intro"] = row[2].split("#")
                dep["func"] = self.formatFunc(list(filter(lambda x: x != '', row[3].split("#"))), "int")
                info.departments.append(dep)
        except Exception as e:
            print("Search Department Error:", e)
        
        return info

    def insertData(self, data):
        ptr = self.db.cursor()
        sql0 =  """
                INSERT INTO info(
                    id, 
                    company,
                    address,
                    introduction,
                    coverField,
                    manager,
                    guanDai,
                    employees,
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
                        '%s', '%s', '%s', '%s');
                """ % (data.fileName, data.company, data.address,
                       "#".join(data.introduction), data.coverField, data.manager,
                       data.guandai, data.employees, data.approver,
                       data.audit, data.announcer, data.releaseDate, 
                       data.auditDate, data.zip, data.phone, data.policy,
                       data.picPath, data.depStruct, data.color)
        try:
           ptr.execute(sql0)
           self.db.commit()
        except Exception as e:
           self.db.rollback()
           print(e)
           return False

        for department in data.departments:
            
            sql1 =  """
                    INSERT INTO department(
                        refId, 
                        name,
                        level,
                        intro,
                        func
                    )VALUES('%s', '%s', %s, '%s', '%s');
                    """ % (data.company, department['name'], str(department["level"]), "#".join(department["intro"]), "#".join(self.formatFunc(department["func"])))
            
            try:
               ptr.execute(sql1)
               self.db.commit()
            except Exception as e:
               self.db.rollback()
               print(e)
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
            print(e)
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
            print(e)
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
        with open("dbConfig.json", "r") as f:
            data = json.load(f)
        return data

    def writeConfig(self):
        data = { 'ip' : 'localhost', 'user' : 'root', 'pswd' : '1234', 'dbname' : 'wordStore', 'port': 3306}
        with open("dbConfig.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
        return data

    def resetConfig(self):
        self.writeConfig()

