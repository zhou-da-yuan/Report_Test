import sys
import time

from api import *
from common.log import Log

log = Log()

def createProject():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 创建项目
        log.info(f"{function_name}-开始创建项目...")
        create_project.main()
        log.info(f"{function_name}-项目创建成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")

def deleteProject():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 删除项目
        log.info(f"{function_name}-开始删除项目...")
        delete_project.main()
        log.info(f"{function_name}-项目删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")

# 源码检测
def source():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 应用检测
        log.info(f"{function_name}-开始应用检测...")
        source_Detect.main()
        log.info(f"{function_name}-应用检测完成")

        time.sleep(100) # 源码检测后马上下载的报告组件状态不对所以需要等待

        # 创建报告
        log.info(f"{function_name}-开始创建报告...")
        create_report.main()
        log.info(f"{function_name}-报告创建成功")

        # 下载报告
        log.info(f"{function_name}-开始下载报告...")
        download_Report.main("源码检测报告")
        log.info(f"{function_name}-报告下载成功")

        # 删除报告
        log.info(f"{function_name}-开始删除报告...")
        delete_Report.main()
        log.info(f"{function_name}-报告删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")

# 二进制检测
def binary():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 应用检测
        log.info(f"{function_name}-开始应用检测...")
        binary_Detect.main()
        log.info(f"{function_name}-应用检测完成")

        # 创建报告
        log.info(f"{function_name}-开始创建报告...")
        create_report.main()
        log.info(f"{function_name}-报告创建成功")

        # 下载报告
        log.info(f"{function_name}-开始下载报告...")
        download_Report.main("二进制检测报告")
        log.info(f"{function_name}-报告下载成功")

        # 删除报告
        log.info(f"{function_name}-开始删除报告...")
        delete_Report.main()
        log.info(f"{function_name}-报告删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")

def image():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 应用检测
        log.info(f"{function_name}-开始应用检测...")
        image_Detect.main()
        log.info(f"{function_name}-应用检测完成")

        # 创建报告
        log.info(f"{function_name}-开始创建报告...")
        create_report.main()
        log.info(f"{function_name}-报告创建成功")

        # 下载报告
        log.info(f"{function_name}-开始下载报告...")
        download_Report.main("镜像检测报告")
        log.info(f"{function_name}-报告下载成功")

        # 删除报告
        log.info(f"{function_name}-开始删除报告...")
        delete_Report.main()
        log.info(f"{function_name}-报告删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")


if __name__ == "__main__":
    # 运行 app 函数
    deleteProject()
    # source()