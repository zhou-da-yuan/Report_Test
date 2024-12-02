import os
import pytest

from Reports import Delete_Report
from common import log
from common.excel_utils import Excel
from common.request import RunMethod

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = log.Log()


@pytest.fixture(scope="class", autouse=True)
def RunMethod_instance():
    log.info("测试开始，RunMethod 实例已创建")
    request = RunMethod()
    yield request
    request.close_session()
    log.info("测试结束，RunMethod 实例已释放")

@pytest.fixture(scope="class",autouse=True)
def app_reports():
    # 下载报告
    # Get_Report.app()
    # 实例用例与测试数据
    excel = Excel('D://供应链场景excel报告.xlsx', "全", BASE_PATH + f'\Reports\源码检测报告.xlsx')
    yield
    excel.close()
    # 删除报告
    Delete_Report.app()
