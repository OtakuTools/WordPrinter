import datetime
from dataStruct import userInfo
import json

def getTime( user_info ):
    modifyDate = []
    #D1
    time = user_info.auditDate.replace('年','-').replace('月','-').replace('日','-').split('-')
    now = datetime.date( int(time[0]) , int(time[1]) , int(time[2]) )
    modifyDate.append(now.strftime("%Y-%m-%d"))
    #D2 to D4
    now = now + datetime.timedelta(days=89)#D2
    delta = datetime.timedelta(days=1)
    for i in range(3):
        now += delta
        modifyDate.append(now.strftime("%Y-%m-%d"))
    #D5=D4
    modifyDate.append(now.strftime("%Y-%m-%d"))
    
    user_info.modifyDate = modifyDate
    return user_info
    