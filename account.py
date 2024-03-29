import requests
import re
import crypto


class account:
    LOGINURL = "https://mobile.yiban.cn/api/v4/passport/login"
    IAPP = "iapp173069"
    AUTHURL = "http://f.yiban.cn/iapp/index"
    HEADERS = {
        "User-Agent": "Yiban",
        "AppVersion": "5.0",
        "Origin": "https://c.uyiban.com",
    }
    CSRF = 114514
    COOKIES = {"csrf_token": CSRF} 

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def login(self):
        params = {
            "mobile": self.account,
            "password": crypto.rsaEncrypt(self.password),
            "ct": "2",
            "identify": "010045026872666",
        }
        loginRequest = requests.get(
            self.LOGINURL, params=params, headers=self.HEADERS, cookies=self.COOKIES
        ).json()
        if loginRequest is not None and str(loginRequest["response"]) == "100":
            self.access_token = loginRequest["data"]["user"]["access_token"]
            self.name = loginRequest['data']['user']['name']
            # return loginRequest
        else:
            raise Exception("账号或密码错误")

    def auth(self):
        params = {"act": self.IAPP, "v": self.access_token}
        locationRequest = requests.get(
            self.AUTHURL, params=params, allow_redirects=False
        )
        location1 = locationRequest.headers.get("location")
        if location1 is None:
            raise Exception("该用户未进行校方认证，无此APP权限")
        verifyRequest = re.findall(r"verify_request=(.*?)&", location1)[0]
        result_auth1 = requests.get(
            "http://47.107.170.15/oauth?verify_request=%s&yb_uid=%s&state=dx2"
            % (verifyRequest, self.yb_uid),
            allow_redirects=False,
        )  # 此处是学校的应用接口
        location2 = result_auth1.headers.get("location")
        if location2 is None:
            raise Exception("学校应用认证失败")
        result_auth2 = requests.get(
            "http://yiban.gxnu.edu.cn/dx-api/oauth/yb?verify_request=%s&yb_uid=%s&state=dx2"
            % (verifyRequest, self.yb_uid),
            allow_redirects=False,
        )
        location3 = result_auth2.headers.get("location")
        if location3 is None:
            raise Exception("获取回调跳转地址失败")
        result_auth3 = requests.get(
            "http://yiban.gxnu.edu.cn/login/callback/yb?verify_request=%s&yb_uid=%s&state=dx2"
            % (verifyRequest, self.yb_uid),
            allow_redirects=False,
        )
        if result_auth3.text != "":
            raise Exception("易知独秀未被授权，请先在客户端上登录并授权易知独秀")
        self.dxtoken = re.findall(
            r"dx-token=(.*?);", result_auth3.headers.get("Set-Cookie")
        )[0]

    def getxToken(self):
        self.cookies = "dx-token=%s" % (self.dxtoken)
        headers = {
            "Host": "yiban.gxnu.edu.cn",
            "Cookie": self.cookies,
            "X-Requested-With": "XMLHttpRequest",
        }  # 此处需要发送Ajax请求，服务器才能正确响应
        self.xToken = requests.get(
            "http://yiban.gxnu.edu.cn/v4/login", headers=headers
        ).headers.get("X-Access-Token")
