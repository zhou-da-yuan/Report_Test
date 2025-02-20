def compare_risk(case, data):
    """
    比较两个风险字符串是否相等，忽略其中项的顺序。

    :param case: 第一个字符串
    :param data: 第二个字符串
    :return: 如果两个字符串表示相同的集合则返回 True，否则返回 False
    """

    def normalize_string(s):
        """
        规范化字符串：去除首尾空白字符，按分号分割，去掉每个部分的首尾空白字符，
        并按逗号分割的风险项排序后重新组合成字典。
        """
        # 去除首尾空白字符并按分号分割
        parts = [part.strip() for part in s.strip().split(';') if part.strip()]

        risk_dict = {}
        for part in parts:
            risk_level, licenses = part.split("：", 1)  # 使用中文冒号分割
            licenses_list = sorted([license.strip() for license in licenses.split(",")])
            risk_dict[risk_level.strip()] = licenses_list

        return risk_dict

    # 对两个字符串分别进行规范化处理
    normalized_report_value = normalize_string(case)
    normalized_value = normalize_string(data)

    # 比较规范化后的字典
    return normalized_report_value == normalized_value


# 使用示例
if __name__ == "__main__":
    report_value = "高风险：AGPL-3.0-only, APL-1.0;中风险：EL-2.0, EL-2.2;低风险：BSD-4-Clause, BSD-3-Clause;"
    value = "高风险：APL-1.0, AGPL-3.0-only;中风险：EL-2.2, EL-2.0;低风险：BSD-3-Clause, BSD-2-Clause;"

    print(compare_risk(report_value, value))
    # 输出: True 或 False 根据比较结果