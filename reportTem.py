import requests
import io
import time
import schedule
import sys
from getToken import getToken


def reportTemperature(cookie, token):
    url = "http://yiban.gxnu.edu.cn/dx-api/novel/reportTemperature"
    headers = {
        "Host": "yiban.gxnu.edu.cn",
        "Content-Type": "application/json;charset=utf-8",
        "x-access-token": token,
        "Origin": "http://yiban.gxnu.edu.cn",
        "Cookie": cookie
    }
    response = requests.post(url=url, headers=headers, data="{\"temperature\": \"36.8\",\"remark\": \"\"}")


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
account = input("请输入账户")
password = input("请输入密码")
try:
    gt = getToken(account, password)
    gt.login()
    gt.auth()
    gt.getxToken()
    cookie = gt.cookies
    token = gt.xToken
    print("ok")

    schedule.every().day.at("07:01").do(reportTemperature, gt.cookies, gt.xToken)
    schedule.every().day.at("12:01").do(reportTemperature, gt.cookies, gt.xToken)
    while True:
        schedule.run_pending()
        time.sleep(10)
except Exception as e:
    print("f")
    print(e)
