import os

from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager


def main():
    log = Log()
    config = ConfigManager()
    sca_env = config.get_config(config.get_use())

    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = INIManager(BASE_PATH + r'\api\variables.ini')

    url = sca_env['base_url'] + "/sca/api-v1/asset/report/deleteBatch"
    report_id = ini.get_value('variables', 'reportid', data_type=int)
    payload = {
        "idList": [report_id]
    }
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
        'Content-Type': 'application/json'
    }

    try:
        response = RunMethod().api_run("POST", url, headers=headers, json=payload)

        if response.json()['code'] == 0:
            log.info(f"删除报告{report_id}成功：{response.json()}")
            print(f"删除报告{report_id}成功：{response.json()}")
        else:
            log.error(f"删除报告{report_id}失败：{response.json()}")
            print(f"删除报告{report_id}失败：{response.json()}")
    except Exception as e:
        log.error(f"删除报告接口请求错误：{e}")
        print(f"删除报告接口请求错误：{e}")


if __name__ == '__main__':
    main()
