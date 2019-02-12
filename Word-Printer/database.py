# -*- coding: utf-8 -*-
import pymysql
import json
import sys

from dataStruct import userInfo

class DB:
    def __init__(self):
        self.info = self.loadConfig()
        print(self.info)
        try:
            self.db = pymysql.connect(host=self.info['ip'], user=self.info['user'], password=self.info['pswd'], port=self.info['port'])
        except Exception as e:
            print(e)
        self.createDB(self.info['dbname'])

    def __del__(self):
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
                   coverField NVARCHAR(100) NOT NULL,
                   manager NVARCHAR(20) NOT NULL,
                   guanDai NVARCHAR(20) NOT NULL,
                   employees NVARCHAR(20) NOT NULL,
                   approver NVARCHAR(20) NOT NULL,
                   releaseDate NVARCHAR(20),
                   auditDate NVARCHAR(20),
                   PRIMARY KEY (id)
               ) ENGINE=InnoDB;
               """,
               """
               CREATE TABLE IF NOT EXISTS department( 
                   refId NVARCHAR(20) NOT NULL,
                   name NVARCHAR(20) NOT NULL,
                   duty NVARCHAR(1500) NOT NULL,
                   resposibility NVARCHAR(200) NOT NULL,
                   PRIMARY KEY (refId, name),
                   FOREIGN KEY (refId) REFERENCES info(id) ON UPDATE CASCADE ON DELETE CASCADE
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
               WHERE id = %s;
               """ % (id)
        sql1 = """
               SELECT (name, duty, resposibility)
               FROM department
               WHERE refId = %s;
               """ % (id)
   
        info = userInfo();
        try:
            ptr.execute(sql0)
            results = ptr.fetchall()
            for row in results:
                info.fileName = row[0]
                info.company = row[1]
                info.address = row[2]
                info.introduction = row[3]
                info.coverField = row[4].split("#")
                info.manager = row[5]
                info.guandai = row[6]
                info.employees = row[7]
                info.approver = row[8]
                info.releaseDate = row[9]
                info.auditDate = row[10]        
        except Exception as e:
            print(e)

        try:
            ptr.execute(sql1)
            results = ptr.fetchall()
            for row in results:
                dep = [rows[0]]
                dep.append(row[1].split("#"))
                dep.append(row[2].split("#"))
                info.departments.append(dep)
        except Exception as e:
            print(e)
        
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
                    releaseDate,
                    auditDate
                )VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                """ % (data.fileName, data.company, data.address,
                       "#".join(data.introduction), "#".join(data.coverField), data.manager,
                       data.guandai, data.employees, data.approver,
                       data.releaseDate, data.auditDate)
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
                        duty,
                        resposibility
                    )VALUES('%s', '%s', '%s', '%s');
                    """ % (data.fileName, department[0], "#".join(department[1]), "#".join(department[2]))
            
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
        if not option_data.__contains__("id") and not option_data.__contains__("refId"):
            return False
        if option_data.__contains__("refId") and not option_data.__contains__("name"):
            return False

        options = list(option_data.keys())
        print(options)
        sql = "UPDATE " + table + " SET "
        if table == "info":
            pos = "id = '%s'" % (option_data["id"])
            options.remove("id")
            for i in range(0, len(options)):
                sql = sql + options[i] + " = '%s'" % (option_data[options[i]])
                if i < len(options)-1:
                    sql = sql + ", "
            sql = sql + " WHERE " + pos
        else:
            # not test
            pos = "refId = '%s' and name = '%s'" % (option_data["refId"], option_data["name"])
            options.remove("refId")
            options.remove("name")
            for i in range(0, len(options)):
                sql = sql + options[i] + " = '%s'" % (option_data[options[i]])
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

    def delete(self, id):
        ptr = self.db.cursor()

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

