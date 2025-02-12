import json
import os
import time

from common.request import RunMethod
from common.log import Log
from common.ini_manager import INIManager
from common.yaml_utils import ConfigManager


def main(fileName):
    log = Log()
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = INIManager(BASE_PATH + r'\api\variables.ini')
    config = ConfigManager()

    sca_env = config.get_config()

    # 根据报告id查询报告状态
    url = sca_env["base_url"] + f":{sca_env['api_port']}/openapi/v1/asset/report/status/" + ini.get_value('variables', 'reportId')

    payload = ""
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
        'Content-Type': 'application/json'
    }

    response = RunMethod().api_run("POST", url, headers=headers, data=payload)

    if response.json()['code'] == 0:
        canProceed = False
        # 循环等待直到 status 等于 1
        max_retries = 100  # 最大重试次数
        retry_interval = 10  # 重试间隔时间（秒）
        for i in range(max_retries):
            try:
                response = RunMethod().api_run("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    status = response.json()['data']['status']
                    if status == 1:
                        log.info("报告生成完成，status 等于 1")
                        canProceed = True
                        print("报告生成完成")
                        break
                    else:
                        log.info(f"当前 status: {status}，等待中...")
                        time.sleep(retry_interval)
                else:
                    log.error(f"状态查询请求失败，状态码: {response.status_code}")
                    break
            except Exception as e:
                log.error(f"状态查询异常: {e}")
                break
        else:
            log.warning("达到最大重试次数，status 仍未等于 5")

        # 报告生成完成后再下载报告
        if canProceed:

            # 发送请求
            try:
                url = sca_env['base_url'] + f":{sca_env['api_port']}/openapi/v1/asset/report/downLoadReport/batch"
                payload = json.dumps({
                    "reportIds": [
                        ini.get_value('variables', 'reportId', data_type=int)
                    ]
                })
                headers = {
                    'OpenApiUserToken': sca_env['OpenApiUserToken'],
                    'Content-Type': 'application/json'
                }

                response = RunMethod().api_run("POST", url, headers=headers, data=payload)

                if response.status_code == 200:
                    log.info(f"报告下载请求成功")
                    file_content = response.content

                    # 构建下载路径
                    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    download_path = os.path.join(BASE_PATH, 'Reports', fileName + '.xlsx')

                    # 确保下载目录存在
                    download_dir = os.path.dirname(download_path)
                    if not os.path.exists(download_dir):
                        try:
                            os.makedirs(download_dir)
                            log.info(f"创建目录: {download_dir}")
                        except Exception as e:
                            log.error(f"无法创建目录: {download_dir}, 错误: {e}")
                            exit(1)
                    with open(download_path, 'wb') as file:
                        file.write(file_content)

                    log.info(f"文件已成功下载并保存到: {download_path}")
                    print("下载成功")
                else:
                    log.error(f"请求失败，状态码: {response.status_code}")
                    log.error(f"响应内容: {response.text}")
            except Exception as e:
                log.error(f"下载报告请求异常: {e}")
    else:
        log.error(f"报告查询失败: {response.json()}")



if __name__ == '__main__':
    main("镜像检测报告")
