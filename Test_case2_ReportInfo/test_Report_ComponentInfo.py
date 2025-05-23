import os
import warnings

from api.get_ComponenyInfo import InfoGet, get_ComponentList
from common.data_utils import DataUtils
from common.excel_utils import Excel
from common.ini_manager import INIManager
from common.log import Log

warnings.filterwarnings("ignore", category=UserWarning)

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = Log()
data_utils = DataUtils()
ini = INIManager(BASE_PATH + r'\api\variables.ini')


def test_source_componentInfo():
    log.info("----------Begin test_source_componentInfo----------")

    report_file_path = os.path.join(BASE_PATH, 'Downloads', '源码检测报告.xlsx')
    marked_output_file_path = os.path.join(BASE_PATH, 'Downloads', '标记副本_源码检测报告.xlsx')  # 标记副本文件路径

    # 初始化Excel类实例，并创建或打开标记副本
    excel = Excel(report_file_path=report_file_path, output_file_path=marked_output_file_path)
    excel.create_report_result()

    target_sheet = '检出组件信息'  # 指定要操作的工作表名称

    # 加载指定的工作表数据
    excel_data = excel.get_ReportSheet(target_sheet, fillna_value='')

    if excel_data is None:
        log.error("加载工作表失败")
        return

    # 获取组件列表信息
    task_id = ini.get_value('variables', 'sourcetaskid')
    ComponentListInfo = get_ComponentList(task_id)['data']['records']

    if not ComponentListInfo:
        log.warning("未获取到组件列表信息")
        return

    all_failed_cells = []
    failed_flag = False

    try:
        # 遍历ComponentListInfo中的每一个组件进行测试
        for component_info in ComponentListInfo:
            try:
                # 获取接口数据（已处理）
                info = InfoGet("sourcetaskid", component_info)
                json_dict = info.get_source_appInfo()

                component_name = json_dict.get('组件名称')

                # 定义需要匹配的键
                keys_to_match = ['组件名称', '版本号', '所属语言']

                log.info(f"正在运行测试 ComponentName:{component_name}...")
                # 查找匹配行
                matching_rows = excel.find_matching_rows(json_dict, keys_to_match, excel_data)

                if len(matching_rows) == 1:
                    log.info("初步测试通过：找到了唯一匹配行")
                    matching_row = matching_rows.iloc[0]

                    # 验证其他字段
                    failed_cells = excel.verify_other_fields(matching_row, json_dict)
                    if failed_cells:
                        log.error("最终测试失败：存在不匹配的字段")
                        all_failed_cells.extend(failed_cells)
                    else:
                        log.info("最终测试通过：所有字段都匹配")
                elif len(matching_rows) > 1:
                    log.error("测试失败：以上条件找到了多于一行的匹配")
                    failed_flag = True
                else:
                    log.error("测试失败：未找到任何匹配行")
                    failed_flag = True

            except KeyError as e:
                log.error(f"缺少必要的键: {e}")
                continue
            except Exception as e:
                log.error(f"在处理组件 {component_name} 时发生错误: {e}")
                continue

    except Exception as e:
        log.error(f"在测试过程中发生错误: {e}")
        assert False

    # 统一保存所有不匹配的结果
    if all_failed_cells:
        excel.mark_cells_in_sheet(all_failed_cells, sheet_name=target_sheet)
        print("所有不匹配内容已标记到输出文件中")
        log.error("测试失败-所有不匹配内容已标记到输出文件中")
        assert False, '源码报告【检出组件信息】测试失败：存在不匹配的内容，请查看输出文件和日志！'
    elif failed_flag:
        log.error("测试失败-报告中可能存在重复数据或缺少某个组件数据")
        assert False, '源码报告【检出组件信息】测试失败：报告中可能存在重复数据或缺少某个组件数据，请查看输出文件和日志！'
    else:
        print("所有测试均通过，无需要标记的不匹配内容")
        log.info("测试通过")
        assert True, '源码报告【检出组件信息】测试通过！'


# 二进制报告检出组件信息测试
def test_binary_componentInfo():
    log.info("----------Begin test_binary_componentInfo----------")

    report_file_path = os.path.join(BASE_PATH, 'Downloads', '二进制检测报告.xlsx')
    marked_output_file_path = os.path.join(BASE_PATH, 'Downloads', '标记副本_二进制检测报告.xlsx')  # 标记副本文件路径

    # 初始化Excel类实例，并创建或打开标记副本
    excel = Excel(report_file_path=report_file_path, output_file_path=marked_output_file_path)
    excel.create_report_result()

    target_sheet = '检出组件信息'  # 指定要操作的工作表名称

    # 加载指定的工作表数据
    excel_data = excel.get_ReportSheet(target_sheet, fillna_value='')

    if excel_data is None:
        log.error("加载工作表失败")
        return

    # 获取组件列表信息
    task_id = ini.get_value('variables', 'binarytaskid')
    ComponentListInfo = get_ComponentList(task_id)['data']['records']

    if not ComponentListInfo:
        log.warning("未获取到组件列表信息")
        return

    all_failed_cells = []
    failed_flag = False

    try:
        # 遍历ComponentListInfo中的每一个组件进行测试
        for component_info in ComponentListInfo:
            try:
                # 获取接口数据（已处理）
                info = InfoGet("binarytaskid", component_info)
                json_dict = info.get_binary_appInfo()

                component_name = json_dict.get('组件名称')

                # 定义需要匹配的键
                keys_to_match = ['组件名称', '版本号', '所属语言']

                log.info(f"正在运行测试 ComponentName:{component_name}...")
                # 查找匹配行
                matching_rows = excel.find_matching_rows(json_dict, keys_to_match, excel_data)

                if len(matching_rows) == 1:
                    log.info("初步测试通过：找到了唯一匹配行")
                    matching_row = matching_rows.iloc[0]

                    # 验证其他字段
                    failed_cells = excel.verify_other_fields(matching_row, json_dict)
                    if failed_cells:
                        log.error("最终测试失败：存在不匹配的字段")
                        all_failed_cells.extend(failed_cells)
                    else:
                        log.info("最终测试通过：所有字段都匹配")
                elif len(matching_rows) > 1:
                    log.error("测试失败：以上条件找到了多于一行的匹配")
                    failed_flag = True
                else:
                    log.error("测试失败：未找到任何匹配行")
                    failed_flag = True

            except KeyError as e:
                log.error(f"缺少必要的键: {e}")
                continue
            except Exception as e:
                log.error(f"在处理组件 {component_name} 时发生错误: {e}")
                continue

    except Exception as e:
        log.error(f"在测试过程中发生错误: {e}")
        assert False

    # 统一保存所有不匹配的结果
    if all_failed_cells:
        excel.mark_cells_in_sheet(all_failed_cells, sheet_name=target_sheet)
        print("所有不匹配内容已标记到输出文件中")
        log.error("测试失败-所有不匹配内容已标记到输出文件中")
        assert False, '二进制报告【检出组件信息】测试失败：存在不匹配的内容，请查看输出文件和日志！'
    elif failed_flag:
        log.error("测试失败-报告中可能存在重复数据或缺少某个组件数据")
        assert False, '二进制报告【检出组件信息】测试失败：报告中可能存在重复数据或缺少某个组件数据，请查看输出文件和日志！'
    else:
        print("所有测试均通过，无需要标记的不匹配内容")
        log.info("测试通过")
        assert True, '二进制报告【检出组件信息】测试通过！'


# 镜像报告检出软件包信息测试
def test_image_componentInfo():
    log.info("----------Begin test_image_componentInfo----------")

    report_file_path = os.path.join(BASE_PATH, 'Downloads', '镜像检测报告.xlsx')
    marked_output_file_path = os.path.join(BASE_PATH, 'Downloads', '标记副本_镜像检测报告.xlsx')  # 标记副本文件路径

    # 初始化Excel类实例，并创建或打开标记副本
    excel = Excel(report_file_path=report_file_path, output_file_path=marked_output_file_path)
    excel.create_report_result()

    target_sheet = '检出组件信息'  # 指定要操作的工作表名称

    # 加载指定的工作表数据
    excel_data = excel.get_ReportSheet(target_sheet, fillna_value='')

    if excel_data is None:
        log.error("加载工作表失败")
        return

    # 获取组件列表信息
    task_id = ini.get_value('variables', 'imagetaskid')
    ComponentListInfo = get_ComponentList(task_id)['data']['records']

    if not ComponentListInfo:
        log.warning("未获取到组件列表信息")
        return

    all_failed_cells = []
    failed_flag = False

    try:
        # 遍历ComponentListInfo中的每一个组件进行测试
        for component_info in ComponentListInfo:
            try:
                # 获取接口数据（已处理）
                info = InfoGet("imagetaskid", component_info)
                json_dict = info.get_image_appInfo()

                component_name = json_dict.get('组件名称')

                # 定义需要匹配的键
                keys_to_match = ['组件名称', '版本号', '组织']

                log.info(f"正在运行测试 ComponentName:{component_name}...")
                # 查找匹配行
                matching_rows = excel.find_matching_rows(json_dict, keys_to_match, excel_data)

                if len(matching_rows) == 1:
                    log.info("初步测试通过：找到了唯一匹配行")
                    matching_row = matching_rows.iloc[0]

                    # 验证其他字段
                    failed_cells = excel.verify_other_fields(matching_row, json_dict)
                    if failed_cells:
                        log.error("最终测试失败：存在不匹配的字段")
                        all_failed_cells.extend(failed_cells)
                    else:
                        log.info("最终测试通过：所有字段都匹配")
                elif len(matching_rows) > 1:
                    log.error("测试失败：以上条件找到了多于一行的匹配")
                    failed_flag = True
                else:
                    log.error("测试失败：未找到任何匹配行")
                    failed_flag = True

            except KeyError as e:
                log.error(f"缺少必要的键: {e}")
                continue
            except Exception as e:
                log.error(f"在处理组件 {component_name} 时发生错误: {e}")
                continue

    except Exception as e:
        log.error(f"在测试过程中发生错误: {e}")
        assert False

    # 统一保存所有不匹配的结果
    if all_failed_cells:
        excel.mark_cells_in_sheet(all_failed_cells, sheet_name=target_sheet)
        print("所有不匹配内容已标记到输出文件中")
        log.error("测试失败-所有不匹配内容已标记到输出文件中")
        assert False, '镜像报告【检出组件信息】测试失败：存在不匹配的内容，请查看输出文件和日志！'
    elif failed_flag:
        log.error("测试失败-报告中可能存在重复数据或缺少某个组件数据")
        assert False, '镜像报告【检出组件信息】测试失败：报告中可能存在重复数据或缺少某个组件数据，请查看输出文件和日志！'
    else:
        print("所有测试均通过，无需要标记的不匹配内容")
        log.info("测试通过")
        assert True, '镜像报告【检出组件信息】测试通过！'
