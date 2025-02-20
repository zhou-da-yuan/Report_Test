import os

import pytest
from Reports import Delete_Report, Get_Report
from api.project_detail import project_exist
from common.log import Log
from common.request import RunMethod

log = Log()


# 定义一个 session 级别的 fixture 来记录测试状态
@pytest.fixture(scope="session", autouse=True)
def test_status(request):
    request.session.test_failed = False


# 使用 pytest_runtest_makereport 钩子来记录测试结果
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # 如果任何一个测试失败，则设置标志
    if rep.when == "call" and rep.failed:
        item.session.test_failed = True
        log.error(f"Test {item.nodeid} failed")


# 使用 pytest_sessionfinish 钩子来在测试会话结束时执行后置函数
def pytest_sessionfinish(session, exitstatus):
    if not getattr(session, 'test_failed', True):  # 默认值为True以确保首次运行时不会误判
        delete_reports()
        log.info("所有用例通过，已清理报告和项目")
    else:
        log.error("存在未通过的用例，报告和项目已保留")


# 定义后置函数
def delete_reports():
    # 删除报告
    Delete_Report.all()
    # 删除项目
    Get_Report.deleteProject()


@pytest.fixture(scope="session", autouse=True)
def a_RunMethod_instance():
    log.info("测试开始，RunMethod 实例已创建")
    request = RunMethod()
    yield request  # 创建requests实例
    request.close_session()
    log.info("测试结束，RunMethod 实例已释放")


@pytest.fixture(scope="session", autouse=True)
def project_manager():
    if project_exist():
        log.info("已存在项目")
    else:
        log.info("项目不存在，创建项目....")
        Get_Report.createProject()
        log.info("删除旧报告....")
        Delete_Report.all()
        log.info("使用新项目生成报告....")
        Get_Report.source()
        Get_Report.binary()
        Get_Report.image()
        log.info("项目报告重新生成成功")


# 确保报告测试时已经生成报告
@pytest.fixture(scope="module",autouse=True)
def Generate_Report():
    # Get_Report.createProject()
    reports = [
        ('Downloads/源码检测报告.xlsx', Get_Report.source),
        ('Downloads/二进制检测报告.xlsx', Get_Report.binary),
        ('Downloads/镜像检测报告.xlsx', Get_Report.image),
    ]

    for report_path, generation_method in reports:
        # 确保 Downloads 目录存在
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        if not os.path.exists(report_path):
            log.info(f"{report_path} 不存在，开始下载报告...")
            generation_method()
        else:
            log.info(f"{report_path} 已存在.")
