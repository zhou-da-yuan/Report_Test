import os

from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager


def main():
    log = Log()
    config = ConfigManager()
    sca_env = config.get_config()

    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = INIManager(BASE_PATH + r'\api\variables.ini')

    url = sca_env['base_url'] + ":8443/openapi/v1/project/delete"
    project_id = ini.get_value('variables', 'projectId', data_type=int)
    payload = {
        "projectId": project_id
    }
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
        'Content-Type': 'application/json'
    }

    response = RunMethod().api_run("POST", url, headers=headers, json=payload)

    if response.json()['code'] == 0:
        log.info(f"删除项目{project_id}成功：{response.json()}")
        print(f"删除项目{project_id}成功：{response.json()}")


if __name__ == '__main__':
    main()
