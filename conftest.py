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
        item.config.cache.set("test_failed", True)

# 使用 pytest_sessionfinish 钩子来在测试会话结束时执行后置函数
def pytest_sessionfinish(session, exitstatus):
    if not session.config.cache.get("test_failed", False):
        # 所有用例都成功，执行后置函数
        delete_reports()
        log.info("所有用例通过，已清理报告")
    else:
        log.error("存在未通过的用例，报告已保留")

# 定义后置函数
def delete_reports():
    # 删除报告
    Delete_Report.all()