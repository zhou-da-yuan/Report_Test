import os
from http.cookiejar import request_port

import pytest

from api import get_ApplicationInfo
from common.excel_utils import Excel
from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()

def test_source_appInfo():
    excel = Excel('D://供应链场景excel报告.xlsx', "sheet标题及表头测试", BASE_PATH+f'\Reports\源码检测报告.xlsx')
    report_data = excel.get_ApplicationInfo()
    case_data = get_ApplicationInfo.get_appInfo()
