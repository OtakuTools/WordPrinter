import datetime
from dataStruct import userInfo
import json

'''
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
'''

def getTime( user_info ):
    modifyDate = []
    #now = datetime.datetime.now()
    time = user_info.auditDate.replace('年','-').replace('月','-').replace('日','-').split('-')
    now = datetime.date( int(time[0]) , int(time[1]) , int(time[2]) )
    modifyDate.append(now.strftime("%Y-%m-%d"))#1-1
    #第二行
    now = now + datetime.timedelta(days=31)
    delta = datetime.timedelta(days=1)
    for i in range(3):
        #print( now.strftime("%Y-%m-%d") )
        modifyDate.append(now.strftime("%Y-%m-%d"))
        now += delta
    user_info.modifyDate = modifyDate
    return user_info
    