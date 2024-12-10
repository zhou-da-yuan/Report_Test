import json
import os
import time

from common.request import RunMethod
from common.log import Log
from common.faker_data import RandomDataGenerator
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager


def main():
    log = Log()
    config = ConfigManager()
    sca_env = config.get_config()

    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = INIManager(BASE_PATH + r'\api\variables.ini')

    # 查询任务状态
    url = sca_env['base_url'] + ":8443/openapi/v1/task/batch/status"
    task_id = ini.get_value('variables', 'scaTaskId', data_type=int)
    payload = json.dumps({
        "taskIdList": [
            task_id
        ]
    })
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
        'Content-Type': 'application/json'
    }

    response = RunMethod().api_run("POST", url, headers=headers, data=payload)

    if response.json()['code'] == 0:
        canProceed = False
        # 循环等待直到 status 等于 5
        max_retries = 1000  # 最大重试次数
        retry_interval = 10  # 重试间隔时间（秒）
        for i in range(max_retries):
            try:
                response = RunMethod().api_run("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    status = response.json()['data']['status'][f'{task_id}']
                    if status == 5:
                        log.info("任务完成，status 等于 5")
                        canProceed = True
                        print("任务完成")
                        break
                    else:
                        log.info(f"当前 status: {status}，等待中...")
                        time.sleep(retry_interval)
                        if status == 8:
                            log.error("检测任务失败，请查看检测详情")
                            break
                else:
                    log.error(f"状态查询请求失败，状态码: {response.status_code}")
                    break
            except Exception as e:
                log.error(f"状态查询异常: {e}")
                break
        else:
            log.warning("达到最大重试次数，status 仍未等于 5")

        # 任务完成后生成报告
        if canProceed:
            url = sca_env['base_url'] + ":8443/openapi/v1/asset/report/task"

            payload = json.dumps({
                "advancedSearch": {
                    "componentSecurityLevelList": [
                        1
                    ]
                },
                "dimension": 5,
                "reportName": f"Report_Test-{RandomDataGenerator().numerify(4)}",
                "scaTaskId": task_id,
                "type": 5
            })

            response = RunMethod().api_run("POST", url, headers=headers, data=payload)

            if response.json()["code"] == 0:
                log.info("报告生成成功")
                print("报告生成成功", {response.text})
                ini.set_value('variables', 'reportId', response.json()['data'])
                ini.save_config()
                log.info(f"报告ID写入成功-{response.json()['data']}")
                print(f"报告ID写入成功-{response.json()['data']}")
            else:
                log.error(f"报告生成失败{response.json()}")
                print(f"报告生成id {task_id}")
        else:
            ini.set_value('variables', 'reportId', "")
            ini.save_config()
            log.error("任务未完成，无法生成报告")


if __name__ == '__main__':
    main()
