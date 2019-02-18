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


if __name__ == '__main__':
    user = userInfo();
    with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
    for dict in data:
        for key in dict.keys():
            setattr( user , key , dict[key] )
        user.picPath = "./save/" + user.fileName + "-20000-SM-M-01_picture.png"
        #replace('sample.docx',user.fileName+'-20000-SM-M-01.docx' , user ).save(user.fileName+'-20000-SM-M-01.docx')
        getTime( user )
