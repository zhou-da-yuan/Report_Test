import pytest
from Reports import Delete_Report
from common.log import Log

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
        log.info("所有用例通过，已清理报告")
    else:
        log.error("存在未通过的用例，报告已保留")

# 定义后置函数
def delete_reports():
    # 删除报告
    Delete_Report.all()
