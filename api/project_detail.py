import os

from common.log import Log
from common.ini_manager import INIManager
from common.request import RunMethod
from common.yaml_utils import ConfigManager

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
config = ConfigManager()
sca_env = config.get_config()
ini = INIManager(BASE_PATH + r'\api\variables.ini')

def project_exist():

    projectId = ini.get_value("variables","projectId")
    url = sca_env['base_url'] + f":{sca_env['api_port']}/openapi/v1/project/detail/{projectId}"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'OpenApiUserToken': sca_env['OpenApiUserToken']
    }

    flag = False
    try:
        response = RunMethod().api_run("GET", url, headers=headers, data=payload)
        if response.json()['code'] == 0:
            flag = True
    except Exception as e:
        log.error(f"状态查询异常: {e}")

    return flag


