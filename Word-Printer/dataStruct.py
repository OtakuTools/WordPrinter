# -*- coding: utf-8 -*-
import re
import os

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
    coverField = ""#经营范围
    #string
    corporateRepresentative = ""#法人代表
    # string
    manager = ""#总经理
    # string
    guandai = ""#管理者代表
    # string
    compiler = ""#编制人
    # string
    approver = ""#批准人
    # string
    audit = ""#
    # string
    announcer = ""#发布人
    # string(Date) x年y月z日
    auditDate = "" # D1
    # array of string(Date) yyyy-mm-dd ["","","",""] #auditdate是UI中的编制日期，modifydate是从D1到D5
    modifyDate = [] # D1 ... D5
    # string(Date) x年y月z日
    releaseDate = ""#实施日期 D6
    # string zip code
    zip = ""
    # string telphone number
    phone = ""
    # string service policy
    policy = ""#服务方针
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

    def resetDepartment(self):
        self.departments = []
        self.departments.append( 
            {
                "name":"总经理",
                "level":1,
                "intro":[
                     "决定公司的生产经营计划和投资方案；",
                     "决定公司内部管理机构的设置；",
                     "批准公司的基本管理制度；",
                     "制订公司年度财务预、决算方案和利润分配方案、弥补亏损方案；",
                     "对公司增加或减少注册资本、分立、合并、终止和清算等重大事项提出方案；",
                     "聘任或解聘公司副总经理、财务部门等负责人，并决定其奖惩。"
                     ],
                "func":[1,2,3,4,5,6,17,18,22]
             } )
        self.departments.append(
            {
                "name":"信息技术服务管理小组",
                "level":2,
                "intro":[
                    "指导执行本公司的经营发展计划；",
                    "制定详细的工作计划分配到各部门；",
                    "对各部门的工作计划进行核定及作业督导；",
                    "处理信息技术服务的各种重要文书、文件；",
                    "协调公司各部门之间的关系；",
                    "处理公司出现的突发事件等。",
                    ],
                "func":[7,8,9,10,11,12,13,14,16,19,20,27,30]
                } )
        self.departments.append(
            {
                "name":"管理者代表",
                "level":2,
                "intro":[
                    "协助信息技术服务管理小组制定公司的信息技术服务方针及目标，并负责宣传、贯彻和检查；",
                    "承担信息技术服务管理体系的文件结构并组织编写；",
                    "监督信息技术服务体系文件的控制，包括文件的编制、评审、发放、更改，以及各部门文件控制检查；",
                    "承担记录的标识、贮存、保护、检索、保存期限的规定和处置的控制；",
                    "协助信息技术服务管理小组制定管理评审计划并组织管理评审会议；",
                    "承担纠正措施和预防措施的制定、落实和监督验证；",
                    "制定本部门的工作计划；",
                    "认真执行信息技术服务管理体系制定的相关文件和记录。",
                    ],
                "func":[]
            } )

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


colorStyle = {
        'FF0000':'fileName',
        'FE0000':'company',
        'FD0000':'introduction',
        'FC0000':'address',
        'FB0000':'coverField',
        'FA0000':'manager',
        'F90000':'guandai',
        'F80000':'compiler',
        'F70000':'approver',
        'F60000':'releaseDate',
        'F50000':'modifyDate',
        'F40000':'zip',
        'F30000':'phone',
        'F20000':'policy',
        'F10000':'audit',
        'F00000':'announcer',
        'EF0000':'logoPath',
        'EE0000':'departments',
        'ED0000':'picPath',
        'EC0000':'corporateRepresentative'
    }