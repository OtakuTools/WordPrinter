#-*- coding:utf-8 -*-
import os, re, json, copy
from pathlib import Path, PurePath

class pathSelection:

    def __init__(self):
        self.initArgs()
        self.autoRefresh()

    def initArgs(self):
        self.sampleDir = "./samples"
        self.saveDir = "./docSave"
        self.reg_file = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
        self.reg_proj = "([A-Z]{3}[项目|组织])"

    def reset(self):
        self.fileTree = {}
        self.customFileTree = {}

    def autoRefresh(self, company=None, projects=None):
        self.reset()
        self.searchAllFiles(self.sampleDir, self.fileTree)
        if company:
            if projects and len(projects):
                self.customizeFilePath(self.fileTree, self.customFileTree, company, projects)
            else:
                self.customizeFilePath(self.fileTree, self.customFileTree, company, ["XXX"])
        else:
            self.customizeFilePath(self.fileTree, self.customFileTree, "ZRXX", ["XXX"])

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
                targetFileTree[temp_k] = [{
                    "type" : v[0],
                    "spath": v[1],
                    "tpath": "/".join([self.saveDir, company] + list(samplePath[1:]))
                }]

    # 输入格式：xxx/xxx/xxx
    def getFileInfo(self, label):
        sPath = PurePath(label).parts
        temp_tree = self.customFileTree[self.sampleDir]
        for p in sPath:
            if p in temp_tree:
                temp_tree = temp_tree[p]
        return temp_tree[0] if isinstance(temp_tree, list) else {}

    # 输入格式：图片名称
    def getLogoInfo(self, label):
        return self.customFileTree[self.sampleDir]["logo"][label]

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
    ps = pathSelection()
    ps.autoRefresh("AAAA", ["PROJECT1", "PROJECT2"])
    with open("File.json", "w") as f:
        json.dump(ps.fileTree, f, indent=4, ensure_ascii=False)
    with open("File_cus.json", "w") as f:
        json.dump(ps.customFileTree, f, indent=4, ensure_ascii=False)
    print(ps.customFileTree[ps.sampleDir])
    print(ps.getFileInfo("Level1/AAAA-20000-SM-M-01 IT服务管理手册.docx"))