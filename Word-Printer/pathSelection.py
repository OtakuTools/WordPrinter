#-*- coding:utf-8 -*-
import os, re
class pathSelection:
    sampleDir = [".\\samples"]
    saveDir = ".\\save"
    samples = {}
    logos = {}
    levelDir = {}

    def __init__(self):
        pass
    
    def __del__(self):
        pass

    def addPath(self, path):
        if os.path.exists(path) and path not in sampleDir:
            self.sampleDir.append(path)
            self.autoRefresh()

    def autoRefresh(self):
        for sdir in self.sampleDir:
            if os.path.exists(sdir):
                self.searchAllSamples(sdir)

    def getFilePath(self, label, fileName = ""):
        if fileName == "":
            return self.samples[label]
        else:
            return self.saveDir + "\\" + fileName + "\\" + self.levelDir[label] + "\\" + re.sub(r"ZRXX", fileName, self.samples[label])

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
                        self.samples["-".join(label)] = file
                        self.levelDir["-".join(label)] = level
                elif suffix in [".jpg", ".png", ".jpeg"]:
                    self.logos[prefix] = file
            for dir in dirs:
                self.searchAllSamples(dir)