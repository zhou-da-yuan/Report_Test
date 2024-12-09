import sys

from api import *
from common.log import Log

log = Log()


def app():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 创建项目
        log.info(f"{function_name}-开始创建项目...")
        create_project.main()
        log.info(f"{function_name}-项目创建成功")

        # 应用检测
        log.info(f"{function_name}-开始应用检测...")
        app_Detect.main()
        log.info(f"{function_name}-应用检测完成")

        # 创建报告
        log.info(f"{function_name}-开始创建报告...")
        create_report.main()
        log.info(f"{function_name}-报告创建成功")

        # 下载报告
        log.info(f"{function_name}-开始下载报告...")
        download_Report.main("源码检测报告")
        log.info(f"{function_name}-报告下载成功")

        # 删除项目
        log.info(f"{function_name}-开始删除项目...")
        delete_project.main()
        log.info(f"{function_name}-项目删除成功")

        # 删除报告
        log.info(f"{function_name}-开始删除报告...")
        delete_Report.main()
        log.info(f"{function_name}-报告删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")

def binary():
    function_name = f"{__name__}.{sys._getframe().f_code.co_name}"
    try:
        # 创建项目
        log.info(f"{function_name}-开始创建项目...")
        create_project.main()
        log.info(f"{function_name}-项目创建成功")

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

        # 删除项目
        log.info(f"{function_name}-开始删除项目...")
        delete_project.main()
        log.info(f"{function_name}-项目删除成功")

        # 删除报告
        log.info(f"{function_name}-开始删除报告...")
        delete_Report.main()
        log.info(f"{function_name}-报告删除成功")
    except Exception as e:
        log.error(f"{function_name}-执行过程中发生错误: {e}")



if __name__ == "__main__":
    # 运行 app 函数
    print(f"{app.function_name}-开始执行...")