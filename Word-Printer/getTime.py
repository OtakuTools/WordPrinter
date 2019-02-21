import datetime
from dataStruct import userInfo
import json

def getTime( user_info ):
    modifyDate = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(4):
        #print( now.strftime("%Y-%m-%d") )
        modifyDate.append(now.strftime("%Y-%m-%d"))
        now += delta
    user_info.modifyDate = modifyDate
    return user_info

