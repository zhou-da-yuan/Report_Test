import pytest

from common.excel_utils import Excel


# 定义一个固件，用于创建和返回 Excel 实例
@pytest.fixture(scope="class", autouse=True)
def excel_instance(request):
    excel = Excel('D://供应链场景excel报告.xlsx', "Sheet3", 'D://SCA_load//【应用报告】grule-master.zip@2-20241129153126.xlsx')
    excel.close()
    request.cls.excel = excel  # 将 Excel 实例绑定到测试类
    yield excel
    # 清理资源
    excel.close()
    excel.log.info("测试结束，Excel 实例已释放")