# -*- coding: utf-8 -*-

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
    coverField = ""
    # string
    manager = ""
    # string
    guandai = ""
    # string
    employees = ""
    # string
    approver = ""
    # string
    audit = ""
    # string
    announcer = ""
    # array of string(Date) yyyy-mm-dd ["","","",""]
    modifyDate = []
    # string(Date) x年y月z日
    releaseDate = ""
    # string(Date) x年y月z日
    auditDate = ""
    # string zip code
    zip = ""
    # string telphone number
    phone = ""
    # string service policy
    policy = ""
    # string path
    picPath = ""
    # string
    depStruct = ""
    # dict array
    """
    #[
    #    {
    #        "name":"",
    #        "level": 0,
    #        "intro":"",
    #        "func"
    #    }
    #]
    """
    # array of string
    departments = []

    def __init__(self):
        pass

    def __del__(self):
        pass

    def validChecker(self):
        errMsg = ""
        isValid = True
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
        if self.manager == "":
            errMsg = errMsg + "经理：不能为空;\n"
            isValid = False
        if self.guandai == "":
            errMsg = errMsg + "管理者代表：不能为空;\n"
            isValid = False
        if self.employees == "":
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
        if not isValid:
            return (False, errMsg)
        return (True, "")