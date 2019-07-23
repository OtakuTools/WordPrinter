#-*- coding:utf-8 -*-
import os, re
class pathSelection:
    sampleDir = [".\\samples"]
    saveDir = ".\\docSave"
    samples = {}
    logos = {}
    levelDir = {}
    docType = {}

    def __init__(self):
        self.autoRefresh()
    
    def __del__(self):
        pass

    def getSamples(self):
        return self.samples
    
    def getLevelDir(self):
        return self.levelDir
    
    def getDocType(self):
        return self.docType

    def reset(self):
        self.samples = {}
        self.logos = {}
        self.levelDir = {}
        self.docType = {}

    def addPath(self, path):
        if os.path.exists(path) and path not in sampleDir:
            self.sampleDir.append(path)
            self.autoRefresh()

    def autoRefresh(self):
        self.reset()
        for sdir in self.sampleDir:
            if os.path.exists(sdir):
                self.searchAllSamples(sdir)

    def getFilePath(self, label, fileName = "", fullName=True):
        if fileName == "":
            return self.samples[label]
        else:
            if not fullName:
                return re.sub(r"ZRXX", fileName, self.samples[label])
            else:
                samplePath = os.path.split(self.samples[label])
                dir = self.saveDir + "\\" + re.sub(r".\\samples", fileName, samplePath[0])
                if not os.path.exists(dir):
                    os.makedirs(dir)
                currentDir = dir + "\\" + re.sub(r"ZRXX", fileName, samplePath[1])
                print(currentDir)
                return currentDir

    def getLogoPath(self, label):
        return self.logos[label]

    def searchAllSamples(self, path):
        self.isLevel4 = False
        for (root, dirs, files) in os.walk(path):
            reg_dir = "(Level\d{1})"
            prefix = re.search(reg_dir, root, re.M|re.I)
            if prefix:
                level = prefix.group(1)
                for file in files:
                    suffix = os.path.splitext(file)[1]
                    if suffix in [".docx", ".doc", ".xls", ".xlsx"]:
                        reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
                        prefix = re.search(reg, os.path.splitext(file)[0], re.M|re.I)
                        if(prefix):
                            label = prefix.group(1).split("-")
                            label = label[-3:len(label)]
                            self.samples["-".join(label)] = os.path.join(root, file)
                            self.levelDir["-".join(label)] = level
                            self.docType["-".join(label)] = suffix
                    elif suffix in [".jpg", ".png", ".jpeg"]:
                        self.logos[prefix] = file
            for dir in dirs:
                self.searchAllSamples(dir)