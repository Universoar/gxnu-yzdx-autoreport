import requests


def reportTemperature(cookie, token):
    url = 'http://yiban.gxnu.edu.cn/v4/affairs/health-report/create'
    headers = {
        'Host': 'yiban.gxnu.edu.cn',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Access-Token': token,
        'Origin': 'http://yiban.gxnu.edu.cn',
        'Cookie': cookie
    }
    body = {'data': {
        'temperature': '36.8',
        'remark': ''
    }
    }
    response = requests.post(url=url, headers=headers,
                             json=body)
    return response
