import os
import json
import re

from common.ini_manager import INIManager
from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()

class JsonUtil:

    def __init__(self, json_file):
        self.json_file = os.path.join(BASE_PATH, json_file.lstrip('/'))  # 使用 os.path.join 来构建路径

    # 读取json文件并获取appInfo下的数据
    def read_ApplicationInfo(self,info_type=None, objects=None):
        try:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data = json.load(f)
                info_data = data.get(info_type, {})
                log.info("读取json文件成功：{}".format(self.json_file))
                ApplicationInfo = self.replace_placeholders(info_data, objects)
                return ApplicationInfo
        except Exception as e:
            log.error("读取json文件出错: {}".format(e))
            print(e)
            return {}

    # 替换占位符
    def replace_placeholders(self, data, objects):
        """
        递归遍历数据结构，查找并替换字符串中的占位符。
        占位符格式为 {object.method} 或 {object.attribute}。
        """
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.replace_placeholders(value, objects)  # 直接更新字典项
        elif isinstance(data, list):
            for i, item in enumerate(data):  # 遍历列表，i是索引，item是元素
                data[i] = self.replace_placeholders(item, objects)  # 更新列表项
        elif isinstance(data, str):
            placeholders = re.findall(r'\{.*?\}', data)
            for placeholder in placeholders:
                try:
                    # 移除 { 和 } 并解析占位符
                    expression = placeholder[1:-1]
                    result = self.resolve_placeholder(expression, objects)
                    data = data.replace(placeholder, str(result))
                except Exception as e:
                    print(f"Error resolving {expression}: {e}")
        return data

    @staticmethod
    def resolve_placeholder(expression, objects):
        """
        解析并执行占位符表达式。
        支持方法调用（如 ini.get_value）和属性访问（如 VOInfo.data.scaStatusStr）。
        """
        parts = expression.split('.')
        obj_name = parts[0]
        obj = objects.get(obj_name)

        if not obj:
            raise ValueError(f"Object '{obj_name}' not found in objects.")

        if len(parts) == 1:  # 如果只有对象名，返回对象本身
            return obj

        # 对于方法调用，例如 ini.get_value('variables', 'appDetectName')
        if '(' in parts[1]:
            method_call = parts[1].split('(')[0]
            args = parts[1].split('(')[1][:-1].split(',')
            method_args = [arg.strip().strip("'").strip('"') for arg in args]
            if hasattr(obj, method_call): # 检查对象是否有该方法。
                method = getattr(obj, method_call) # 获取方法引用。
                return method(*method_args) # 调用方法并返回结果。

        # 对于属性访问，例如 VOInfo.data.scaStatusStr
        else:
            attr_path = '.'.join(parts[1:])
            result = obj
            for attr in attr_path.split('.'):
                if isinstance(result, dict):
                    result = result.get(    attr)
                else:
                    result = getattr(result, attr, None)
                if result is None:
                    raise AttributeError(f"Attribute '{attr}' not found.")
            return result

# 示例用法
if __name__ == "__main__":
    ini = INIManager(BASE_PATH + r'\api\variables.ini')
    VOInfo = {'data': {'scaStatusStr': '已完成', 'socStatusStr': '未完成', 'riskLevelStr': '低风险',
                       'userName': '张三', 'scaDetectTime': '30分钟', 'socDetectTime': '2小时'}}
    CVLCount = {'data': {'componentNum': 150, 'poisonNum': 2, 'vulNum': 5, 'licenseNum': 3, 'licenseConflictNum': 1}}
    TaskDetails = {'data': {'detectStartTime': '2024-12-10 10:00:00', 'detectEndTime': '2024-12-10 12:30:00'}}

    context = {
        'ini': ini,
        'VOInfo': VOInfo,
        'CVLCount': CVLCount,
        'TaskDetails': TaskDetails
    }

    json_util = JsonUtil('casedata/ApplicationInfo.json')  # 替换为你的 JSON 文件路径
    app_info = json_util.read_ApplicationInfo("appInfo",context)
    print(app_info)
