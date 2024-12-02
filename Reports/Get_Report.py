
from api import create_project, app_Detect, create_report, download_Report, delete_project
from common.log import Log

log = Log()


def app():
    try:
        # 创建项目
        log.info("开始创建项目...")
        create_project.main()
        log.info("项目创建成功")

        # 应用检测
        log.info("开始应用检测...")
        app_Detect.main()
        log.info("应用检测完成")

        # 创建报告
        log.info("开始创建报告...")
        create_report.main()
        log.info("报告创建成功")

        # 下载报告
        log.info("开始下载报告...")
        download_Report.main()
        log.info("报告下载成功")

        # 删除项目
        log.info("开始删除项目...")
        delete_project.main()
        log.info("项目删除成功")
    except Exception as e:
        log.error(f"执行过程中发生错误: {e}")


if __name__ == "__main__":
    # 运行 app 函数
    app()