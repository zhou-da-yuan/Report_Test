import urllib3 as urllib3
from requests import session

from common.log import Log


class RunMethod:
    log = Log()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self):
        """session管理器"""
        self.s = session()
        self.s.verify = False

    def api_run(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        return self.s.request(method, url, params=params, data=data, json=json, headers=headers, verify=False, **kwargs)

    def close_session(self):
        """关闭session"""
        self.s.close()

if __name__ == '__main__':
    r = RunMethod()
    result = r.api_run('get', 'https://www.baidu.com')
    print(result.cookies)