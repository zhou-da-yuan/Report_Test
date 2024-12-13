import os

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
            log.info("获取应用信息成功")
            print(f"获取应用信息成功{response.json()}")
            return response.json()
        else:
            log.error("请求失败")
            print(f"请求失败{response.json()}")

    except Exception as e:
        log.error("获取应用信息失败")
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
            log.info("获取应用CVL信息成功")
            print(f"获取应用CVL信息成功{response.json()}")
            return response.json()
        else:
            log.error("CVL请求失败")
            print(f"CVL请求失败{response.json()}")

    except Exception as e:
        log.error("获取应用CVL信息失败")
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
            log.info("获取任务详情成功")
            print(f"获取任务详情成功{response.json()}")
            return response.json()
        else:
            log.error("获取任务详情请求失败")
            print(f"获取任务详情请求失败{response.json()}")

    except Exception as e:
        log.error("获取任务详情失败")
        print(e)


# 配置app检测基础应用信息
def set_appInfo(taskId):
    VOInfo = get_VOInfoByTaskId(taskId)
    CVLCount = get_CVLCountTaskId(taskId)
    TaskDetails = get_TaskDetails(taskId)
    case_data = { "应用名称": ini.get_value('variables', 'appDetectName'),"版本号": "test1",
                 "项目名称": ini.get_value('variables', 'projectname'), "应用资产属性":"有效资产",
                  "来源":"本地文件","供应链场景":"应用包审查分析","项目负责人":"xmirror",
                  "检测状态":f"组件依赖分析:{VOInfo["data"]["scaStatusStr"]}\n代码溯源分析:{VOInfo["data"]["socStatusStr"]}",
                  "恶意组件分析":"开启","可达性分析":"未开启",
                  "风险等级":f"{VOInfo["data"]["riskLevelStr"]}",
                  "组件数":f"{CVLCount['data']['componentNum']}",
                  "恶意组件数":f"{CVLCount['data']['poisonNum']}",
                  "漏洞数":f"{CVLCount['data']['vulNum']}",
                  "许可证数":f"{CVLCount['data']['licenseNum']}",
                  "许可证冲突数":f"{CVLCount['data']['licenseConflictNum']}",
                  "添加人":f"{VOInfo["data"]["userName"]}",
                  "开始检测时间":f"{TaskDetails['data']['detectStartTime']}",
                  "检测完成时间":f"{TaskDetails['data']['detectEndTime']}",
                  "检测时长":f"组件: {VOInfo["data"]["scaDetectTime"]}\n代码: {VOInfo["data"]["socDetectTime"]}",
                  "应用描述":"这个是应用描述"}
    print(case_data)


if __name__ == '__main__':
    set_appInfo()
