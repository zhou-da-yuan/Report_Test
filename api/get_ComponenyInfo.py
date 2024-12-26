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
               'language': language,
               'versionOrder': "ascend"
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

# web接口获取镜像检测软件包依赖包信息
def get_dependencies(hashCode):
    url = sca_env['base_url'] + f"/sca/api-v1/asset/image/package/{hashCode}/dependencies?pageNum=1&pageSize=100"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }

    try:
        response = RunMethod().api_run("GET", url, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_dependencies获取镜像检测软件包依赖包信息成功")
            print(f"et_dependencies获取镜像检测软件包依赖包信息成功{response.json()}")
            return response.json()
        else:
            log.error(f"et_dependencies获取镜像检测软件包依赖包信息失败{response.json()}")
            print(f"et_dependencies获取镜像检测软件包依赖包信息失败{response.json()}")

    except Exception as e:
        log.error(f"et_dependencies获取镜像检测软件包依赖包信息失败-{e}")
        print(e)


class InfoGet:
    def __init__(self, taskId_type, ComponentInfo):
        self.taskId = ini.get_value('variables', taskId_type)
        self.ComponentInfo = ComponentInfo
        self.objects = None
        self.json_util = JsonUtil(r'casedata\ComponentInfo.json')  # 使用json组件信息模板

        try:
            self._initialize_objects()
            log.info(f"componentName: {self.ComponentInfo['componentName']} 接口数据获取成功！")
        except Exception as e:
            log.error(f"componentName: {self.ComponentInfo['componentName']} 接口数据获取失败,请查看日志-{e}")

    def _initialize_objects(self):
        """初始化接口数据"""
        data = {
            "componentName": self.ComponentInfo['componentName'],
            "language": self.ComponentInfo['language'],
            "vendor": self.ComponentInfo['vendor'],
            "version": self.ComponentInfo['version'],
            "hashCode": self.ComponentInfo['hashCode']
        }

        self.objects = {
            'ini': ini,
            'ComponentInfo': self.ComponentInfo,
            'ComponentVersionInfo': get_OtherComponentVersion(data['hashCode'], data['language'])['data'],
            'ComponentDependencyInfo': get_ComponentDependency(
                self.taskId,
                componentName=data['componentName'],
                language=data['language'],
                vendor=data['vendor'],
                version=data['version'],
                hashCode=data['hashCode']
            )['data']['records'],
            'ComponentESInfo': get_ComponentESInfo(
                self.taskId,
                componentName=data['componentName'],
                language=data['language'],
                version=data['version'],
                hashCode=data['hashCode']
            )['data'],
            'ComponentDetailInfo': get_ComponentDetail(
                componentName=data['componentName'],
                language=data['language'],
                vendor=data['vendor'],
                version=data['version']
            )['data'],
            'ComponentVulList': get_ComponentVulList(
                self.taskId,
                hashCode=data['hashCode']
            )['data']
        }

    def _clean_app_info(self, app_info, transformations):
        """清洗app_info中的数据"""
        if self.objects is None:
            error_msg = f"componentName: {self.ComponentInfo['componentName']} InfoGet接口数据初始化失败"
            log.error(error_msg)
            return error_msg

        data_Trans = DataUtils()
        for key, transform_func in transformations.items():
            if key in app_info:
                try:
                    app_info[key] = transform_func(app_info[key])
                except Exception as e:
                    log.error(
                        f"componentName: {self.ComponentInfo['componentName']} 字段 '{key}' 数据清洗出错 - {e}")
                    continue

        return app_info

    def _destroy_objects(self):
        """销毁应用信息对象"""
        if self.objects:
            for obj_name in list(self.objects.keys()):
                del self.objects[obj_name]
            self.objects = None

    # 获取源码检测检出组件信息
    def get_source_appInfo(self):
        if self.objects is None:
            return self._error_response("源码检测检出组件信息")

        app_info = self.json_util.read_ApplicationInfo("sourceInfo", self.objects)

        transformations = {
            '风险等级': DataUtils().riskLevel_Trans,
            '依赖方式': DataUtils().dependencyType_Trans,
            '恶意组件': DataUtils().is_Trans,
            '私有组件': DataUtils().is_Trans,
            '许可证信息': DataUtils().license_Trans,
            '无漏洞可用版本': DataUtils().noVulVersion_Trans,
            '组件依赖路径': DataUtils().dependencyPath_Trans,
            '漏洞数': DataUtils().vulCount,
            '漏洞编号': DataUtils().vulNumber,
        }

        cleaned_app_info = self._clean_app_info(app_info, transformations)
        self._destroy_objects()

        return cleaned_app_info

    # 获取二进制检测检出组件信息
    def get_binary_appInfo(self):
        if self.objects is None:
            return self._error_response("二进制检测检出组件信息")

        app_info = self.json_util.read_ApplicationInfo("binaryInfo", self.objects)

        transformations = {
            '风险等级': DataUtils().riskLevel_Trans,
            '恶意组件': DataUtils().is_Trans,
            '私有组件': DataUtils().is_Trans,
            '许可证信息': DataUtils().license_Trans,
            '无漏洞可用版本': DataUtils().noVulVersion_Trans,
            '组件依赖路径': DataUtils().dependencyPath_Trans,
            '漏洞数': DataUtils().vulCount,
            '漏洞编号': DataUtils().vulNumber,
        }

        cleaned_app_info = self._clean_app_info(app_info, transformations)
        self._destroy_objects()

        return cleaned_app_info

    # 获取镜像检测检出软件包信息
    def get_image_appInfo(self):
        if self.objects is None:
            return self._error_response("镜像检测检出软件包信息")

        keys_to_remove = ["ComponentVersionInfo", "ComponentESInfo"]
        [self.objects.pop(key, None) for key in keys_to_remove]

        dependenciesInfo = get_dependencies(self.ComponentInfo['hashCode'])['data']
        self.objects.update({"dependenciesInfo": dependenciesInfo})

        app_info = self.json_util.read_ApplicationInfo("imageInfo", self.objects)

        transformations = {
            '风险等级': DataUtils().riskLevel_Trans,
            '许可证数': DataUtils().licenseCount,
            '许可证信息': DataUtils().license_Trans,
            '漏洞数': DataUtils().vulCount_image,
            '漏洞编号': DataUtils().vulNumber,
            '依赖包名称': DataUtils().dependencies_Trans,
            '检出路径数': DataUtils().dependencyCount,
            '依赖包数': int
        }

        cleaned_app_info = self._clean_app_info(app_info, transformations)
        self._destroy_objects()

        return cleaned_app_info

    def _error_response(self, info_type):
        """构建错误响应"""
        error_msg = f"componentName: {self.ComponentInfo['componentName']} {info_type}接口数据初始化失败"
        log.error(error_msg)
        return error_msg


if __name__ == '__main__':
    # taskId = ini.get_value('variables', 'sourcetaskid')
    # ComponentListInfo = get_ComponentList(taskId)['data']['records']
    # for ComponentInfo in ComponentListInfo:
    #     info = InfoGet("sourcetaskid", ComponentInfo)
    #     print(info.get_source_appInfo())

    # taskId = ini.get_value('variables', 'binarytaskid')
    # ComponentListInfo = get_ComponentList(taskId)['data']['records']
    # for ComponentInfo in ComponentListInfo:
    #     info = InfoGet("binarytaskid", ComponentInfo)
    #     print(info.get_binary_appInfo())

    taskId = ini.get_value('variables', 'imagetaskid')
    ComponentListInfo = get_ComponentList(taskId)['data']['records']
    for ComponentInfo in ComponentListInfo:
        info = InfoGet("imagetaskid", ComponentInfo)
        print(info.get_image_appInfo())

