import os

from common.data_utils import JsonUtil
from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
config = ConfigManager()
sca_env = config.get_config()
ini = INIManager(BASE_PATH + r'\api\variables.ini')

# web接口获取应用信息
def get_VOInfoByTaskId(taskId):

    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/ApplicationPackageOverView/getApplicationVOInfoByTaskId?taskId={taskId}"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("获取VOIn信息成功")
            print(f"获取VOIn信息成功{response.json()}")
            return response.json()
        else:
            log.error("VOIn请求失败")
            print(f"VOIn请求失败{response.json()}")

    except Exception as e:
        log.error("获取VOIn信息失败")
        print(e)

# web接口获取检测组件、漏洞、许可证统计信息
def get_CVLCountTaskId(taskId):

    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/ApplicationPackageOverView/getApplicationCVLCountByTaskId?taskId={taskId}"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("获取CVLCount信息成功")
            print(f"获取CVLCount信息成功{response.json()}")
            return response.json()
        else:
            log.error("CVLCount请求失败")
            print(f"CVLCount请求失败{response.json()}")

    except Exception as e:
        log.error("获取CVLCountL信息失败")
        print(e)

# openapi接口根据任务id获取任务详情
def get_TaskDetails(taskId):
    url = sca_env["base_url"]+f":8443/openapi/v1/task/{taskId}"
    headers = {
        'OpenApiUserToken': '8c20b45e8a394c818493261357d4b90a'
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("获取TaskDetails情成功")
            print(f"获取TaskDetails成功{response.json()}")
            return response.json()
        else:
            log.error("获取TaskDetails请求失败")
            print(f"获取TaskDetails请求失败{response.json()}")

    except Exception as e:
        log.error("获取TaskDetails失败")
        print(e)


# 配置app检测基础应用信息
def set_appInfo(taskId):
    VOInfo = get_VOInfoByTaskId(taskId)
    CVLCount = get_CVLCountTaskId(taskId)
    TaskDetails = get_TaskDetails(taskId)

    objects = {
        'ini': ini,
        'VOInfo': VOInfo,
        'CVLCount': CVLCount,
        'TaskDetails': TaskDetails
    }

    json_util = JsonUtil('casedata/ApplicationInfo.json')  # 替换为你的 JSON 文件路径
    app_info = json_util.read_ApplicationInfo("appInfo", objects)
    print(app_info)


if __name__ == '__main__':
    set_appInfo(612780)
