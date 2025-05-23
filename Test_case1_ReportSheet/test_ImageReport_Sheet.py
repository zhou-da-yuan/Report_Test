import os

import pytest

from common.excel_utils import Excel
from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()

# 实例用例与测试数据
excel = Excel(BASE_PATH + f'\Downloads\镜像检测报告.xlsx', BASE_PATH + f'\casedata\供应链场景excel报告测试.xlsx',
              "sheet标题及表头测试")


# 清理测试数据
def teardown_module(module):
    excel.close()
    log.info("test_ImageReport_Sheet测试结束，报告已关闭！")


class TestSheet:
    # 测试工作表标题
    def test_sheets_title(self):
        try:
            case_sheets = excel.read_caseData('镜像检测', 'sheet标题')
            if case_sheets:
                report_sheets = excel.read_report_sheetNames()
                if case_sheets != report_sheets:
                    diff = set(case_sheets).symmetric_difference(set(report_sheets))
                    if len(diff) != 0:
                        log.error(f"镜像检测报告-sheet标题与用例数据不匹配！diff:{diff}")
                        assert False, f"数据不匹配-diff:{diff}"
                    else:
                        log.error(f"镜像检测报告-sheet标题与用例顺序不匹配！")
                        assert False, f"顺序不匹配"
                log.info("Sheet标题数据匹配成功！")
            else:
                pytest.fail("没有找到对应的测试用例数据。")
                log.warning("没有找到对应的测试用例数据。")
        except Exception as e:
            pytest.fail(f"发生错误: {e}")

    # 测试每个工作表的表头
    @pytest.mark.parametrize("sheet_name", excel.read_caseData('镜像检测', 'sheet标题'))
    def test_sheet_headers(self, sheet_name):
        try:
            case_data = excel.read_caseData('镜像检测', sheet_name)
            if case_data:
                headers = excel.read_report_headers(sheet_name)
                if case_data != headers:
                    diff = set(case_data).symmetric_difference(set(headers))
                    if len(diff) != 0:
                        log.error(f"工作表 {sheet_name} 的表头与用例数据不匹配！diff:{diff}")
                        assert False, f"数据不匹配-diff:{diff}"
                    else:
                        log.error(f"工作表 {sheet_name} 的表头与用例顺序不匹配！")
                        assert False, f"顺序不匹配"
                log.info(f"工作表 {sheet_name} 的表头与用例数据匹配成功！")
            else:
                pytest.fail("没有找到对应的测试用例数据。")
                log.warning("没有找到对应的测试用例数据。")
        except Exception as e:
            pytest.fail(f"发生错误: {e}")
