def getColorStyle():
    return {
        #RGB(Hex):key           #RGB(Dem)
        'None':'',              #it happens
        'FF0000':'user.fileName',    #(255,0,0)
        'FE0000':'user.company',     #(254,0,0)
        'FD0000':'',#introduction#(253,0,0)
        'FC0000':'user.address',     #(252,0,0)
        'FB0000':'user.coverField',  #(251,0,0)
        'FA0000':'user.manager',     #(250,0,0)
        'F90000':'user.guandai',     #(249,0,0)
        'F80000':'user.compiler',    #(248,0,0)
        'F70000':'user.approver',    #(247,0,0)
        'F60000':'user.releaseDate', #(246,0,0)
        'F50000':'user.modifyDate',  #(245,0,0)
        'F50001':'user.modifyDate.index1',#(245,0,1)
        'F50002':'user.modifyDate.index2',#(245,0,2)
        'F50003':'user.modifyDate.index3',#(245,0,3)
        'F50004':'user.modifyDate.index4',#(245,0,4)
        'F50005':'user.modifyDate.index5',#(245,0,5)
        'F40000':'user.zip',         #(244,0,0)
        'F30000':'user.phone',       #(243,0,0)
        'F20000':'user.policy',      #(242,0,0)
        'F10000':'user.audit',       #(241,0,0)
        'F00000':'user.announcer',   #(240,0,0)
        'EF0000':'',#logoPath   #(239,0,0)
        'EE0000':'',#departments#(238,0,0)
        'ED0000':'',#picPath'   #(237,0,0)
        'EC0000':'user.corporateRepresentative', #(236,0,0)
        'EB0000':'user.organization.Audit.auditLeader', #(235,0,0)
        'EA0000':'user.organization.Audit.audit1',      #(234,0,0)
        'E90000':'user.organization.Audit.audit2',      #(233,0,0)
        'E80000':'user.organization.Audit.audit3',      #(232,0,0)
        'E70000':'user.organization.Audit.planDate',    #(231,0,0)
        'E60000':'user.organization.Audit.auditDate',   #(230,0,0)
        'E50000':'user.organization.Audit.scheduleDate',#(229,0,0)
        'E40000':'user.organization.Audit.compiler',    #(228,0,0)
        'E30000':'user.organization.Audit.compileDate', #(227,0,0)
        'E20000':'user.organization.Audit.audit',       #(226,0,0)
        'E10000':'user.organization.Audit.approveDate', #(225,0,0)
        'E00000':'user.organization.Audit.reviewDate',  #(224,0,0)
        'DF0000':'user.organization.Audit.excuteDate',  #(223,0,0)
        'DE0000':'user.organization.Audit.reportDate',  #(222,0,0)
        'DD0000':'user.organization.Record.fileName',    #(221,0,0)
        'DC0000':'user.organization.Record.auditContent',#(220,0,0)
        'DB0000':'user.organization.Record.auditProcess',#(219,0,0)
        'DA0000':'user.organization.Record.audit',       #(218,0,0)
        'D90000':'user.organization.Record.auditDate',   #(217,0,0)
        'D80000':'user.organization.Record.approver',    #(216,0,0)
        'D70000':'user.organization.Record.approveDate', #(215,0,0)
        'D60000':'user.organization.Record.provider',    #(214,0,0)
        'D50000':'',#12/07部门名称#(213,0,0)
        'D40000':'project.BasicInfo.PartyA.projectName',     #(212,0,0)
        'D30000':'project.BasicInfo.PartyA.company',        #(211,0,0)
        'D20000':'project.BasicInfo.PartyA.name',            #(210,0,0)
        'D10000':'project.BasicInfo.PartyA.phone',           #(209,0,0)
        'D00000':'project.BasicInfo.PartyA.address',         #(208,0,0)
        'CF0000':'project.BasicInfo.PartyB.contactName',   #(207,0,0)
        'CE0000':'project.BasicInfo.PartyB.serviceName',   #(206,0,0)
        'CD0000':'project.BasicInfo.PartyB.serviceMail',   #(205,0,0)
        'CC0000':'project.BasicInfo.PartyB.servicePhone',  #(204,0,0)
        'B00000':'project.BasicInfo.PartyB.complainName',  #(176,0,0)
        'CB0000':'project.BasicInfo.PartyB.complainMail',  #(203,0,0)
        'CA0000':'project.BasicInfo.PartyB.complainPhone', #(202,0,0)
        'C90000':'project.BasicInfo.Detail.amount',     #(201,0,0)
        'C80000':'project.BasicInfo.Detail.period',     #(200,0,0)
        'C70000':'project.BasicInfo.Detail.config',     #(199,0,0)
        'C60000':'project.BasicInfo.Detail.name',       #(198,0,0)
        'C50000':'project.BasicInfo.Detail.level',      #(197,0,0)
        'C40000':'project.BasicInfo.Detail.details',    #(196,0,0)
        'C30000':'project.BasicInfo.Detail.demand',     #(195,0,0)
        'C20000':'project.BasicInfo.Detail.ddl',        #(194,0,0)
        'C10000':'project.BasicInfo.Team.startTime', #(193,0,0)
        'C00000':'project.BasicInfo.Team.require',   #(192,0,0)
        'BF0000':'project.BasicInfo.Team.PM',        #(191,0,0)
        'BE0000':'project.BasicInfo.Team.TM',        #(190,0,0)
        'BD0000':'project.ServiceProcess.Report.time',        #(189,0,0)
        'BC0000':'project.ServiceProcess.Report.keypoint',    #(188,0,0)
        'BB0000':'project.ServiceProcess.Report.revisit',     #(187,0,0)
        'BA0000':'project.ServiceProcess.Event.eventManager',     #(186,0,0)
        'B90000':'project.ServiceProcess.Event.issueManager',     #(185,0,0)
        'B80000':'project.ServiceProcess.Event.level',            #(184,0,0)
        'B70000':'project.ServiceProcess.Event.accepted',         #(183,0,0)
        'B60000':'project.ServiceProcess.Event.closed',           #(182,0,0)
        'B50000':'project.ServiceProcess.Event.transformed',       #(181,0,0)
        'B40000':'project.ServiceProcess.Event.summarized',       #(180,0,0)
        'B30000':'project.ServiceProcess.Config.modifyManager',         #(179,0,0)
        'B20000':'project.ServiceProcess.Config.configManager',         #(178,0,0)
        'B10000':'project.ServiceProcess.Config.releaseManager',        #(177,0,0)
        'AF0000':'project.ServiceProcess.Config.relatedManager',        #(175,0,0)
        'AE0000':'project.ServiceProcess.Config.configVersion',         #(174,0,0)
        'AD0000':'project.ServiceProcess.Config.configReleaseDate',     #(173,0,0)
        'AC0000':'project.ServiceProcess.Config.changes',               #(172,0,0)
        'AB0000':'project.ServiceProcess.Config.releases',              #(171,0,0)
        'AA0000':'project.ServiceProcess.Config.releaseDate',           #(170,0,0)
        'A90000':'project.ServiceProcess.Config.preReleaseDate',        #(169,0,0)
        'A80000':'project.ServiceProcess.Config.applicationDate',       #(168,0,0)
        'A70000':'project.ServiceProcess.Config.SN',                    #(167,0,0)
        'A60000':'project.ServiceProcess.Config.target',                #(166,0,0)
        'A50000':'project.ServiceProcess.Config.item',                  #(165,0,0)
        'A40000':'project.ServiceProcess.Config.releaseVersion',        #(164,0,0)
        'A30000':'project.ServiceProcess.Continuity.process',      #(163,0,0)
        'A20000':'project.ServiceProcess.Continuity.result',       #(162,0,0)
        'A10000':'project.ServiceProcess.Continuity.date',         #(161,0,0)
        'A00000':'project.ServiceProcess.Continuity.technicist',   #(160,0,0)
        '9F0000':'project.ServiceProcess.Continuity.approver',     #(159,0,0)
        '9E0000':'project.ServiceProcess.Continuity.compileDate',  #(158,0,0)
        '9D0000':'project.ServiceProcess.Continuity.auditDate',    #(157,0,0)
    }

def getGraphStyle():
    return [
        { 'nodes': {
            'fontname': 'KaiTi',
            'shape': 'box',
            'fontcolor': 'black',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#008000',
            },
            'lineLen' : 3},
        { 'nodes': {
            'fontname': 'KaiTi',
            'shape': 'box',
            'fontcolor': 'black',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#800000',
            },
            'lineLen' : 3},
        { 'nodes': {
            'fontname': 'KaiTi',
            'shape': 'box',
            'fontcolor': 'black',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#000080',
            },
            'lineLen' : 3},
        { 'nodes': {
            'fontname': 'KaiTi',
            'shape': 'box',
            'fontcolor': 'black',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#ffff00',
            },
            'lineLen' : 3}
    ]

def getDepartments():
    return [
        {
            "name": "总经理",
            "level": 1,
            "intro": [
                "决定公司的生产经营计划和投资方案；",
                "决定公司内部管理机构的设置；",
                "批准公司的基本管理制度；",
                "制订公司年度财务预、决算方案和利润分配方案、弥补亏损方案；",
                "对公司增加或减少注册资本、分立、合并、终止和清算等重大事项提出方案；",
                "聘任或解聘公司副总经理、财务部门等负责人，并决定其奖惩。"
            ],
            "func": [1, 2, 3, 4, 5, 6, 17, 18, 22],
            "leader": "",
            "operator": ""
        },
        {
            "name": "信息技术服务管理小组",
            "level": 2,
            "intro": [
                "指导执行本公司的经营发展计划；",
                "制定详细的工作计划分配到各部门；",
                "对各部门的工作计划进行核定及作业督导；",
                "处理信息技术服务的各种重要文书、文件；",
                "协调公司各部门之间的关系；",
                "处理公司出现的突发事件等。",
            ],
            "func": [7, 8, 9, 10, 11, 12, 13, 14, 16, 19, 20, 27, 30],
            "leader": "",
            "operator": ""
        },
        {
            "name": "管理者代表",
            "level": 2,
            "intro": [
                "协助信息技术服务管理小组制定公司的信息技术服务方针及目标，并负责宣传、贯彻和检查；",
                "承担信息技术服务管理体系的文件结构并组织编写；",
                "监督信息技术服务体系文件的控制，包括文件的编制、评审、发放、更改，以及各部门文件控制检查；",
                "承担记录的标识、贮存、保护、检索、保存期限的规定和处置的控制；",
                "协助信息技术服务管理小组制定管理评审计划并组织管理评审会议；",
                "承担纠正措施和预防措施的制定、落实和监督验证；",
                "制定本部门的工作计划；",
                "认真执行信息技术服务管理体系制定的相关文件和记录。",
            ],
            "func": [],
            "leader": "",
            "operator": ""
        },
        {
            "name": "客户服务中心",
            "level": 3,
            "intro": [
                "按计划完成公司签订的服务合同，并对进入维护期以后的工程项目进行维护；",
                "制定公司的服务方案、开发公司的服务品种以及服务报价；",
                "在研讨会上讲解公司的服务理念以及具体的实施；",
                "保持与产品原厂商服务部门的联络沟通；",
                "处理服务热线的客户服务要求，及时处理和解决客户的故障和维修问题；",
                "负责客户和内部员工的培训；",
                "认真执行ISO20000制定的相关文件和记录。",
                "负责进入维护期以后的工程项目进行维护；",
                "处理服务热线的客户服务要求，及时处理和解决客户的故障和维修问题等。",
                "根据公司资源，为客户提供硬件、本地网络、远程网络、系统平台、开发环境等的综合优化选择、提供系统规划或二次开发支持等增值性服务方案。",
                "负责客户和内部员工相关培训课程的建设与完善；",
                "满足不同项目客户培训需要；",
                "提供丰富的系统应用和产品培训课程。",
                "针对不同客户的特殊需求，提供各项专题培训。"
            ],
            "func": [15, 21, 23, 24, 25, 31, 33, 34, 35, 36, 37, 38, 39],
            "leader": "",
            "operator": ""
        },
        {
            "name": "系统集成中心",
            "level": 3,
            "intro": [
                "系统集成中心是公司的直接创利部门之一，进行系统集成方面的业务开拓，实现公司要求的年度经营目标；",
                "提供技术方面的售前技术支持，包括硬件产品的报价、系统集成项目方案的编写、招投标文件的编写等，促进业务的开展；",
                "按项目合同标准提供技术方面的实施和售后服务，包括系统工程实施、系统售后服务等，保证达到公司要求的实施目标和客户满意度；",
                "结合行业情况，进行集成技术的研究，提高集成技术水平，实现公司业务利润目标；",
                "制定本部门的工作计划；",
                "认真执行信息技术服务管理体系制定的相关文件和记录。",
                "公司代理的高低端产品的询价、报价及监督和认真执行ISO 20000制定的相关文件和记录；",
                "了解客户或招标的需求并加以分析，根据要求编写各种技术方案和投标文件;",
                "负责各项工程项目的具体实施运作；",
                "在项目实施过程中负责组织施工计划、设备进场，安装、调度、验收等工作。"
            ],
            "func": [],
            "leader": "",
            "operator": ""
        },
        {
            "name": "营销管理中心",
            "level": 3,
            "intro": [
                "制定公司年度的销售计划和考核计划，报领导审批；",
                "完成公司规定的年度销售计划；",
                "及时了解行业的最新动态，依据市场环境的变化趋势和内部出现的问题，对销售指标作出调整；",
                "稳固老客户，挖掘新客户，并制定销售策略；",
                "培训和管理销售管理人员；",
                "认真执行ISO20000制定的相关文件和记录。",
                "实现以系统集成业务、软件产品类型分类进行产品、解决方案销售；",
                "负责公司年度市场推广计划的制定；",
                "产品和技术研讨会的组织安排；",
                "公司企业形象的设计执行和推广；",
                "公司广告宣传；",
                "公司的客户满意度调查；",
                "公司资质的认证；",
                "市场策划；",
                "专项申请等。"
            ],
            "func": [21, 31, 33],
            "leader": "",
            "operator": ""
        },
        {
            "name": "软件研发中心",
            "level": 3,
            "intro": [
                "负责公司的整体软件开发核心技术，组织制定和实施重大技术决策和技术方案；",
                "指导、审核、制定、开发软件项目，对各项结果做最终质量评估、归档；",
                "设计、开发、维护、管理软件项目及软件产品。",
                "完善部门发展规划，组织审定部门各项技术标准，编制完善软件开发流程；",
                "完善与其他部门的沟通与协作；",
                "协助参与公司项目的招投标软件接口等资料的编写和策划；",
                "制定技术方案，根据项目类型提成准确的需求，制定项目进度计划表，负责验收工作；",
                "填写测试报告，编写相关操作手册文档；",
                "关注最新技术动态，组织内部技术交流与技术传递。",
                "负责公司内外部软件开发项目的需求调查、方案制定、软件编程、成果申报等组织实施工作;",
                "负责对自行开发、合作开发以及外购软件的安装、测试、培训、系统维护和售后服务等工作。",
                "负责与开发部配合根据需求说明书制订《项目测试方案》，编写《测试用例》，建立测试环境；",
                "负责软件产品开发过程和投入运营之前的新增软件和修改升级软件的模块测试和系统测试；",
                "负责软件问题解决过程跟踪记录。",
                "负责对软件行业信息的收集、整理、研究及利用;",
                "负责自主开发软件产品的销售及售前技术支持;",
                "负责推广实施软件开发文档规范化工作，管理研发产品相关文档。"
            ],
            "func": [21, 28, 29, 40, 41, 42],
            "leader": "",
            "operator": ""
        },
        {
            "name": "行政中心",
            "level": 3,
            "intro": [
                "负责公司行政文件及决议的起草、文印、分发及存档工作；",
                "公司基础设施的提供、维护，环境卫生和安全防范的工作；",
                "公司固定资产管理的工作；",
                "负责公司组织的各类活动；",
                "行政规章制度的制订与实施；",
                "负责公司人员编制计划的制订及实施；",
                "负责人事相关管理工作；",
                "工程项目的交接、设备订货发货；",
                "设备出入库管理；",
                "合同管理（包括公司签定的合同以及与供货商的合同）；",
                "认真执行IS020000制定的相关文件和记录。",
                "负责办理员工招聘、任用、调配、解聘及培训、考核、提拔、奖惩等人事管理工作；",
                "负责公司培训计划；",
                "负责办理劳动、人事、社保手续;",
                "负责保管人事档案等。",
                "负责公司相关集成项目设备的采购订货及合同管理等。",
                "负责公司设备的进出库管理工作。"
            ],
            "func": [17, 32],
            "leader": "",
            "operator": ""
        },
        {
            "name": "财务部",
            "level": 3,
            "intro": [
                "负责制定客户服务部门年度财务预算与核算，处理各相关客户的财务会计事项；",
                "向上级财务主管部门、税务部门、统计主管部门等提供财务报告、报表和统计报告，保持联系并协调关系；",
                "负责公司记帐、算帐和报帐，出具内部财务报告，进行财务分析，提出财务建议。"
            ],
            "func": [33],
            "leader": "",
            "operator": ""
        }]