import os


from common.data_utils import JsonUtil, DataUtils
from common.excel_utils import Excel
from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
config = ConfigManager()
sca_env = config.get_config()

# web接口获取应用信息
def get_VOInfoByTaskId(taskId):

    url = sca_env['base_url'] + f":{sca_env['web_port']}/sca/api-v1/commonDetail/ApplicationPackageOverView/getApplicationVOInfoByTaskId?taskId={taskId}"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("获取VOInfo信息成功")
            print(f"获取VOInfo信息成功{response.json()}")
            return response.json()
        else:
            log.error(f"VOInfo请求失败{response.json()}")
            print(f"VOInfo请求失败{response.json()}")

    except Exception as e:
        log.error("获取VOIn信息失败")
        print(e)

# web接口获取检测组件、漏洞、许可证统计信息
def get_CVLCountTaskId(taskId):

    url = sca_env['base_url'] + f":{sca_env['web_port']}/sca/api-v1/commonDetail/ApplicationPackageOverView/getApplicationCVLCountByTaskId?taskId={taskId}"
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
            log.error(f"CVLCount请求失败{response.json()}")
            print(f"CVLCount请求失败{response.json()}")

    except Exception as e:
        log.error("获取CVLCountL信息失败")
        print(e)

# # openapi接口根据任务id获取任务详情
# # 目前没有使用
# def get_TaskDetails(taskId):
#     url = sca_env["base_url"]+f":{sca_env['api_port']}/openapi/v1/task/{taskId}"
#     headers = {
#         'OpenApiUserToken': sca_env['OpenApiUserToken']
#     }
#
#     try:
#         response = RunMethod().api_run("GET", url, headers=headers)
#         if response.json()['code'] == 0:
#             log.info("获取TaskDetails情成功")
#             print(f"获取TaskDetails成功{response.json()}")
#             return response.json()
#         else:
#             log.error(f"获取TaskDetails请求失败{response.json()}")
#             print(f"获取TaskDetails请求失败{response.json()}")
#
#     except Exception as e:
#         log.error("获取TaskDetails失败")
#         print(e)

class InfoGet:
    # 初始化获取接口信息
    def __init__(self,taskId_type):
        ini = INIManager(BASE_PATH + r'\api\variables.ini')
        self.taskId = ini.get_value('variables', taskId_type)

        VOInfo = get_VOInfoByTaskId(self.taskId)
        CVLCount = get_CVLCountTaskId(self.taskId)
        # TaskDetails = get_TaskDetails(self.taskId)
        self.objects = {
            'ini': ini,
            'VOInfo': VOInfo,
            'CVLCount': CVLCount
            # 'TaskDetails': TaskDetails
        }
        self.json_util = JsonUtil(r'casedata\ApplicationInfo.json')  # 替换为你的 JSON 文件路径


    # 获取源码检测基础应用信息
    def get_source_appInfo(self):

        app_info = self.json_util.read_ApplicationInfo("sourceInfo", self.objects)
        # 数据清理
        app_info["可达性分析"] = "已开启" if app_info["可达性分析"] else "未开启"
        # 销毁应用信息对象
        for obj_name in list(self.objects.keys()):
            del self.objects[obj_name]

        return app_info

    # 获取二进制检测基础应用信息
    def get_binary_appInfo(self):

        app_info = self.json_util.read_ApplicationInfo("binaryInfo", self.objects)
        # 数据清理
        app_info["可达性分析"] = "已开启" if app_info["可达性分析"] else "未开启"
        # 销毁应用信息对象
        for obj_name in list(self.objects.keys()):
            del self.objects[obj_name]

        return app_info

    # 获取镜像检测基础应用信息
    def get_image_appInfo(self):

        app_info = self.json_util.read_ApplicationInfo("imageInfo", self.objects)
        # 销毁应用信息对象
        for obj_name in list(self.objects.keys()):
            del self.objects[obj_name]

        return app_info


if __name__ == '__main__':
    ini = INIManager(BASE_PATH + r'\api\variables.ini')
    taskId = ini.get_value('variables', 'binarytaskid')

    VOInfo = get_VOInfoByTaskId(taskId)
    CVLCount = get_CVLCountTaskId(taskId)


    # # 测试
    # excel = Excel(BASE_PATH + r'\Reports\二进制检测报告.xlsx', 'D://供应链场景excel报告.xlsx', "sheet标题及表头测试")
    #
    # report_data = excel.get_ApplicationInfo()
    # info = InfoGet("binaryTaskId")
    # case_data = info.get_binary_appInfo()
    #
    # data_utils = DataUtils()
    # comparison_results = data_utils.compare_dicts(report_data, case_data)
    #
    # flag = True
    # for key, equal, report_value, case_value in comparison_results:
    #     if equal is None:
    #         log.warning(f"Key '{key}' not found in report_data.")
    #         print(f"Key '{key}' not found in report_data.")
    #     elif equal:
    #         log.info(f"Key '{key}' 匹配成功！")
    #     else:
    #         log.error(f"Key '{key}': Values differ - Report: '{report_value}', Case: '{case_value}'")
    #         flag = False
    # if flag:
    #     log.info(f"所有应用信息匹配成功")
    #     assert True, f"所有应用信息匹配成功"
    # else:
    #     log.error(f"部分应用信息匹配失败，请查看日志")
    #     assert False, f"部分应用信息匹配失败，请查看日志"