from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
import json,os

from replace import Replace
from excel import excel
import xlwt
import re
from dataStruct import userInfo

class docWriter:
    def __init__(self):
        self.saveDir = "./docSave/"

    def __del__(self):
        pass

    def saveAsDocx(self, doc, filepath):
        try:
            doc.save(filepath)
        except Exception as e:
            print(e)

    def saveAsPdf(self, doc):
        pass

    def saveAsExcel( self , xls , dst ):
        try:
            xls.save(dst)
        except Exception as e:
            print(e)

    def loadAndWrite(self, user , templateFile, graphStyle = [], targetFile = ""):
        mode = templateFile.split('.')[-1]
        self.write(templateFile, targetFile if targetFile != "" else user.fileName+'-20000-SM-M-01.docx', user, mode)
        
    def loadInfo(self):
        user = userInfo();
        with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
            for dict in data:
                for key in dict.keys():
                    setattr( user , key , dict[key] )
        return user

    def write(self, src, dst, user, mode="docx"):
        if mode == "docx":
            rep = Replace()
            doc = rep.run(src, dst, user)
            self.saveAsDocx(doc, dst)
        elif mode == "xls":
            xls = excel()
            reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
            prefix = re.search(reg, dst, re.M|re.I).group(1)
            print( prefix )
            xlsx = xls.title( src , dst , str(prefix) )
            self.saveAsExcel( xlsx , dst )

        else:
            self.saveAsPdf(doc, dst)
