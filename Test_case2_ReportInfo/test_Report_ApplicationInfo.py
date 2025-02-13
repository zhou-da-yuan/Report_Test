import os

import pytest

from Reports import Get_Report
from api.get_ApplicationInfo import InfoGet
from common.data_utils import DataUtils
from common.excel_utils import Excel
from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
data_utils = DataUtils()


# 源码应用信息测试
def test_source_appInfo():
    log.info("----------Begin test_source_appInfo----------")
    # Get_Report.source()
    info = InfoGet("sourceTaskId")
    excel = Excel(BASE_PATH + r'\Reports\源码检测报告.xlsx')

    report_data = excel.get_ApplicationInfo()
    case_data = info.get_source_appInfo()

    comparison_results = data_utils.compare_dicts(report_data, case_data)

    flag = True
    for key, equal, report_value, case_value in comparison_results:
        if equal is None:
            log.warning(f"Key '{key}' not found in report_data.")
            print(f"Key '{key}' not found in report_data.")
        elif equal:
            log.info(f"Key '{key}' 匹配成功！")
        else:
            log.error(f"Key '{key}': Values differ - Report: '{report_value}', Case: '{case_value}'")
            flag = False
    if flag:
        log.info(f"所有应用信息匹配成功-PASS")
        assert True, f"所有应用信息匹配成功"
    else:
        log.error(f"部分应用信息匹配失败，请查看日志")
        assert False, f"部分应用信息匹配失败，请查看日志"

    excel.close()
    log.info("测试结束，报告已关闭！")


# 二进制应用信息测试
def test_binary_appInfo():
    log.info("----------Begin test_binary_appInfo----------")
    # Get_Report.source()
    info = InfoGet("binaryTaskId")
    excel = Excel(BASE_PATH + r'\Reports\二进制检测报告.xlsx')

    report_data = excel.get_ApplicationInfo()
    case_data = info.get_binary_appInfo()

    comparison_results = data_utils.compare_dicts(report_data, case_data)

    flag = True
    for key, equal, report_value, case_value in comparison_results:
        if equal is None:
            log.warning(f"Key '{key}' not found in report_data.")
            print(f"Key '{key}' not found in report_data.")
        elif equal:
            log.info(f"Key '{key}' 匹配成功！")
        else:
            log.error(f"Key '{key}': Values differ - Report: '{report_value}', Case: '{case_value}'")
            flag = False
    if flag:
        log.info(f"所有应用信息匹配成功-PASS")
        assert True, f"所有应用信息匹配成功"
    else:
        log.error(f"部分应用信息匹配失败，请查看日志")
        assert False, f"部分应用信息匹配失败，请查看日志"

    excel.close()
    log.info("测试结束，报告已关闭！")


# 镜像应用信息测试
def test_image_appInfo():
    log.info("----------Begin test_image_appInfo----------")
    # Get_Report.source()
    info = InfoGet("imageTaskId")
    excel = Excel(BASE_PATH + r'\Reports\镜像检测报告.xlsx')

    report_data = excel.get_ApplicationInfo()
    case_data = info.get_image_appInfo()

    comparison_results = data_utils.compare_dicts(report_data, case_data)

    flag = True
    for key, equal, report_value, case_value in comparison_results:
        if equal is None:
            log.warning(f"Key '{key}' not found in report_data.")
            print(f"Key '{key}' not found in report_data.")
        elif equal:
            log.info(f"Key '{key}' 匹配成功！")
        else:
            log.error(f"Key '{key}': Values differ - Report: '{report_value}', Case: '{case_value}'")
            flag = False
    if flag:
        log.info(f"所有应用信息匹配成功-PASS")
        assert True, f"所有应用信息匹配成功"
    else:
        log.error(f"部分应用信息匹配失败，请查看日志")
        assert False, f"部分应用信息匹配失败，请查看日志"

    excel.close()
    log.info("测试结束，报告已关闭！")
