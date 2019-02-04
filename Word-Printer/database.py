# -*- coding: utf-8 -*-
import pymysql
import json

class DB:
    def __init__(self):
        self.info = self.loadConfig()
        print(self.info)
        self.db = pymysql.connect(self.info['ip'], self.info['user'], self.info['pswd'], self.info['dbname'])
        self.search()

    def __del__(self):
        self.db.close()

    def loadConfig(self):
        with open("dbConfig.json", "r") as f:
            data = json.load(f)
        return data

    def writeConfig(self):
        data = { 'ip' : 'localhost', 'user' : 'root', 'pswd' : '1234', 'dbname' : 'wordStore'}
        with open("dbConfig.json", "w") as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
        return data

    def resetConfig(self):
        self.writeConfig()

    def search(self):
        ptr = self.db.cursor()
        sql = "SELECT * FROM client"
        try:
            ptr.execute(sql)
            results = ptr.fetchall()
            for row in results:
                print(row)
        except:
            print("error")
        self.db.close()
