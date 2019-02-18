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