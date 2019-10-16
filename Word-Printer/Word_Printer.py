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
from comtypes.client import CreateObject

class docWriter:
    def __init__(self):
        self.saveDir = "./docSave/"

    def __del__(self):
        pass

    def saveAsDocx(self, doc, filepath):
        doc.save(filepath)

    def saveAsPdf(self, fullsrc, fulldst):
        if fullsrc and fullsrc.split('.')[-1] == 'docx':
            word = CreateObject("Word.Application")
            doc = word.Documents.Open(fullsrc)
            print(fulldst)
            doc.SaveAs(fulldst,17)
        '''
        if fullsrc and fullsrc.split(',')[-1] == 'docx':
            word = CreateObject("Excel.Application")
            doc = word.Workbooks.Open(fullsrc)
            doc.SaveAs(fulldst)
        '''
        pass

    def saveAsExcel( self , xls , dst ):
        xls.save(dst)

    def loadAndWrite(self, user , templateFile, targetFile, mode=".docx", projectName=None, PDFlag=False):
        self.write(templateFile, targetFile, user, mode, projectName, PDFlag)
        
    def loadInfo(self):
        user = userInfo()
        with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
            for dict in data:
                for key in dict.keys():
                    setattr( user , key , dict[key] )
        return user

    def write(self, src, dst, user, mode=".docx", projectName=None, PDFlag=False):
        try:
            absolutSrcPath = Path(src) if Path(src).is_absolute() else Path.cwd() / Path(src)
            absolutDstPath = Path(dst) if Path(dst).is_absolute() else Path.cwd() / Path(dst)
            if not absolutDstPath.parent.exists():
                absolutDstPath.parent.mkdir(parents=True)
            src = str(absolutSrcPath)
            dst = str(absolutDstPath)

            #获取项目对象
            project = None
            try:
                if projectName != None and projectName != "" :
                    for proj in user.projects:
                        project = proj if proj.BasicInfo.PartyA.projectName == projectName else project
            except Exception as e:
                raise

            #依类型替换
            if mode == ".docx":
                rep = Replace()
                doc = rep.run(src, dst, user,project)
                self.saveAsDocx(doc, dst)
                if PDFlag == 2:
                    pdfdst = dst
                    self.saveAsPdf( dst , pdfdst.replace('docx','pdf') )
            elif mode == '.xlsx':
                xls = excel()
                reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
                prefix = re.search(reg, dst.split('\\')[-1], re.M|re.I).group(1)
                xlsx = xls.run( src , dst , str(prefix) , project)
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
