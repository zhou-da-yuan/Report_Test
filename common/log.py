# 日志公共方法

import logging
import os
import time
from colorlog import ColoredFormatter


# 日志存放路径
log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)


class Log:
    def __init__(self):
        # 在日志路径下添加日志文件名
        self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        # logger日志对象初始化
        self.logger = logging.getLogger()
        # 设置日志等级
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s]-%(filename)s]-[]-%(levelname)s:%(message)s')

        self.formatter_color = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    def __console(self, level, message):
        # 创建一个 FileHandler，用于写到本地
        fh = logging.FileHandler(self.log_name, 'a', "utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        # 创建一个 StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(self.formatter_color)
        self.logger.addHandler(ch)
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == "__main__":
    log = Log()
    log.info("---测试开始---")
    log.info("操作步骤1,2,3")
    log.warning("---测试结束---")
    logging.info("日志信息")