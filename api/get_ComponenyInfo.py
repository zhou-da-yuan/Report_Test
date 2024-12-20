import os

from common.data_utils import JsonUtil, DataUtils
from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
config = ConfigManager()
sca_env = config.get_config()
ini = INIManager(BASE_PATH + r'\api\variables.ini')


# web接口获取组件列表信息
def get_ComponentList(taskId):
    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/Component/getComponentListByTaskId"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    payload = {
        "pageNum": 1,
        "pageSize": 1000,
        "taskId": taskId
    }

    try:
        response = RunMethod().api_run("POST", url, json=payload, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentList-获取组件列表成功")
            print(f"get_ComponentList-获取组件列表成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentList-组件列表请求失败{response.json()}")
            print(f"get_ComponentList-组件列表请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentList-获取组件列表请求出错-{e}")
        print(e)


# web接口获取组件无漏洞可用版本
def get_OtherComponentVersion(hashcode, language):
    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/Component/getOtherComponentVersionESPage"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    payload = {'pageNum': 1,
               'pageSize': 1000,
               'hashCode': hashcode,
               'language': language
               }

    try:
        response = RunMethod().api_run("POST", url, json=payload, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_OtherComponentVersion-获取组件无漏洞可用版本成功")
            print(f"get_OtherComponentVersion-获取组件无漏洞可用版本成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_OtherComponentVersion-组件无漏洞可用版本请求失败{response.json()}")
            print(f"get_OtherComponentVersion-组件无漏洞可用版本请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_OtherComponentVersion-获取组件无漏洞可用版本请求出错-{e}")
        print(e)


# web接口获取组件依赖
def get_ComponentDependency(taskId, **kwargs):
    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/Component/getDependencyLevelPathById"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    payload = {"pageNum": 1,
               "pageSize": 100,
               "taskId": taskId,
               "componentName": kwargs['componentName'],
               "language": kwargs['language'],
               "vendor": kwargs['vendor'],
               "version": kwargs['version'],
               "hashCode": kwargs['hashCode']
               }

    try:
        response = RunMethod().api_run("POST", url, json=payload, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentDependency-获取组件依赖成功")
            print(f"get_ComponentDependency-获取组件依赖成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentDependency-获取组件依赖请求失败{response.json()}")
            print(f"get_ComponentDependency-获取组件依赖请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentDependency-获取组件依赖请求出错-{e}")
        print(e)


# web接口获取组件ES详情信息
def get_ComponentESInfo(taskId, **kwargs):
    url = sca_env['base_url'] + (f"/sca/api-v1/commonDetail/Component/getComponentESInfoByCondition?"
                                 f"taskId={taskId}"
                                 f"&language={kwargs['language']}"
                                 f"&version={kwargs['version']}"
                                 f"&componentName={kwargs['componentName']}"
                                 f"&hashCode={kwargs['hashCode']}"
                                 )
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentESInfo获取组件ES详情信息成功")
            print(f"get_ComponentESInfo获取组件ES详情信息成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentESInfo获取组件ES详情信息请求失败{response.json()}")
            print(f"get_ComponentESInfo获取组件ES详情信息请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentESInfo获取组件ES详情信息请求失败-{e}")
        print(e)


# openapi接口获取组件详情
def get_ComponentDetail(**kwargs):
    url = sca_env['base_url'] + (f":8443/openapi/v1/component/detail?"
                                 f"name={kwargs['componentName']}"
                                 f"&language={kwargs['language']}"
                                 f"&vendor={kwargs['vendor']}"
                                 f"&version={kwargs['version']}"
                                 )
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentDetail-获取组件详情信息成功")
            print(f"get_ComponentDetail-获取组件详情信息成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentDetail-获取组件详情信息请求失败{response.json()}")
            print(f"get_ComponentDetail-获取组件详情信息请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentDetail-获取组件详情信息请求出错-{e}")
        print(e)


# web接口获取组件漏洞列表
def get_ComponentVulList(taskId, **kwargs):
    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/Component/getVulListByComponentId"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    payload = {"pageNum": 1,
               "pageSize": 1000,
               "taskId": taskId,
               "hashCode": kwargs['hashCode']
               }

    try:
        response = RunMethod().api_run("POST", url, json=payload, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentVulList-获取组件漏洞列表成功")
            print(f"get_ComponentVulList-获取组件漏洞列表成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentVulList-获取组件漏洞列表请求失败{response.json()}")
            print(f"get_ComponentVulList-获取组件漏洞列表请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentVulList-获取组件漏洞列表失败-{e}")
        print(e)


class InfoGet:
    # 初始化获取接口信息
    def __init__(self, taskId_type, record_index, ComponentList):
        self.taskId = ini.get_value('variables', taskId_type)
        self.index = record_index
        self.ComponentList = ComponentList
        # 获取接口数据
        try:
            # ComponentListInfo = get_ComponentList(self.taskId)['data']['records'][self.index]
            ComponentListInfo = self.ComponentList[self.index]
            data = {"componentName": ComponentListInfo['componentName'],
                    "language": ComponentListInfo['language'],
                    "vendor": ComponentListInfo['vendor'],
                    "version": ComponentListInfo['version'],
                    "hashCode": ComponentListInfo['hashCode']}
            ComponentVersion = get_OtherComponentVersion(data['hashCode'], data['language'])
            ComponentDependencyInfo = get_ComponentDependency(self.taskId,
                                                              componentName=data['componentName'],
                                                              language=data['language'],
                                                              vendor=data['vendor'],
                                                              version=data['version'],
                                                              hashCode=data['hashCode']
                                                              )
            ComponentESInfo = get_ComponentESInfo(self.taskId,
                                                  componentName=data['componentName'],
                                                  language=data['language'],
                                                  version=data['version'],
                                                  hashCode=data['hashCode'])
            ComponentDetailInfo = get_ComponentDetail(componentName=data['componentName'],
                                                      language=data['language'],
                                                      vendor=data['vendor'],
                                                      version=data['version']
                                                      )
            ComponentVulList = get_ComponentVulList(self.taskId,
                                                    hashCode=data['hashCode']
                                                    )

            self.objects = {
                'ini': ini,
                'ComponentListInfo': ComponentListInfo,
                'ComponentVersionInfo': ComponentVersion['data']['records'],
                'ComponentDependencyInfo': ComponentDependencyInfo['data']['records'],
                'ComponentESInfo': ComponentESInfo['data'],
                'ComponentDetailInfo': ComponentDetailInfo['data'],
                'ComponentVulList': ComponentVulList['data']
            }
            log.info(
                f"componentName: {self.ComponentList[self.index]["componentName"]} index：{self.index} 接口数据获取成功！")
        except Exception as e:
            self.objects = None
            log.error(
                f"componentName: {ComponentList[self.index]["componentName"]} index: {self.index} 接口数据获取失败,请查看日志-{e}")

        self.json_util = JsonUtil(r'casedata\ComponentInfo.json')  # 替换为你的 JSON 文件路径

    # 配置app检测基础应用信息
    def get_source_appInfo(self):
        data_Trans = DataUtils()
        if self.objects is None:
            log.error(
                f"componentName: {self.ComponentList[self.index]["componentName"]} index：{self.index} InfoGet接口数据初始化失败")
            return f"componentName: {self.ComponentList[self.index]["componentName"]} index：{self.index} InfoGet接口数据初始化失败"
        app_info = self.json_util.read_ApplicationInfo("sourceInfo", self.objects)

        # 接口数据二次清洗
        try:
            app_info['风险等级'] = data_Trans.riskLevel_Trans(app_info['风险等级'])
            app_info['依赖方式'] = data_Trans.dependencyType_Trans(app_info['依赖方式'])
            app_info['恶意组件'] = data_Trans.is_Trans(app_info['恶意组件'])
            app_info['私有组件'] = data_Trans.is_Trans(app_info['私有组件'])
            app_info['许可证信息'] = data_Trans.license_Trans(app_info['许可证信息'])
            app_info['无漏洞可用版本'] = data_Trans.noVulVersion_Trans(app_info['无漏洞可用版本'])
            app_info['组件依赖路径'] = data_Trans.dependencyPath_Trans(app_info['组件依赖路径'])
            app_info['漏洞数'] = data_Trans.vulCount(app_info['漏洞数'])
            app_info['漏洞编号'] = data_Trans.vulNumber(app_info['漏洞编号'])
        except Exception as e:
            log.error(
                f"componentName: {self.ComponentList[self.index]["componentName"]} index：{self.index} app_info数据清洗出错-{e}")

        # 销毁应用信息对象
        for obj_name in list(self.objects.keys()):
            del self.objects[obj_name]

        return app_info


if __name__ == '__main__':
    taskId = ini.get_value('variables', 'scataskid')
    ComponentListInfo = get_ComponentList(taskId)['data']['records']
    for i in range(len(ComponentListInfo)):
        info = InfoGet("scataskid", i, ComponentListInfo)
        print(info.get_source_appInfo())
    # info = InfoGet("scataskid", 0)
    # print(info.get_source_appInfo())
    # f = DataUtils()
    # ComponentListInfo = get_ComponentList(613243)['data']['records'][0]
    # data = {"componentName": ComponentListInfo['componentName'],
    #         "language": ComponentListInfo['language'],
    #         "vendor": ComponentListInfo['vendor'],
    #         "version": ComponentListInfo['version'],
    #         "hashCode": ComponentListInfo['hashCode']}
    # ComponentVulList = get_ComponentVulList(taskId=613243,
    #                                         hashCode=data['hashCode']
    #
    #                                         )
    # print(f"{ComponentVulList['data']['records']}")
    # print(f.vulNumber(f"{ComponentVulList['data']['records']}"))
