import warnings
import pandas as pd

from common.log import Log

# 忽略特定的警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
class Excel:


    def __init__(self, case_file_path, case_file_sheet, report_file_path):
        self.case_file_path = case_file_path
        self.case_file_sheet = case_file_sheet
        self.report_file_path = report_file_path
        self.case_dataframe = None  # 用于缓存用例数据
        self.report_excel = None  # 用于缓存报告文件
        self.log = Log()  # 日志器对象

    def load_case_data(self):
        """加载用例数据到dataframe中"""
        if self.case_dataframe is None:
            self.log.info("开始加载用例数据")
            try:
                self.case_dataframe = pd.read_excel(self.case_file_path, sheet_name=self.case_file_sheet)
                self.log.info("用例数据加载完成")
            except Exception as e:
                self.log.error(f"用例加载发生错误: {e}")


    def load_report_data(self):
        """加载报告Excel文件"""
        if self.report_excel is None:
            self.log.info("开始加载报告数据")
            try:
                self.report_excel = pd.ExcelFile(self.report_file_path)
                self.log.info("报告数据加载完成")
            except Exception as e:
                self.log.error(f"报告加载发生错误: {e}")

    def read_caseData(self, module_name, case_name):
        """根据模块名和用例名筛选数据并转换为列表"""
        self.log.info(f"开始读取用例数据: 模块名-{module_name}, 用例名称-{case_name}")
        self.load_case_data()
        df = self.case_dataframe
        filtered_df = df[(df['所属模块'] == module_name) & (df['用例名称(关键字)'] == case_name)]
        if not filtered_df.empty:
            data_list = filtered_df["数据"].values[0].split(',')
            result = [item.strip() for item in data_list]
            self.log.info(f"用例数据读取成功: {result}")
            return result
        else:
            self.log.warning(f"没有找到工作表模块：{module_name} 对应的测试用例数据：{case_name}")
            return []

    def read_report_sheetNames(self):
        """读取报告文件的所有工作表名称并转换为列表"""
        self.log.info("开始读取报告中的所有工作表名称")
        self.load_report_data()
        sheet_names = self.report_excel.sheet_names
        self.log.info(f"报告中的工作表名称读取成功: {sheet_names}")
        return sheet_names

    def read_report_headers(self, sheet_name):
        """读取指定工作表的首行表头并转换为列表"""
        self.log.info(f"开始读取工作表 {sheet_name} 的首行表头")
        df = pd.read_excel(self.report_file_path, sheet_name=sheet_name, nrows=1)
        headers = df.columns.tolist()
        self.log.info(f"工作表 {sheet_name} 的首行表头读取成功: {headers}")
        return headers

    def close(self):
        """清理资源"""
        self.log.info("开始清理Excel实例资源")
        if self.report_excel:
            self.report_excel.close()
            self.report_excel = None
        if self.case_dataframe is not None:
            del self.case_dataframe
            self.case_dataframe = None
        self.log.info("Excel实例资源清理完成")


def str_to_list(str_val):
    """将字符串转换为列表，去除空格"""
    return [item.strip() for item in str_val.split(',')]

if __name__ == '__main__':
    pass