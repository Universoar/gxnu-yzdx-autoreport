import requests
import re


class account:
    # 感谢https://github.com/xlc520/yiban_auto_submit提供的接口！
    LOGINURL = "https://mobile.yiban.cn/api/v3/passport/login"  # 不需要加密密码直接登录的接口
    IAPP = "iapp173069"
    AUTHURL = "http://f.yiban.cn/iapp/index"

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def login(self):
        params = {
            "mobile": self.account,
            "imei": "0",
            "password": self.password
        }
        loginRequest = requests.get(self.LOGINURL, params=params).json()
        if loginRequest is not None and str(loginRequest["response"]) == "100":
            self.access_token = loginRequest["data"]["user"]["access_token"]
            self.yb_uid = loginRequest["data"]["user"]["id"]
            # return loginRequest
        else:
            raise Exception("账号或密码错误")

    def auth(self):
        params = {
            "act": self.IAPP,
            "v": self.access_token
        }
        locationRequest = requests.get(
            self.AUTHURL, params=params, allow_redirects=False)
        location1 = locationRequest.headers.get("location")
        if location1 is None:
            raise Exception("该用户未进行校方认证，无此APP权限")
        verifyRequest = re.findall(r"verify_request=(.*?)&", location1)[0]
        result_auth1 = requests.get(
            "http://47.107.170.15/oauth?verify_request=%s&yb_uid=%s&state=dx2" % (
                verifyRequest, self.yb_uid), allow_redirects=False)  # 此处是学校的应用接口
        location2 = result_auth1.headers.get("location")
        if location2 is None:
            raise Exception("学校应用认证失败")
        result_auth2 = requests.get("http://yiban.gxnu.edu.cn/dx-api/oauth/yb?verify_request=%s&yb_uid=%s&state=dx2" % (
            verifyRequest, self.yb_uid), allow_redirects=False)
        self.phpseedid = re.findall(
            r"PHPSESSID=(.*?);", result_auth2.headers.get("Set-Cookie"))[0]
        self.yzdxToken = re.findall(
            r"YZDXdxUserToken=(.*?);", result_auth2.headers.get("Set-Cookie"))[0]

    def getxToken(self):
        self.cookies = "PHPSESSID=%s; YZDXdxUserToken=%s" % (
            self.phpseedid, self.yzdxToken)
        self.xToken = requests.get(
            "http://yiban.gxnu.edu.cn/dx-api/user/getUserInfo", cookies={"PHPSESSID": self.phpseedid, "YZDXdxUserToken": self.yzdxToken}).headers.get("X-Access-Token")
