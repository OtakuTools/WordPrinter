from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
import json,os
from pathlib import Path
from replace import Replace
from excel import excel
import re
from dataStruct import userInfo
import time

class docWriter:
    def __init__(self):
        self.saveDir = "./docSave/"

    def __del__(self):
        pass

    def saveAsDocx(self, doc, filepath):
        doc.save(filepath)

    def saveAsPdf(self, doc, filepath):
        pass

    def saveAsExcel( self , xls , dst ):
        xls.save(dst)

    def loadAndWrite(self, user , templateFile, targetFile, mode=".docx", projectName=None):
        self.write(templateFile, targetFile, user, mode, projectName)
        
    def loadInfo(self):
        user = userInfo()
        with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
            for dict in data:
                for key in dict.keys():
                    setattr( user , key , dict[key] )
        return user

    def write(self, src, dst, user, mode=".docx", projectName=None):
        try:
            absolutSrcPath = Path(src) if Path(src).is_absolute() else Path.cwd() / Path(src)
            absolutDstPath = Path(dst) if Path(dst).is_absolute() else Path.cwd() / Path(dst)
            if not absolutDstPath.parent.exists():
                absolutDstPath.parent.mkdir(parents=True)
            src = str(absolutSrcPath)
            dst = str(absolutDstPath)
            if mode == ".docx":
                rep = Replace()
                doc = rep.run(src, dst, user,projectName)
                self.saveAsDocx(doc, dst)
            elif mode == '.xlsx':
                xls = excel()
                reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
                prefix = re.search(reg, dst.split('\\')[-1], re.M|re.I).group(1)
                xlsx = xls.title( src , dst , str(prefix) )
                self.saveAsExcel( xlsx , dst )
            else:
                rep = Replace()
                doc = rep.run(src, dst, user, projectName)
                self.saveAsPdf(doc, dst)
        except Exception as e:
            if not os.path.exists( './logging/' ):
                os.mkdir( './logging/' )
            stamp = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
            file = './logging/debug ' + stamp + '.log'
            log = open( file , 'a' )
            log.write( str(dst) + "  :  " +str(e) + '\n' )
            log.close()
            print(e)
