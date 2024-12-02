import configparser
import os


class INIManager:
    def __init__(self, file_path):
        """
        初始化 INI 管理器
        :param file_path: INI 文件的路径
        """
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """
        从文件中加载配置
        """
        if os.path.exists(self.file_path):
            self.config.read(self.file_path)

    def save_config(self):
        """
        将配置保存到文件
        """
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    def get_value(self, section, option, default=None, data_type=str):
        """
        获取指定节和选项的值，并根据需要转换数据类型
        :param section: 节名称
        :param option: 选项名称
        :param default: 如果选项不存在，返回的默认值
        :param data_type: 数据类型 (str, int, float, bool)
        :return: 选项的值或默认值
        """
        try:
            if data_type == str:
                return self.config.get(section, option)
            elif data_type == int:
                return self.config.getint(section, option)
            elif data_type == float:
                return self.config.getfloat(section, option)
            elif data_type == bool:
                return self.config.getboolean(section, option)
            else:
                raise ValueError("Unsupported data type")
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set_value(self, section, option, value):
        """
        设置指定节和选项的值
        :param section: 节名称
        :param option: 选项名称
        :param value: 选项的值
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def remove_option(self, section, option):
        """
        删除指定节和选项
        :param section: 节名称
        :param option: 选项名称
        """
        if self.config.has_section(section) and self.config.has_option(section, option):
            self.config.remove_option(section, option)

    def remove_section(self, section):
        """
        删除指定节
        :param section: 节名称
        """
        if self.config.has_section(section):
            self.config.remove_section(section)

    def get_sections(self):
        """
        获取所有节的名称
        :return: 节名称列表
        """
        return self.config.sections()

    def get_options(self, section):
        """
        获取指定节的所有选项
        :param section: 节名称
        :return: 选项名称列表
        """
        if self.config.has_section(section):
            return self.config.options(section)
        return []

    def get_items(self, section):
        """
        获取指定节的所有选项及其值
        :param section: 节名称
        :return: 选项及其值的字典
        """
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}


if __name__ == "__main__":
    # 创建 INI 管理器实例
    ini_manager = INIManager('../api/variables.ini')

