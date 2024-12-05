import os
import pytest

from Reports import Delete_Report
from common import log
from common.request import RunMethod

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = log.Log()


@pytest.fixture(scope="session", autouse=True)
def RunMethod_instance():
    log.info("测试开始，RunMethod 实例已创建")
    request = RunMethod()
    yield request
    request.close_session()
    log.info("测试结束，RunMethod 实例已释放")

@pytest.fixture(scope="session",autouse=True)
def clear_reports():
    yield    # 删除报告
    Delete_Report.app()
