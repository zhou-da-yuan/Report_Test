import os
import yaml

from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = BASE_PATH + '/config/sca.yaml'
log = Log()


class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self._config = yaml.load(f, Loader=yaml.FullLoader)
                log.info("读取sca配置文件成功")
        except Exception as e:
            log.error("读取sca配置文件出错: {}".format(e))
            self._config = {}

    def get_use(self):
        use_env = self._config.get('use')
        if use_env:
            log.info("使用环境：{}".format(use_env))
        else:
            log.error("未找到使用环境配置")
        return use_env

    def get_config(self, env):
        env_config = self._config.get(env)
        if env_config:
            log.info("环境配置：{}".format(env_config))
        else:
            log.error("未找到环境配置：{}".format(env))
        return env_config


if __name__ == '__main__':
    config_manager = ConfigManager()

    # 获取当前使用的环境
    use_env = config_manager.get_use()
    # 读取环境变量配置
    sca_env = config_manager.get_config(use_env)

    if sca_env:
        print(sca_env['base_url'])
        print(sca_env['OpenApiUserToken'])