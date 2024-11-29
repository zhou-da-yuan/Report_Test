import pytest

from common.excel_utils import Excel
from common.log import Log

# 实例用例与测试数据
excel = Excel('D://供应链场景excel报告.xlsx', "Sheet3", 'D://SCA_load//【应用报告】grule-master.zip@2-20241129153126.xlsx')
log = Log()
class TestSheet:
    # 测试工作表标题
    def test_sheets_title(self):
        try:
            df = excel.read_caseData('源码检测', 'sheet标题及顺序')
            if df:
                report_sheets = excel.read_report_sheetNames()
                if set(df) != set(report_sheets):
                    excel.log.info("Sheet标题数据匹配失败！")
                    assert False, "数据不匹配"
                log.info("Sheet标题数据匹配成功！")
            else:
                pytest.fail("没有找到对应的测试用例数据。")
                log.warning("没有找到对应的测试用例数据。")
        except Exception as e:
            pytest.fail(f"发生错误: {e}")

    # 测试每个工作表的表头
    @pytest.mark.parametrize("sheet_name",excel.read_report_sheetNames())
    def test_sheet_headers(self, sheet_name):
        try:
            case_data = excel.read_caseData('源码检测', sheet_name)
            if case_data :
                headers = excel.read_report_headers(sheet_name)
                if set(case_data) != set(headers):
                    log.info(f"工作表 {sheet_name} 的表头与用例数据不匹配！")
                    assert False, "数据不匹配"
                log.info(f"工作表 {sheet_name} 的表头与用例数据匹配成功！")
            else:
                pytest.fail("没有找到对应的测试用例数据。")
                log.warning("没有找到对应的测试用例数据。")
        except Exception as e:
            pytest.fail(f"发生错误: {e}")

