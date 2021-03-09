import requests


def reportTemperature(cookie, token):
    url = "http://yiban.gxnu.edu.cn/dx-api/novel/reportTemperature"
    headers = {
        "Host": "yiban.gxnu.edu.cn",
        "Content-Type": "application/json;charset=utf-8",
        "x-access-token": token,
        "Origin": "http://yiban.gxnu.edu.cn",
        "Cookie": cookie
    }
    response = requests.post(url=url, headers=headers,
                             data="{\"temperature\": \"36.8\",\"remark\": \"\"}")
    return response
