import requests
import os
import sys
import time
import account
import reportTem
import json

DATAFILENAME = "data.json"
REPORTHOUR = [[7, 10], [12, 15]]  # 上报体温的时间段，单位为小时
SLEEPTIME = 3600


def userLogin(userGroup):
    tokenGroup = []  # 字典数组
    try:
        for user in userGroup:
            userAccount = account.account(user["username"], user["password"])
            userAccount.login()
            userAccount.auth()
            userAccount.getxToken()
            tokenGroup.append({"cookies": userAccount.cookies,
                               "token": userAccount.xToken})
    except Exception as e:
        print("登录出错")
        print(e)
    print("登录成功")
    return tokenGroup


def readData():
    userGroup = []  # 字典数组
    try:
        print("从目录中读取账户数据...")
        if haveDataFile() == False:
            print("未读取到数据，新建数据文件")
            dataFile = open(DATAFILENAME, "x")
            username = input("请输入账号：")
            password = input("请输入密码：")
            user = {"username": username, "password": password}
            userGroup.append(user)
            json.dump(userGroup, dataFile)
        dataFile = open(DATAFILENAME, "r")
        userGroup = json.load(dataFile)
    except Exception as e:
        print("读取数据出错")
        print(e)

    print("成功读取数据")
    return userGroup


def haveDataFile():
    path = os.getcwd()
    filelist = os.listdir(path)
    for file in filelist:
        if file == DATAFILENAME:
            return True
    return False


if __name__ == '__main__':
    print("脚本运行")
    userGroup = readData()
    lastTime = None
    while True:
        nowTime = time.time()
        nowHour = time.localtime()[3]
        if lastTime == None or nowTime-lastTime > 86400:
            tokenGroup = userLogin(userGroup)
            lastTime = nowTime
        for i in range(len(REPORTHOUR)):
            if nowHour >= REPORTHOUR[i][0] and nowHour < REPORTHOUR[i][1]:
                print("开始上报")
                for account in tokenGroup:
                    response = reportTem.reportTemperature(
                        account["cookies"], account["token"])
                    print(response.text)
        time.sleep(SLEEPTIME)
