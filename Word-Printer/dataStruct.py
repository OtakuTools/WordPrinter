# -*- coding: utf-8 -*-
import re
import os
import json,datetime

from presetData import *

class DotDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def toDotDict(data):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    data[k] = DotDict(v)
                    DotDict.toDotDict(data[k])
        else:
            return data

        return DotDict(data)

class Organization():
    def __init__(self):
        self.Info = {
            "Audit" : {
                "planDate" : "" , # 内审计划时间
                "auditDate" : "" , # 内审审核执行时间
                "auditLeader" : "" , # 审核组长
                "audit1" : "" , # 审核员1
                "audit2" : "" , # 审核员2
                "audit3" : "" , # 审核员3
                "reviewDate" : "" , # 预期管理评审时间
                "scheduleDate" : "" , # 管评计划时间
                "excuteDate" : "" , # 管理评审执行日期
                "reportDate" : "" , # 管评实施报告日期
                "compiler" : "" , # 审核编制人
                "audit" : "" , # 审核审批人
                "compileDate" : "" , # 审核编制日期
                "approveDate" : "" , # 审核审批时间
            },

            "Record" : {
                "target" : "" , # 审计对象
                "time" : "" , # 审计时间
                "staff" : "" , # 审计人员
                "arrange" : "" , # 审计安排
                "content" : "" , # 文件审批内容
                "fileName" : "" , # 审批文件名称
                "auditContent" : "" , # 审批文件审核内容
                "auditProcess" : "" , # 审批文件过程简述
                "audit" : "" , # 文件审批人
                "auditDate" : "" , # 文件审批日期
                "approver" : "" , # 文件批准人
                "approveDate" : "" , # 文件批准日期
                "provider" : "" , # 文件发放人
            }
        }
        self.__dict__ = DotDict.toDotDict(self.Info)

class Project():
    def __init__(self, projectName=""):
        self.Info = {
            "BasicInfo": {
                "PartyA": {
                    "projectName": "",  # 项目名称
                    "company": "",  # 甲方名称
                    "name": "",  # 甲方联系人姓名
                    "phone": "",  # 甲方联系电话
                    "address": ""  # 甲方地址
                },

                "PartyB": {
                    "contactName": "",  # 乙方联系人姓名
                    "serviceName": "",  # 乙方服务联系人姓名
                    "serviceMail": "",  # 乙方服务联系人邮箱
                    "servicePhone": "",  # 乙方服务联系人手机
                    "complainName": "",  # 乙方服务投诉人姓名
                    "complainMail": "",  # 乙方服务投诉人邮箱
                    "complainPhone": ""  # 乙方服务投诉人手机
                },

                "Detail": {
                    "amount": "",  # 项目金额
                    "period": "",  # 项目有效期
                    "config": "",  # 服务配置项
                    "name": "",  # 服务名称
                    "level": "",  # 服务级别
                    "details": "",  # 服务内容
                    "demand": "",  # 服务要求
                    "ddl": ""  # 服务时间要求
                },
                "Team": {
                    "startTime": "",  # 项目启动时间
                    "require": "",  # 项目需求分析
                    "PM": "",  # 项目经理
                    "TM": "",  # 项目技术经理
                }
            },

            "ServiceProcess": {

                "Report": {
                    "time": "",  # 服务报告期
                    "keypoint": "",  # 下阶段重点工作内容
                    "revisit": "",  # 服务回访日期
                },

                "Event": {
                    "eventManager": "",  # 事件管理经理
                    "issueManager": "",  # 问题管理经理
                    "level": "S1",  # 受理事件等级
                    "accepted": 0,  # 受理事件数
                    "closed": 0,  # 关闭事件数
                    "transformed": 0,  # 转化为问题的事件数
                    "summarized": 0,  # 汇总问题数
                },

                "Config": {
                    "modifyManager": "",  # 变更经理
                    "configManager": "",  # 配置经理
                    "releaseManager": "",  # 发布经理
                    "relatedManager": "",  # 关系经理
                    "configVersion": "",  # 配置版本
                    "configReleaseDate": "",  # 配置发布日期
                    "changes": 0,  # 变更数量
                    "releases": 0,  # 发布总数量
                    "releaseDate": "",  # 发布日期
                    "preReleaseDate": "",  # 预发布日期
                    "applicationDate": "",  # 发布申请时间
                    "SN": "",  # 发布单号
                    "target": "",  # 发布目标
                    "item": "",  # 发布交付物
                    "releaseVersion": "",  # 发布版本
                },

                "Continuity": {
                    "process": "",  # 连续性测试经过内容
                    "result": "",  # 连续性测试结果内容
                    "date": "",  # 连续性测试日期
                    "technicist": "",  # 可用性技术人员
                    "approver": "",  # 可用性审批人员
                    "compileDate": "",  # 记录编制时间
                    "auditDate": "",  # 记录审核时间
                }
            }
        }
        self.Info["BasicInfo"]["PartyA"]["projectName"] = projectName
        self.__dict__ = DotDict.toDotDict(self.Info)

class userInfo:
    # string filename
    fileName = ""
    # string
    company = ""
    # string
    address = ""
    # array of string ["",""] under 800
    introduction = []
    # string under 50
    coverField = "" # 经营范围
    #string
    corporateRepresentative = "" # 法人代表
    # string
    manager = "" # 总经理
    # string
    guandai = "" # 管理者代表
    # string
    compiler = "" # 编制人
    # string
    approver = "" # 批准人
    # string
    audit = "" # 审核人
    # string
    announcer = "" # 发布人
    # string(Date) x年y月z日
    auditDate = "" #  D1
    # array of string(Date) yyyy-mm-dd ["","","",""] #auditdate是UI中的编制日期，modifydate是从D1到D5
    modifyDate = [] # D1 ... D5
    # string(Date) x年y月z日
    releaseDate = "" # 实施日期 D6
    # string zip code
    zip = ""
    # string telphone number
    phone = ""
    # string service policy
    policy = "" # 服务方针
    # string path
    picPath = ""
    # string path
    logoPath = ""
    # string
    depStruct = ""
    # string
    color = ""
    # dict array
    """
    #[
    #    {
    #        "name":"",
    #        "level": 0,
    #        "intro":[""],
    #        "func":[],
    #        "leader":"",#部门负责人
    #        "operator":"" # 部门经办人
    #    }
    #]
    """
    # array of {"name":departmentName,...}
    departments = []
    # array of project
    projects = []
    # instance of organization
    organization = Organization()

    def __init__(self):
        self.auditDate = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        self.releaseDate = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        self.resetDepartment()
        self.projects = []

    def __del__(self):
        pass

    def resetDepartment(self):
        self.departments = []
        try:
            with open('./config/preset.json', 'r', encoding="utf8") as f:
                deps = json.load(f)
            for dep in deps:
                self.departments.append( dict(dep) )
        except Exception as e:
            self.departments = getDepartments()
            print(e)

    def validChecker(self):
        errMsg = ""
        isValid = True
        #检空
        if self.fileName == "":
            errMsg = errMsg + "公司缩写：不能为空;\n"
            isValid = False
        if self.company == "":
            errMsg = errMsg + "公司名称：不能为空;\n"
            isValid = False
        if self.address == "":
            errMsg = errMsg + "公司地址：不能为空;\n"
            isValid = False
        if len(self.introduction) == 0:
            errMsg = errMsg + "公司简介：不能为空;\n"
            isValid = False
        if self.coverField == "":
            errMsg = errMsg + "经营范围：不能为空;\n"
            isValid = False
        #法人
        if self.corporateRepresentative == "":
            errMsg = errMsg + "法人代表：不能为空；\n"
            isValid = False
        if self.manager == "":
            errMsg = errMsg + "经理：不能为空;\n"
            isValid = False
        if self.guandai == "":
            errMsg = errMsg + "管理者代表：不能为空;\n"
            isValid = False
        if self.compiler == "":
            errMsg = errMsg + "编制人：不能为空;\n"
            isValid = False
        if self.approver == "":
            errMsg = errMsg + "批准人：不能为空;\n"
            isValid = False
        if self.audit == "":
            errMsg = errMsg + "审计人：不能为空;\n"
            isValid = False
        if self.announcer == "":
            errMsg = errMsg + "发布人：不能为空;\n"
            isValid = False
        if self.zip == "":
            errMsg = errMsg + "邮编：不能为空;\n"
            isValid = False
        if self.phone == "":
            errMsg = errMsg + "联系方式：不能为空;\n"
            isValid = False
        if self.policy == "":
            errMsg = errMsg + "服务方针：不能为空;\n"
            isValid = False
        if len(self.departments) == 0:
            errMsg = errMsg + "部门：不能为空;\n"
            isValid = False
        #公司缩写
        if re.compile(r"^[A-Z]{4}$").match(self.fileName) == None:
            errMsg = errMsg + "公司缩写：必须为4位大写英文字母；\n"
            isValid = False
        #业务范围
        if len( self.coverField) > 50:
            errMsg = errMsg + "业务范围：50字以内\n"
            isValid = False
        #公司简介
        if len( ':'.join(self.introduction) ) > 800:
            errMsg = errMsg + "公司简介：800字以内\n"
            isValid = False
        #电话格式
        if re.compile(r"^((\d{3})|(\d{3}\-))?(\d{8})$").match(self.phone) == None:
            errMsg = errMsg + "电话：请输入合法的电话\n"
            isValid = False
        #邮编
        if re.compile(r"^\d{6}$").match(self.zip) == None:
            errMsg = errMsg + "邮编：请输入合法的邮编\n"
            isValid = False
        #部门简介
        for dep in self.departments:
            if( len(dep["intro"]) == 0 ):
                errMsg = errMsg + dep["name"] + ":部门简介不能为空"
                isValid = False
        return ( isValid , errMsg )

if __name__ == "__main__":
    test = Project("aaa")
    print(test.BasicInfo.PartyA.projectName)
    print(test.__dict__["BasicInfo"]["PartyA"]["projectName"])
    test.BasicInfo.PartyA.projectName = "ccc"
    print(test.BasicInfo.PartyA.projectName)
    print(test.__dict__["BasicInfo"]["PartyA"]["projectName"])
    print(test.Info["BasicInfo"]["PartyA"]["projectName"])