import glob
import os

from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
def all():
    # 删除报告
    reports_dir = os.path.join(BASE_PATH, 'Downloads')

    # 检查 Downloads 目录是否存在
    if not os.path.exists(reports_dir):
        log.warning(f"目录不存在: {reports_dir}")
        print(f"目录不存在: {reports_dir}")
        return

    # 查找所有的 .xlsx 文件
    xlsx_files = glob.glob(os.path.join(reports_dir, '*.xlsx'))

    if not xlsx_files:
        log.info("没有找到任何 .xlsx 文件")
        print("没有找到任何 .xlsx 文件")
        return

    # 删除每个 .xlsx 文件
    for file_path in xlsx_files:
        try:
            os.remove(file_path)
            log.info(f"文件已成功删除: {file_path}")
            print(f"文件已成功删除: {file_path}")
        except Exception as e:
            log.error(f"删除文件时发生错误: {file_path}, 错误信息: {e}")
            print(f"删除文件时发生错误: {file_path}, 错误信息: {e}")

if __name__ == '__main__':
    all()