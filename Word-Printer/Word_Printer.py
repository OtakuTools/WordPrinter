from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
import json,os

from replace import Replace
from dataStruct import userInfo
from generateGraph import drawGraph

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

    def loadAndWrite(self, user , templateFile, graphStyle = [], targetFile = ""):
        #user = self.loadInfo()
        graph = drawGraph()
        user = graph.draw("save", user, graphStyle)
        self.write(templateFile, targetFile if targetFile != "" else user.fileName+'-20000-SM-M-01.docx', user)
        
    def loadInfo(self):
        user = userInfo();
        with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
            for dict in data:
                for key in dict.keys():
                    setattr( user , key , dict[key] )
        return user

    def write(self, src, dst, user, mode="docx"):
        rep = Replace()
        doc = rep.run(src, dst, user)
        if mode == "docx":
            self.saveAsDocx(doc, dst)
        else:
            self.saveAsPdf(doc, dst)
