import json
import os

from common.request import RunMethod
from common.log import Log
from common.faker_data import RandomDataGenerator
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager



def main():
  BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  ini = INIManager(BASE_PATH + r'\api\variables.ini')
  log = Log()
  config = ConfigManager()

  sca_env = config.get_config(config.get_use())

  url = sca_env['base_url']+":8443/openapi/v1/project/create"
  payload = json.dumps({
    "name": f"Report_Test-{RandomDataGenerator().numerify(4)}",
    "description": "报告自动化测试",
    "memberList": [
      1
    ],
    "managerList": [
      1
    ]
  })
  headers = {
    'Content-Type': 'application/json',
    'OpenApiUserToken': sca_env['OpenApiUserToken']
  }

  response = RunMethod().api_run("POST", url, headers=headers, data=payload)

  # 提取项目id与项目名称
  if response.status_code == 200:
    log.info(f"创建项目成功：{response.json()}")
    print(f"创建项目成功：{response.json()}")
    project_id = response.json()['data']['id']
    try:
      ini.set_value('variables', 'projectId', f'{project_id}')
      ini.save_config()
      log.info(f"projectId变量写入成功-{project_id}")
      print(f"projectId变量写入成功-{project_id}")
    except Exception as e:
      log.error(f"projectId变量写入失败-{e}")
      print(f"projectId变量写入失败-{e}")

    url = sca_env['base_url']+":8443/openapi/v1/project/detail/"+str(project_id)

    payload={}
    headers = {
       'OpenApiUserToken': sca_env['OpenApiUserToken'],
       'Content-Type': 'application/json'
    }

    response = RunMethod().api_run("GET", url, headers=headers, json=payload)
    if response.status_code == 200:
      log.info(f"获取项目详情成功：{response.json()}")
      print(f"获取项目详情成功：{response.json()}")
      project_name = response.json()['data']['name']
      try:
        ini.set_value('variables', 'projectName', f'{project_name}')
        ini.save_config()
        log.info(f"projectName变量写入成功-{project_name}")
        print(f"projectName变量写入成功-{project_name}")
      except Exception as e:
        log.error(f"projectName变量写入失败-{e}")

if __name__ == '__main__':
  main()
