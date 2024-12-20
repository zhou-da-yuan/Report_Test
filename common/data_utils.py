import ast
import os
import json
import re

from common.log import Log

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()


class JsonUtil:

    def __init__(self, json_file):
        self.json_file = os.path.join(BASE_PATH, json_file.lstrip('/'))  # 使用 os.path.join 来构建路径

    # 读取json文件并获取appInfo下的数据
    def read_ApplicationInfo(self, info_type=None, objects=None):
        try:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data = json.load(f)
                info_data = data.get(info_type, {})
                log.info("读取json文件成功：{}".format(self.json_file))
                ApplicationInfo = self.replace_placeholders(info_data, objects)  # 替换占位符
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
        支持方法调用（如 ini.get_value）和属性访问（如 VOInfo.data.scaStatusStr[0]）。
        如果最终结果为空或 None，则返回空数据而不抛出异常。
        """
        parts = expression.split('.')
        obj_name = parts[0]
        obj = objects.get(obj_name)

        if not obj:
            raise ValueError(f"Object '{obj_name}' not found in objects.")

        if len(parts) == 1:  # 如果只有对象名，返回对象本身
            return obj if obj is not None else ""

        # 对于方法调用，例如 ini.get_value('variables', 'appDetectName')
        if '(' in parts[1]:
            method_call = parts[1].split('(')[0]
            args_part = parts[1].split('(', 1)[1][:-1]
            args = [arg.strip().strip("'").strip('"') for arg in args_part.split(',')] if args_part else []
            if hasattr(obj, method_call):  # 检查对象是否有该方法。
                method = getattr(obj, method_call)  # 获取方法引用。
                result = method(*args)  # 调用方法并返回结果。
            else:
                raise AttributeError(f"Method '{method_call}' not found on object '{obj_name}'.")
        else:
            # 对于属性访问，例如 VOInfo.data.scaStatusStr 或 VOInfo.data.scaStatusStr[0]
            attr_path = '.'.join(parts[1:])
            result = obj
            for part in attr_path.split('.'):
                # 检查是否包含索引访问 [index]
                if '[' in part and ']' in part:
                    attr, _, index_part = part.partition('[')
                    index_part = index_part.rstrip(']')
                    try:
                        index = int(index_part)
                    except ValueError:
                        raise AttributeError(f"Invalid index '{index_part}' in attribute path.")

                    # 先获取属性/键，再根据索引访问列表元素
                    if isinstance(result, dict):
                        result = result.get(attr)
                    elif hasattr(result, attr):
                        result = getattr(result, attr)
                    else:
                        raise AttributeError(f"Attribute '{attr}' not found on object '{obj_name}'.")

                    if result is None:
                        break

                    if not isinstance(result, list) or index < 0 or index >= len(result):
                        raise IndexError(f"Index '{index}' out of range for attribute '{attr}'.")

                    result = result[index]
                else:
                    # 普通属性访问
                    if isinstance(result, dict):
                        result = result.get(part)
                    elif hasattr(result, part):
                        result = getattr(result, part)
                    else:
                        raise AttributeError(f"Attribute '{part}' not found on object '{obj_name}'.")

                    if result is None:
                        break

        # 如果结果是 None 或者是空的集合类型，返回空字符串
        if result is None or (isinstance(result, (str, list, dict, set)) and not result):
            return ""

        return result


class DataUtils:
    def compare_dicts(self, report_data, case_data):
        """
        比较两个字典中的值，如果case_data中的键在report_data中存在就测试值是否相等。

        :param report_data: 报告中读取的数据，作为基准进行比较
        :param case_data: 接口中读取的数据，其键和值与report_data进行对比
        :return: 包含比较结果的列表，每个元素是一个元组 (key, equal_flag, report_value, case_value)
                 equal_flag 是 True 或 False 表示值是否相等
        """
        results = []

        for key, case_value in case_data.items():
            if key in report_data:
                report_value = report_data[key]
                # 特别处理 "0.0" 和 "0" 的情况
                if report_value == "0.0":
                    report_value = "0"
                elif case_value == "0.0":
                    case_value = "0"
                equal = report_value == case_value
                results.append((key, equal, report_value, case_value))
            else:
                # 如果report_data中没有这个键，可以选择记录或者忽略
                results.append((key, None, "Key not found in report_data", case_value))

        return results

    def riskLevel_Trans(self, data):
        """
        将风险等级ID转换为对应的描述性字符串。

        参数:
            data (str): 风险等级ID的字符串表示，例如 "1" 表示严重。

        返回:
            str: 对应的风险等级描述。

        抛出:
            ValueError: 如果传入的data不在预期的风险等级范围内。
        """
        # 定义风险等级映射
        risk_level_map = {
            '1': '严重',
            '2': '高危',
            '3': '中危',
            '4': '低危',
            '5': '无漏洞'
        }

        # 检查输入是否有效
        if data not in risk_level_map:
            log.error(f"无效的风险等级ID: {data}，请查看相关日志!!")
            raise ValueError(f"无效的风险等级ID: {data}。有效的ID范围是 1 到 5。")

        # 返回对应的描述性字符串
        return risk_level_map[data]

    def dependencyType_Trans(self, data_str):
        """
        将传入的依赖数据字符串（列表格式）转换成 "直接依赖:X\n间接依赖:Y" 格式的字符串。

        参数:
            data_str (str): 依赖数据的列表字符串表示。

        返回:
            str: 格式化后的依赖信息字符串。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        try:
            # 将字符串转换为列表
            data = str_to_list(data_str)
        except ValueError as e:
            raise ValueError(f"无效的依赖数据字符串: {e}")

        # 初始化计数器
        direct_count = 0
        indirect_count = 0

        # 遍历传入的数据并更新计数器
        for item in data:
            if not isinstance(item, dict) or 'count' not in item or 'name' not in item:
                raise ValueError("输入数据格式不正确，必须是包含 'count' 和 'name' 键的字典列表。")

            count = item.get('count', 0)
            name = item.get('name')

            if name == '直接依赖':
                direct_count = count
            elif name == '间接依赖':
                indirect_count = count

        # 如果没有提供数量，默认设置为0
        return f"直接依赖:{direct_count}\n间接依赖:{indirect_count}"

    def is_Trans(self, data):
        """
        将传入的字符串 "0" 转换为 "否"，将 "1" 转换为 "是"。

        参数:
            data (str): 表示布尔值的字符串，"0" 或 "1"。

        返回:
            str: 对应的中文描述 "否" 或 "是"。

        抛出:
            ValueError: 如果输入不是 "0" 或 "1"。
        """
        # 检查输入是否有效
        if data not in ('0', '1'):
            raise ValueError(f"无效的输入数据: {data}。有效的输入只能是 '0' 或 '1'。")

        # 根据输入返回相应的中文描述
        return "是" if data == '1' else "否"

    def license_Trans(self, data_str):
        """
        将传入的许可证数据字符串转换为按 securityLevel 排序的风险描述字符串。

        参数:
            data_str (str): 许可证数据的列表字符串表示。

        返回:
            str: 格式化后的风险描述字符串。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        if data_str == '':
            log.info("该组件无许可证")
            return ""
        try:
            # 将字符串转换为列表
            data = ast.literal_eval(data_str)
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ValueError("输入不是一个有效的许可证数据列表。")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"无效的许可证数据字符串: {e}")

        # 定义风险等级映射
        risk_level_map = {
            1: '高风险',
            2: '中风险',
            3: '低风险'
        }

        # 检查并排序数据
        sorted_data = sorted(
            data,
            key=lambda x: x.get('securityLevel', 4),  # 默认值4确保无效级别排在最后
            reverse=False  # 从高到低排序，1为最高风险，3为最低风险
        )

        # 生成格式化字符串
        formatted_output = []
        for item in sorted_data:
            security_level = item.get('securityLevel')
            name = item.get('name')

            if security_level not in risk_level_map:
                continue  # 跳过无效的风险级别

            risk_description = risk_level_map[security_level]
            formatted_output.append(f"{risk_description}：{name}")

        return '; '.join(formatted_output) + ';' if formatted_output else ""

    def noVulVersion_Trans(self, data_str):
        """
        将传入的版本数据字符串提取出版本号并转为指定格式。

        参数:
            data_str (str): 版本数据的列表字符串表示。

        返回:
            str: 格式化后的版本号字符串，以逗号分隔。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        try:
            # 将字符串转换为列表
            data = ast.literal_eval(data_str)
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ValueError("输入不是一个有效的版本数据列表。")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"无效的版本数据字符串: {e}")

        # 提取版本号
        versions = [item.get('version') for item in data if 'version' in item]

        return ', '.join(versions)

    def dependencyPath_Trans(self, data_str):
        """
        将传入的依赖数据字符串提取出所有 "dependencyPath" 数据并使用分号分隔。

        参数:
            data_str (str): 依赖数据的列表字符串表示。

        返回:
            str: 所有 "dependencyPath" 数据以分号分隔的字符串。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        try:
            # 将字符串转换为列表
            data = ast.literal_eval(data_str)
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ValueError("输入不是一个有效的依赖数据列表。")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"无效的依赖数据字符串: {e}")

        # 提取所有的 "dependencyPath" 数据
        dependency_paths = [item.get('dependencyPath', '') for item in data if 'dependencyPath' in item]

        # 使用分号分隔并返回
        return '; '.join(dependency_paths)

    def vulCount(self, data_str):
        """
        统计漏洞数量及不同严重程度的漏洞数量。

        参数:
            data_str (str): 包含组件信息和漏洞列表的 JSON 字符串。

        返回:
            str: 总漏洞数量及不同严重程度的漏洞数量的格式化字符串。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        try:
            # 尝试使用 ast.literal_eval 安全解析 Python 字面量表达式
            data = ast.literal_eval(data_str)
            if not isinstance(data, dict) or 'vulList' not in data:
                raise ValueError("输入不是一个有效的漏洞数据字符串。")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"无效的漏洞数据字符串: {e}")

        # 提取漏洞数据
        vul_list = data.get('vulList')

        if vul_list is None:
            log.debug("该组件无漏洞")
            return "0(严重:0;高危:0;中危:0;低危:0)"

        if not isinstance(vul_list, list):
            raise ValueError("vulList 不是一个有效的列表。")

        # 定义严重程度映射
        severity_map = {
            1: '严重',
            2: '高危',
            3: '中危',
            4: '低危'
        }

        # 初始化统计变量
        total_vul_count = len(vul_list)
        severity_counts = {severity: 0 for severity in severity_map.values()}

        # 统计不同严重程度的漏洞数量
        for vul in vul_list:
            security_level_id = vul.get('securityLevelId')
            if security_level_id in severity_map:
                severity_counts[severity_map[security_level_id]] += 1

        # 确保至少有一个严重程度的计数大于 0
        non_zero_severities = [f"{severity}:{count}" for severity, count in severity_counts.items() if count > 0]
        formatted_output = f"{total_vul_count}({';'.join(non_zero_severities)})" if non_zero_severities else f"{total_vul_count}(严重:0;高危:0;中危:0;低危:0)"

        return formatted_output

    def vulNumber(self, data_str):
        """
        提取并格式化漏洞信息中的 cveId、cnnvdId、cweId 或 vulId，
        并根据严重程度分类输出。

        参数:
            data_str (str): 包含漏洞信息的 Python 列表字符串。

        返回:
            str: 格式化后的漏洞 ID 字符串。

        抛出:
            ValueError: 如果输入数据格式不正确或解析失败。
        """
        if data_str == '' or data_str is None:
            log.debug("该组件无漏洞")
            return ""
        try:
            # 使用 ast.literal_eval 安全解析 Python 字面量列表字符串
            vul_list = ast.literal_eval(data_str)
            if not isinstance(vul_list, list):
                raise ValueError("输入不是一个有效的漏洞列表字符串。")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"无效的漏洞列表字符串: {e}")

        # 定义严重程度映射
        severity_map = {
            1: '严重',
            2: '高危',
            3: '中危',
            4: '低危'
        }

        # 初始化结果字典
        result = {severity: [] for severity in severity_map.values()}

        # 遍历漏洞列表并分类收集所有 ID
        for vul in vul_list:
            security_level_id = vul.get('securityLevelId')
            if security_level_id in severity_map:
                severity = severity_map[security_level_id]
                # 按优先级选择 ID
                id_to_use = (
                        vul.get('cveId') or
                        vul.get('cnnvdId') or
                        vul.get('cweId') or
                        vul.get('vulId')
                )
                result[severity].append(id_to_use)

        # 构建最终输出字符串
        formatted_output_parts = []
        for severity_level_id in sorted(severity_map.keys()):
            severity = severity_map[severity_level_id]
            ids = result[severity]
            if ids:
                formatted_ids = ','.join(ids)
                formatted_output_parts.append(f"{severity}:{formatted_ids}")

        formatted_output = ';'.join(formatted_output_parts)

        return formatted_output


def str_to_list(list_str):
    """
    将列表的字符串表示转换为 Python 列表。

    参数:
        list_str (str): 列表的字符串表示。

    返回:
        list: 转换后的 Python 列表。

    抛出:
        ValueError: 如果输入不是有效的列表字符串表示。
    """
    try:
        # 使用 ast.literal_eval 安全地解析字符串
        result = ast.literal_eval(list_str)
        if not isinstance(result, list):
            raise ValueError("输入不是一个有效的列表字符串表示。")
        return result
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"无效的列表字符串表示: {e}")


def clean_json_string(json_str):
    """
    清理并尝试修正 JSON 字符串中的常见错误。

    参数:
        json_str (str): 需要清理的 JSON 字符串。

    返回:
        str: 清理后的 JSON 字符串。
    """
    # 将单引号替换为双引号以符合 JSON 规范
    cleaned_str = json_str.replace("'", '"')
    return cleaned_str


# 示例用法
if __name__ == "__main__":
    f = DataUtils()
    data_str = "{'componentEsId': '', 'componentName': '', 'componentVersion': '', 'language': '', 'author': None, 'vendor': '', 'homeUrl': '', 'downloadUrl': '', 'sourceUrl': '', 'docUrl': '', 'description': '', 'migrationComponentList': [], 'licenseList': None, 'vulList': None}"

    print(f.vulCount(data_str))
