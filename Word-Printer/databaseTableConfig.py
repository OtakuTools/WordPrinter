class databaseTableConfig:
    tables = [
        """
        CREATE TABLE IF NOT EXISTS info( 
            id NVARCHAR(20) NOT NULL, 
            company NVARCHAR(100) NOT NULL,
            address NVARCHAR(100) NOT NULL,
            introduction NVARCHAR(1000) NOT NULL,
            coverField NVARCHAR(1000) NOT NULL,
            corporate NVARCHAR(20) NOT NULL,
            manager NVARCHAR(20) NOT NULL,
            guanDai NVARCHAR(20) NOT NULL,
            compiler NVARCHAR(20) NOT NULL,
            approver NVARCHAR(20) NOT NULL,
            audit NVARCHAR(20) NOT NULL,
            announcer NVARCHAR(20) NOT NULL,
            releaseDate NVARCHAR(20) NOT NULL,
            auditDate NVARCHAR(20) NOT NULL,
            zip NVARCHAR(6) NOT NULL,
            phone NVARCHAR(20) NOT NULL,
            policy NVARCHAR(200) NOT NULL,
            picPath NVARCHAR(200) NOT NULL,
            depStruct NVARCHAR(1000) NOT NULL,
            color NVARCHAR(1000) NOT NULL,
            PRIMARY KEY (company)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS department( 
            refId NVARCHAR(100) NOT NULL,
            level INT(1) NOT NULL DEFAULT 0,
            name NVARCHAR(20) NOT NULL,
            leader NVARCHAR(20) NOT NULL,
            operator NVARCHAR(20) NOT NULL,
            intro NVARCHAR(1500) NOT NULL,
            func NVARCHAR(200) NOT NULL,
            seq INT(5) NOT NULL,
            PRIMARY KEY (refId, name),
            FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS logoStore( 
            refId NVARCHAR(100) NOT NULL,
            logopath NVARCHAR(200),
            photo MEDIUMBLOB DEFAULT NULL,
            PRIMARY KEY (refId),
            FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS projectInfo(
            refId NVARCHAR(100) NOT NULL,
            AprojectName nvarchar(100) NOT NULL,
            Acompany nvarchar(50) NOT NULL,
            Aname nvarchar(30),
            Aphone nvarchar(15),
            Aaddress nvarchar(100),
            BcontactName nvarchar(30),
            BserviceName nvarchar(30),
            BserviceMail nvarchar(30),
            BservicePhone nvarchar(15),
            BcomplainName nvarchar(30),
            BcomplainMail nvarchar(30),
            BcomplainPhone nvarchar(15),
            Damount nvarchar(30),
            Dperiod nvarchar(30),
            Dconfig nvarchar(300),
            Dname nvarchar(30),
            Dlevel nvarchar(10),
            Ddetails nvarchar(300),
            Ddemand nvarchar(300),
            Dddl nvarchar(300),
            TstartTime nvarchar(30),
            Trequire nvarchar(300),
            TPM nvarchar(30),
            TTM nvarchar(30),
            seq int,
            PRIMARY KEY (refId, AprojectName),
            INDEX(AprojectName),
            FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS serviceProcess(
            refId NVARCHAR(100) NOT NULL,
            refAprojectName nvarchar(100) NOT NULL,
            RepTime nvarchar(30),
            RepKeypoint nvarchar(300),
            RepRevisit nvarchar(30),
            EveEventManager nvarchar(30),
            EveIssueManager nvarchar(30),
            EveS1 int,
            EveS2 int,
            EveS3 int,
            EveS4 int,
            EveClosed int,
            EveTransformed int,
            EveSummarized int,
            CofModifyManager nvarchar(30),
            CofConfigManager nvarchar(30),
            CofReleaseManager nvarchar(30),
            CofRelatedManager nvarchar(30),
            CofConfigVersion nvarchar(30),
            CofConfigReleaseDate nvarchar(30),
            CofChanges int,
            CofReleases int,
            CofReleaseDate nvarchar(30),
            CofPreReleaseDate nvarchar(30),
            CofApplicationDate nvarchar(30),
            CofSN nvarchar(50),
            CofTarget nvarchar(50),
            CofItem nvarchar(50),
            CofReleaseVersion nvarchar(30),
            CofSubject nvarchar(100),
            CotProcess nvarchar(400),
            CotResult nvarchar(400),
            CotDate nvarchar(30),
            CotTechnicist nvarchar(30),
            CotApprover nvarchar(30),
            CotCompileDate nvarchar(30),
            CotAuditDate nvarchar(30),
            PRIMARY KEY (refId, refAprojectName),
            FOREIGN KEY (refId) REFERENCES projectInfo(refId) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (refAprojectName) REFERENCES projectInfo(AprojectName) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS organization(
            refId NVARCHAR(100) NOT NULL,
            AudPlanDate nvarchar(30),
            AudAuditDate nvarchar(30),
            AudAuditLeader nvarchar(30),
            AudAudit1 nvarchar(30),
            AudAudit2 nvarchar(30),
            AudAudit3 nvarchar(30),
            AudReviewDate nvarchar(30),
            AudScheduleDate nvarchar(30),
            AudExcuteDate nvarchar(30),
            AudReportDate nvarchar(30),
            AudCompiler nvarchar(30),
            AudAudit nvarchar(30),
            AudCompileDate nvarchar(30),
            AudApproveDate nvarchar(30),
            RecTarget nvarchar(30),
            RecTime nvarchar(30),
            RecStaff nvarchar(30),
            RecArrange nvarchar(30),
            RecContent nvarchar(300),
            RecFileName nvarchar(100),
            RecAuditContent nvarchar(100),
            RecAuditProcess nvarchar(100),
            RecAudit nvarchar(30),
            RecAuditDate nvarchar(30),
            RecApprover nvarchar(30),
            RecApproveDate nvarchar(30),
            RecProvider nvarchar(30),
            PRIMARY KEY (refId),
            FOREIGN KEY (refId) REFERENCES info(company) ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """]

    def __init__(self):
        pass

    def getTables(self):
        return self.tables