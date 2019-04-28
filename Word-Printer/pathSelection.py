#-*- coding:utf-8 -*-
import os, re
class pathSelection:
    sampleDir = [".\\samples"]
    saveDir = ".\\docSave"
    samples = {}
    logos = {}
    levelDir = {}

    def __init__(self):
        self.autoRefresh()
    
    def __del__(self):
        pass

    def getSamples(self):
        return self.samples
    
    def getLevelDir(self):
        return self.levelDir

    def reset(self):
        self.samples = {}
        self.logos = {}
        self.levelDir = {}

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
                dir = self.saveDir + "\\" + fileName + "\\" + self.levelDir[label]
                if not os.path.exists(dir):
                    os.makedirs(dir)
                return dir + "\\" + re.sub(r"ZRXX", fileName, os.path.split(self.samples[label])[1])

    def getLogoPath(self, label):
        return self.logos[label]

    def searchAllSamples(self, path):
        for (root, dirs, files) in os.walk(path):
            level = root.split("\\")[-1]
            for file in files:
                suffix = os.path.splitext(file)[1]
                if suffix in [".docx", ".doc"]:
                    reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
                    prefix = re.search(reg, os.path.splitext(file)[0], re.M|re.I)
                    if(prefix):
                        label = prefix.group(1).split("-")
                        label = label[-3:len(label)]
                        self.samples["-".join(label)] = os.path.join(root, file)
                        self.levelDir["-".join(label)] = level
                elif suffix in [".jpg", ".png", ".jpeg"]:
                    self.logos[prefix] = file
            for dir in dirs:
                self.searchAllSamples(dir)