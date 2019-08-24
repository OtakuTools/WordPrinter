import requests
import os, json, sys, subprocess

class AutoUpdate():
    baseURL = "http://otakutools.top:8000/"
    version_url = "version.json"

    versionController = {}
    Config = ""

    def is_downloadable(self, url):
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def checkVersion(self):
        res = requests.get(self.baseURL + self.version_url, allow_redirects=True)
        open("version.json", 'wb').write(res.content)
        with open("version.json", "r") as f:
            self.versionController = json.load(f)
        with open("config/help.json", "r") as f:
            self.Config = json.load(f)
        return self.versionController["version"] > self.Config["version"]

    def downloadEXE(self):
        exeURI = self.baseURL + self.versionController["path"]
        if self.is_downloadable(exeURI):
            res = requests.get(exeURI, allow_redirects=True)
            open("main_new.exe", 'wb').write(res.content)
            self.Config["version"] = self.versionController["version"]
            with open("config/help.json", "w") as f:
                json.dump(self.Config, f)
            return True
        else:
            print("can not download exe")
            return False

    def installNewEXE(self):
        if os.path.isfile("upgrade.bat"):
            os.remove("upgrade.bat")
        self.WriteRestartCmd("main_new.exe")

    def WriteRestartCmd(self, exe_name):
        with open("upgrade.bat", 'w') as b:
            TempList = "@echo off\n";  # 关闭bat脚本的输出
            TempList += "if not exist " + exe_name + " exit \n";  # 新文件不存在,退出脚本执行
            TempList += "sleep 3\n"  # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
            TempList += "del " + os.path.realpath("main.exe") + "\n"  # 删除当前文件
            TempList += "ren " + exe_name + " main.exe" + "\n"  # 删除当前文件
            TempList += "start main.exe"  # 启动新程序
            b.write(TempList)
        subprocess.Popen("upgrade.bat")
        sys.exit()


if __name__=="__main__":
    au = AutoUpdate()
    print("正在检查版本")
    has_new = au.checkVersion()
    if has_new:
        print("检查到出现新版本，开始下载....")
        is_ok = au.downloadEXE()
        if is_ok:
            print("下载完成,正在执行安装程序")
            au.installNewEXE()
    else:
        print("该版本已经是最新版")
    print("更新完毕")