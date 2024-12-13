import os

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

    file_path = os.path.join(BASE_PATH, r'Packages\curl.zst')

    url = sca_env['base_url'] + ":8443/openapi/v1/binary/detect-file"
    project_name = ini.get_value('variables', 'projectName')
    binaryDetectName = f"Report_Test{RandomDataGenerator().numerify(4)}"
    payload = {'projectName': project_name,
               'applicationName': binaryDetectName,
               'applicationVersion': '1.0',
               'applicationDescription': '这个是应用描述',
               'enablePoison': 'true',
               'isAddRvcTask': 1
               }
    files = [
        ('file', ('curl.zst', open(file_path, 'rb'), 'application/zip'))
    ]
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    try:
        response = RunMethod().api_run("POST", url, headers=headers, data=payload, files=files)

        if response.json()['code'] == 0:
            log.info(f"binary上传检测成功：{response.json()}")
            print(f"binary上传检测成功：{response.json()}")
            application_id = response.json()['data']['applicationId']
            scaTask_id = response.json()['data']['scaTaskId']
            try:
                ini.set_value('variables', 'applicationId', f'{application_id}')
                ini.set_value('variables', 'scaTaskId', f'{scaTask_id}')
                ini.set_value('variables', 'binaryDetectName', f'{binaryDetectName}')
                ini.set_value('variables', 'binaryTaskId', f'{scaTask_id}')
                ini.save_config()
                log.info(f"applicationId-{application_id}、scaTaskId-{scaTask_id}变量写入成功")
                print(f"applicationId-{application_id}、scaTaskId-{scaTask_id}变量写入成功")
            except Exception as e:
                log.error(f"写入applicationId、scaTaskId变量失败-{e}")
        else:
            log.error(f"binary上传检测失败：{response.json()}")
            print("检测项目名称" + project_name)
    except Exception as e:
        log.error(f"binary上传检测接口请求错误：{e}")
        print(f"binary上传检测接口请求错误：{e}")


if __name__ == '__main__':
    main()
