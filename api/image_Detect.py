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
    sca_env = config.get_config(config.get_use())
    ini = INIManager(BASE_PATH + r'\api\variables.ini')

    file_path = os.path.join(BASE_PATH, r'Packages\alpine.tar')

    url = sca_env['base_url'] + ":8443/openapi/v1/image/detect-file"
    project_name = ini.get_value('variables', 'projectName')
    payload = {'projectName': project_name,
               'applicationName': f'Report_Test{RandomDataGenerator().numerify(4)}',
               'applicationVersion': '1.0',
               'applicationDescription': '这个是应用描述',
               'enablePoison': 'true',
               'sensitive': 'true'
               }
    files = [
        ('file', ('alpine.tar', open(file_path, 'rb'), 'application/zip'))
    ]
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    try:
        response = RunMethod().api_run("POST", url, headers=headers, data=payload, files=files)

        if response.json()['code'] == 0:
            log.info(f"image上传检测成功：{response.json()}")
            print(f"image上传检测成功：{response.json()}")
            application_id = response.json()['data']['applicationId']
            scaTask_id = response.json()['data']['scaTaskId']
            try:
                ini.set_value('variables', 'applicationId', f'{application_id}')
                ini.set_value('variables', 'scaTaskId', f'{scaTask_id}')
                ini.save_config()
                log.info(f"applicationId、scaTaskId变量写入成功-{application_id}、{scaTask_id}")
                print(f"变量写入成功")
            except Exception as e:
                log.error(f"写入applicationId、scaTaskId变量失败-{e}")
        else:
            log.error(f"image上传检测失败：{response.json()}")
            print("检测项目名称" + project_name)
    except Exception as e:
        log.error(f"image上传检测接口请求错误：{e}")
        print(f"image上传检测接口请求错误：{e}")


if __name__ == '__main__':
    main()