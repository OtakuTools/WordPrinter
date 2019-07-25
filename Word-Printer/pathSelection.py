#-*- coding:utf-8 -*-
import os, re, json, copy
from pathlib import Path, PurePath

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
        if os.path.exists(path) and path not in self.sampleDir:
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

class pathSelection_v2:

    def __init__(self):
        self.initArgs()
        self.autoRefresh()

    def initArgs(self):
        self.sampleDir = ".\\samples"
        self.saveDir = ".\\docSave"
        self.reg_file = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
        self.reg_proj = "([A-Z]{3}[项目|组织])"

    def reset(self):
        self.fileTree = {}
        self.customFileTree = {}

    def autoRefresh(self):
        self.reset()
        self.searchAllFiles(self.sampleDir, self.fileTree)

    def customizeFilePath(self, originFileTree, targetFileTree, company, projects, projIndex=-1):
        for k, v in originFileTree.items():
            prefix_file = re.search(self.reg_file, k, re.M | re.I)
            prefix_proj = re.search(self.reg_proj, k, re.M | re.I)
            temp_k = k
            isProject = False
            if prefix_file:
                temp_k = re.sub(r"ZRXX", company, temp_k)
                temp_k = re.sub(r"(XXX|XXXX)", projects[projIndex], temp_k)
            elif prefix_proj:
                isProject = True
            if isinstance(v, dict):
                if isProject:
                    for i in range(len(projects)):
                        temp_k = re.sub(r"(XXX|XXXX)", projects[i], k)
                        targetFileTree[temp_k] = {}
                        temp_v = copy.deepcopy(v)
                        self.customizeFilePath(temp_v, targetFileTree[temp_k], company, projects, i)
                else:
                    targetFileTree[temp_k] = {}
                    temp_v = copy.deepcopy(v)
                    self.customizeFilePath(temp_v, targetFileTree[temp_k], company, projects, projIndex)
            elif isinstance(v, list):
                filePath = re.sub(r"ZRXX", company, v[1])
                filePath = re.sub(r"(XXX|XXXX)", projects[projIndex], filePath)
                samplePath = PurePath(filePath).parts
                targetFileTree[temp_k] = [v[0],
                                          filePath,
                                          "/".join([self.saveDir, company] + list(samplePath[1:]))]
    '''
    def getFilePath(self, label, fileName = "", fullName=True):


    def getLogoPath(self, label):
    '''

    def searchAllFiles(self, path, fileTree={}, initial=True):
        if initial:
            root = path if isinstance(path, str) else str(path)
            fileTree[root] = {}
            initial = False
            return self.searchAllFiles(root, fileTree[root], initial)
        p = Path(path if isinstance(path, str) else str(path))
        dirs = [x for x in p.iterdir() if x.is_dir()]
        files = [x for x in p.iterdir() if x.is_file()]
        for file in files:
            fileTree[file.name] = [file.suffix, file.as_posix()]
        for dir in dirs:
            fileTree[str(dir.parts[-1])] = {}
            self.searchAllFiles(dir, fileTree[str(dir.parts[-1])], initial)

if __name__ == "__main__":
    ps = pathSelection_v2()
    #print(ps.testFileList)
    t = {}
    t_c = {}
    ps.searchAllFiles("./samples", t)
    ps.customizeFilePath(t, t_c, "AAAA", ["PROJECT1", "PROJECT2"])
    with open("File.json", "w") as f:
        json.dump(t, f, indent=4, ensure_ascii=False)
    with open("File_cus.json", "w") as f:
        json.dump(t_c, f, indent=4, ensure_ascii=False)
    #print(ps.testFileList)