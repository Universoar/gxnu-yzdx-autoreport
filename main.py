import requests
import os
import sys
import time
import account
import json

DATAFILENAME = "data.json"  # 数据文件的名称
REPORTHOUR = [[7, 10], [12, 15]]  # 上报体温的时间段，单位为小时
SLEEPTIME = 1800  # 检查上报时间的频率，单位为秒


def userLogin(userGroup):
    tokenGroup = []  # 字典数组
    try:
        for user in userGroup:
            userAccount = account.account(user["username"], user["password"])
            userAccount.login()
            userAccount.auth()
            userAccount.getxToken()
            tokenGroup.append(
                {"cookies": userAccount.dxtoken, "token": userAccount.xToken}
            )
        print(
            "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "登录成功，现在每隔",
            "{}".format(SLEEPTIME),
            "秒就会检查一次上报时间",
        )
    except Exception as e:
        print(
            "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), "登录出错"
        )
        print(e)
        os.system("pause")
        sys.exit()
    return tokenGroup


def readData():
    userGroup = []  # 字典数组
    try:
        print(
            "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "从目录中读取用户数据...",
        )
        if haveDataFile() == False:
            print(
                "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                "未读取到数据，新建数据文件",
            )
            username = input("请输入账号：")
            password = input("请输入密码：")
            if username == "" or password == "":
                raise Exception("数据不能为空")
            user = {"username": username, "password": password}
            userGroup.append(user)
            with open(DATAFILENAME, "w") as dataFile:
                json.dump(userGroup, dataFile)
        with open(DATAFILENAME, "r") as dataFile:
            userGroup = json.load(dataFile)
        print(
            "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "成功读取数据",
        )
    except Exception as e:
        print(
            "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "读取数据出错",
        )
        print(e)
        os.system("pause")
        sys.exit()
    return userGroup


def haveDataFile():
    path = os.getcwd()
    filelist = os.listdir(path)
    for file in filelist:
        if file == DATAFILENAME:
            return True
    return False


def reportTemperature(cookie, token):
    url = "http://yiban.gxnu.edu.cn/v4/affairs/health-report/create"
    headers = {
        "Host": "yiban.gxnu.edu.cn",
        "Content-Type": "application/json;charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "X-Access-Token": token,
        "Origin": "http://yiban.gxnu.edu.cn",
        "Cookie": cookie,
    }
    body = {"data": {"temperature": "36.8", "remark": ""}}
    response = requests.post(url=url, headers=headers, json=body)
    return response


if __name__ == "__main__":
    print("[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), "脚本运行")
    lastTime = None
    isReport = False
    while True:
        isReportTime = False
        nowTime = time.time()
        nowHour = time.localtime()[3]
        if lastTime == None or nowTime - lastTime > 86400:  # 每天更新一次tokenGroup
            userGroup = readData()
            tokenGroup = userLogin(userGroup)
            lastTime = nowTime
        for i in range(len(REPORTHOUR)):
            if nowHour >= REPORTHOUR[i][0] and nowHour < REPORTHOUR[i][1]:
                isReportTime = True
            if (
                nowHour >= REPORTHOUR[i][0]
                and nowHour < REPORTHOUR[i][1]
                and isReport == False
            ):
                print(
                    "[{}]".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    "开始上报",
                )
                for account in tokenGroup:
                    response = reportTemperature(account["cookies"], account["token"])
                    responseData = response.json()
                    if responseData["code"] == 200:
                        print(
                            "[{}]".format(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            ),
                            "上报成功，体温36.8°C",
                        )
                    else:
                        print(
                            "[{}]".format(
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            ),
                            "上报失败，返回信息：{}".format(responseData["msg"]),
                        )
                isReport = True
        if isReportTime == False:
            isReport = False
        time.sleep(SLEEPTIME)
