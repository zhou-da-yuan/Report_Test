import os
from enum import verify

from common.faker_data import RandomDataGenerator
from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    log = Log()
    config = ConfigManager()
    sca_env = config.get_config()
    ini = INIManager(BASE_PATH + r'\api\variables.ini')

    file_path = os.path.join(BASE_PATH, r'Packages\fastweixin-master.zip')

    url = sca_env['base_url'] + f":{sca_env['api_port']}/openapi/v1/app-package/detect-file"
    project_name = ini.get_value('variables', 'projectName')
    sourceDetectName = f"sourceDetect{RandomDataGenerator().numerify(4)}"
    payload = {'projectName': project_name,
               'applicationName': f'{sourceDetectName}',
               'applicationVersion': 'test1',
               'applicationDescription': '这个是应用描述',
               'enablePoison': 'true',
               'isAddSocTask': 'false'
               }
    files = [
        ('file', ('fastweixin-master.zip', open(file_path, 'rb')))
    ]
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken']
    }
    try:
        response = RunMethod().api_run("POST", url, headers=headers, data=payload, files=files)

        if response.json()['code'] == 0:
            log.info(f"app上传检测成功：{response.json()}")
            print(f"app上传检测成功：{response.json()}")
            application_id = response.json()['data']['applicationId']
            scaTask_id = response.json()['data']['scaTaskId']
            if hasattr(response.json()['data'], 'socTaskId'):
                socTask_id = response.json()['data']['socTaskId']
                ini.set_value('variables', 'socTask_id', f'{socTask_id}')
            try:
                ini.set_value('variables', 'applicationId', f'{application_id}')
                ini.set_value('variables', 'scaTaskId', f'{scaTask_id}')
                ini.set_value('variables', 'sourceDetectName', f'{sourceDetectName}')
                ini.set_value('variables', 'sourceTaskId', f'{scaTask_id}')
                ini.save_config()
                log.info(f"applicationId、scaTaskId变量写入成功-{application_id}、{scaTask_id}")
                print(f"变量写入成功")
            except Exception as e:
                log.error(f"写入applicationId、scaTaskId变量失败-{e}")
        else:
            log.error(f"app上传检测失败：{response.json()}")
            print("检测项目名称" + project_name)
    except Exception as e:
        log.error(f"app上传检测接口请求错误：{e}")
        print(f"app上传检测接口请求错误：{e}")


if __name__ == '__main__':
    main()
