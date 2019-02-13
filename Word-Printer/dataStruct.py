# -*- coding: utf-8 -*-

class userInfo:
    # string
    company = ""
    # string
    address = ""
    # array of string ["",""] under 800
    introduction = []
    # array of string ["",""] under 50
    coverField = []
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
    # string(Date) x年y月z日
    releaseDate = ""
    # string(Date) x年y月z日
    auditDate = ""
    # dict array
    """
    #[
    #    {
    #        "name":"",
    #        "intro":"",
    #        "func"
    #    },
    #    {
    #        "name":"",
    #        "intro":"",
    #        "func"
    #    }
    #]
    """
    departments = []
    # string path
    picPath = ""
    # string filename
    fileName = ""
    # string zip code
    zip = ""
    # string telphone number
    phone = ""
    # string service policy
    policy = ""

    def __init__(self):
        pass

    def __del__(self):
        pass