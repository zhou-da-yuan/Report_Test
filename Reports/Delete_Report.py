import os

from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
def app():
    # 删除报告
    file_path = BASE_PATH + '\Reports\源码检测报告.xlsx'
    try:
        # 删除文件
        os.remove(file_path)
        log.info("源码检测报告成功删除")
        print(f"文件已成功删除: {file_path}")
    except FileNotFoundError:
        log.error("源码检测报告未找到")
        print(f"文件未找到: {file_path}")
    except PermissionError:
        log.error("权限错误")
        print(f"权限错误: 无法删除文件 {file_path}")
    except Exception as e:
        log.error("删除文件时发生错误")
        print(f"删除文件时发生错误: {e}")