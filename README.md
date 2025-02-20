## 目录说明
```plain
Report_Test
│
├── /api                  # 封装接口：接口调用的代码
├── /casedata             # 存放测试数据或数据模板
├── /common               # 公共模板：共享的公共函数或模板
├── /config               # 全局配置文件
├── /Downloads            # 存放下载文件
├── /logs                 # 日志文件：记录日志信息
├── /Packages             # 存储检测包
├── /Reports              # 报告相关操作：生成和删除
│
├── /Test_case1_ReportSheet    # 报告sheet页测试用例：首行测试用例
├── /Test_case2_ReportInfo     # 报告信息测试用例：各sheet页报告信息
│
├── conftest.py           # pytest 配置：定义 fixture 和钩子函数
├── main.py               # 测试运行函数：测试套件入口点
└── pytest.ini            # pytest 配置文件：定制 pytest 行为
```



## 运行测试
#### 打开项目安装依赖
```plain
pip install requirments.txt
```

#### 更改配置文件
`/config/sca.yaml`

```yaml
# 这个字段选择当前测试环境配置
use:
  192.168.111.6

192.168.111.6:
  base_url: 'https://192.168.111.6' # 环境url
  api_port: '30002' # 环境openapi的端口号
  web_port: '30001' # 环境web端口号
  user: 'circle' # sca用户
  OpenApiUserToken: '9802cfa145104ac29dd2480c61191215' # sca-Token
```

#### 运行`main.py`
> main 会运行所有的测试用例
>

##### 运行逻辑
1. common/yaml_utils.py 初始化测试环境配置
2. 收集所有测试用例
3. 运行 conftest 前置
    1. `a_RunMethod_instance()`创建 request 实例
    2. `project_manager()`判断测试项目是否存在，不存在则重新创建项目并删除旧报告再使用新项目生成报告
    3. `Generate_Report()`每个模块测试时都检查报告是否存在不存在则生成相应报告
4. 如果存在项目和报告文件不会再创建报告，直接使用当前报告测试速度会快很多
5. 按顺序执行测试用例
6. 运行 conftest 后置
    1. 钩子函数记录测试运行结果
    2. `delete_reports()`如果测试全部通过则执行删除报告和项目，测试有一条用例失败则保留测试报告和用例以供调试查看
    3. 释放 request 实例



#### 查看测试结果
![](https://cdn.nlark.com/yuque/0/2025/png/46069453/1739950695497-89fd76d0-9d34-45af-a86f-29c0f4a42c0f.png)

1. 通过用例名称查看是哪个报告测试失败
2. sheet 页和标题测试用例在终端可以直接查看到对比结果
    1. 如果字段信息顺序不同会报错 顺序不匹配
    2. 如果没找到测试字段会报错 not found
3. sheet 页内容需要在日志中查看 ERROR 日志查看到对比结果
    1. 可以`Ctrl+f`搜索 ERROR
4. `test_Report_ApplicationInfo.py`

![](https://cdn.nlark.com/yuque/0/2025/png/46069453/1739950816744-7c9b6d98-d7f3-4634-a3e0-722fa7ea272b.png)

5. `test_Report_ComponentInfo.py`

![](https://cdn.nlark.com/yuque/0/2025/png/46069453/1739950878271-f6dad343-ebd4-4471-8d06-4aad917e6c66.png)

6. 有些数据可能只是顺序不同但是内容相同也会测试失败，这是因为 web 接口获取到的数据顺序和报告中顺序不一致，但是大部分顺序都是找到最优顺序时和报告匹配的，只有少部分像上面这个一样（目前已优化）【`common/helpers.py`在辅助模块中自定义方法在`EXCEl.verify_other_fields()`对特定字段进行精准匹配测试】
7. <font style="background-color:#FBDE28;">检出组件信息 sheet 页</font>还可以通过查看标记报告副本直接查看数据不匹配的地方
    1. ![](https://cdn.nlark.com/yuque/0/2025/png/46069453/1739951199726-5e7fecfa-eca1-48ff-a017-ca2ce1a33d49.png)
    2. 报告测试完成后会生成标记副本高亮显示不匹配的单元格（应用信息 sheet 页不支持），以后的 sheet 页测试都可以支持。
    3. ![](https://cdn.nlark.com/yuque/0/2025/png/46069453/1739951298682-db953113-838c-47d6-846c-680d17b45020.png)



#### 调试和回归测试
1. 有测试不通过的用例时会保留报告和项目，可以查看日志和 web 内容验证匹配失败的数据
2. 运行`get_xxxx.py`查看接口数据是否获取正确
3. 查看 casedada 内容是否正确
4. 如果确实是报告数据错误可以删除该报告然后再次运行`main`即可重新下载报告进行回归测试
5. 运行`Reports/Delete_Report.py`可以删除所有报告，进行回归测试



## 新增测试用例
#### 创建数据模板
+ 在casedata 中创建需要测试的 sheet 页数据模板

```json
# 如：源码检测-检出路径列表
"sourceInfo": {
  "hashCode": "{ComponentInfo.hashCode}",
  "风险等级": "{ComponentInfo.securityLevelId}",
  "组件名称": "{ComponentInfo.componentNameVendor}",
  "版本号": "{ComponentInfo.version}",
  "所属语言": "{ComponentInfo.language}",
  "恶意组件": "{ComponentInfo.poison}",
  "私有组件": "{ComponentInfo.isPrivate}",
  "漏洞数": "{ComponentDetailInfo}",
  "漏洞编号": "{ComponentVulList.records}",
  "许可证信息": "{ComponentInfo.license}",
  "依赖方式": "{ComponentDependencyInfo.dependTypeStr}",
  "依赖层级": "{ComponentDependencyInfo.dependLevel}",
  "组件作用域": "{ComponentDependencyInfo.scopes}",
  "组件完整性": "{ComponentDependencyInfo.jarCompletenessCheck}",
  "依赖路径": "{ComponentDependencyInfo.dependencyPath}",
  "文件位置": "{ComponentDependencyInfo.filePath}",
  "引入组件": "",
  "依赖声明代码": ""
}
```

#### 封装接口
+ 在 api 中创建`get_xxxx.py`封装接口获取 web 上的数据，需要在多个接口获取数据则创建多个函数

```python
# 如：获取组件列表接口

# web接口获取组件漏洞列表
def get_ComponentVulList(taskId, **kwargs):
    url = sca_env['base_url'] + f"/sca/api-v1/commonDetail/Component/getVulListByComponentId"
    headers = {
        'OpenApiUserToken': sca_env['OpenApiUserToken'],
    }
    payload = {"pageNum": 1,
               "pageSize": 1000,
               "taskId": taskId,
               "hashCode": kwargs['hashCode']
              }

    try:
        response = RunMethod().api_run("POST", url, json=payload, headers=headers)
        if response.json()['code'] == 0:
            log.info("get_ComponentVulList-获取组件漏洞列表成功")
            print(f"get_ComponentVulList-获取组件漏洞列表成功{response.json()}")
            return response.json()
        else:
            log.error(f"get_ComponentVulList-获取组件漏洞列表请求失败{response.json()}")
            print(f"get_ComponentVulList-获取组件漏洞列表请求失败{response.json()}")

    except Exception as e:
        log.error(f"get_ComponentVulList-获取组件漏洞列表失败-{e}")
        print(e)
```

+ 其他所有接口都可参照这个格式更改 url 接口参数和日志信息即可



#### 动态数据获取
在`get_xxxx.py`中创建`class InfoGet`类并实现功能：

##### InfoGet 对象初始化
```python
class InfoGet:
    def __init__(self, taskId_type, ComponentInfo):
        self.taskId = ini.get_value('variables', taskId_type)
        self.ComponentInfo = ComponentInfo
        self.objects = None
        self.json_util = JsonUtil(r'casedata\ComponentInfo.json')  # 使用json组件信息模板
```

1. InfoGet对象接收一个固定参数taskId_type用于区分是哪个任务，通过读取`api/variables.ini`变量文件获取：
    1. sourcetaskid-源码检测任务
    2. binarytaskid-二进制检测任务
    3. imagetaskid-镜像检测任务
2. 接受 ComponentInfo 参数用户获取单个组件信息，因为有些接口需要组件信息作为参数
3. self.objects 用于接受所有需要使用的接口数据对象
4. self.json_util = JsonUtil(r'casedata\ComponentInfo.json')   使用数据模板初始化 json 处理对象

##### 初始化接口对象数据
```python
def _initialize_objects(self):
    """初始化接口数据"""
    data = {
        "componentName": self.ComponentInfo['componentName'],
        "hashCode": self.ComponentInfo['hashCode']
    }

    self.objects = {
        'ComponentInfo': self.ComponentInfo,
        'ComponentVersionInfo': get_OtherComponentVersion(
            data['hashCode'], 
            data['language']
        )['data'],
        'ComponentVulList': get_ComponentVulList(
            self.taskId,
            hashCode=data['hashCode']
        )['data'],
        'LicenseList': get_LicenseList(
            self.taskId,
            hashCode=data['hashCode']
        )['data'],
    }
```

1. data 中获取一些接口请求中需要使用的组件信息参数 如组件名称、组件 hashCode 等
2. objects 用于存储从接口获取到的响应数据：
    1. 如`get_ComponentVulList(self.taskId,hashCode=data['hashCode'])`获取到的数据为：

```json
{
  'code': 0,
  'message': 'success',
  'data': {
    'records': [
      {
      'id': 271897,
      'vulId': 'XMIRROR-E5B7140E-B012C295',
      'vulNumStr': 'XMIRROR-E5B7140E-B012C295|CVE-2019-14697|CNNVD-201908-417|CWE-787',
      'cveId': 'CVE-2019-14697',
      'cnnvdId': 'CNNVD-201908-417',
      'cnvdId': '',
      'xmirrorId': 'XMIRROR-E5B7140E-B012C295',
      'cweId': 'CWE-787',
      .....
      }
    ]
  }
}
```

    2. 所以`ComponentVulList`中的数据为：

```json
'records': [
      {
      'id': 271897,
      'vulId': 'XMIRROR-E5B7140E-B012C295',
      'vulNumStr': 'XMIRROR-E5B7140E-B012C295|CVE-2019-14697|CNNVD-201908-417|CWE-787',
      'cveId': 'CVE-2019-14697',
      'cnnvdId': 'CNNVD-201908-417',
      'cnvdId': '',
      'xmirrorId': 'XMIRROR-E5B7140E-B012C295',
      'cweId': 'CWE-787',
      .....
      }
    ]
```

    3. 需要取哪一部分数据需要根据测试的内容来判断

##### 清洗接口数据
将获取到的接口数据二次清洗变为报告中一致的内容格式

```json
def _clean_app_info(self, app_info, transformations):
    """清洗app_info中的数据"""
    if self.objects is None:
        error_msg = f"componentName: {self.ComponentInfo['componentName']} InfoGet接口数据初始化失败"
        log.error(error_msg)
        return error_msg

    data_Trans = DataUtils()
    for key, transform_func in transformations.items():
        if key in app_info:
            try:
                app_info[key] = transform_func(app_info[key])
            except Exception as e:
                log.error(
                    f"componentName: {self.ComponentInfo['componentName']} 字段 '{key}' 数据清洗出错 - {e}")
                continue

    return app_info
```

1. `_clean_app_info`接受两个必要参数 app_info：初始的测试数据，transformation：需要清洗的数据对象
2. 迭代清洗数据对象清洗 app_info 中的数据，返回清洗后的最终数据

##### 销毁 object 对象
销毁 object

```json
def _destroy_objects(self):
    """销毁应用信息对象"""
    if self.objects:
        for obj_name in list(self.objects.keys()):
            del self.objects[obj_name]
        self.objects = None
```



#### 获取测试数据
在`InfoGet`类中创建`get_xxxx_appInfo()`函数（根据不同函数获取相应报告的测试数据）

```json
# 获取源码检测检出组件信息
def get_source_appInfo(self):
    if self.objects is None:
        return self._error_response("源码检测检出组件信息")

    app_info = self.json_util.read_ApplicationInfo("sourceInfo", self.objects)

    transformations = {
        '风险等级': DataUtils().riskLevel_Trans,
        '依赖方式': DataUtils().dependencyType_Trans,
        '恶意组件': DataUtils().is_Trans,
        '私有组件': DataUtils().is_Trans,
        '许可证信息': DataUtils().license_Trans,
        '无漏洞可用版本': DataUtils().noVulVersion_Trans,
        '组件依赖路径': DataUtils().dependencyPath_Trans,
        '漏洞数': DataUtils().vulCount,
        '漏洞编号': DataUtils().vulNumber,
    }

    cleaned_app_info = self._clean_app_info(app_info, transformations)
    self._destroy_objects()

    return cleaned_app_info
```

1. 检查接口对象数据是否获取成功
2. 获取初始化数据
3. 创建清洗对象
4. 使用清洗函数获取清洗后的测试数据
5. 销毁接口对象
6. 返回最终测试数据



#### 定义数据清洗方法
在`common/data_utils/DataUtils`中定义清洗方法，在 transformations 中使用对应方法清洗接口数据

如：`DataUtils().riskLevel_Trans`

```json
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
        '5': '无风险'
    }

    # 检查输入是否有效
    if data not in risk_level_map:
        log.error(f"无效的风险等级ID: {data}，请查看相关日志!!")
        raise ValueError(f"无效的风险等级ID: {data}。有效的ID范围是 1 到 5。")

    # 返回对应的描述性字符串
    return risk_level_map[data]
```

一般使用 AI 生成自己稍微调试即可

<font style="color:#DF2A3F;">Prompt</font> 参考：`def xxxx_Trans(self,data)`函数实现接受一个字符串数据 “（部分接口获取到的数据）”实现将其转换为（报告数据）的格式并返回



#### 创建测试用例
1. 在 Test_case2_ReportInfo 中创建新的测试用例
2. 创建不同报告的测试函数

##### 测试函数实现
###### 数据初始化
```python
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
```

1. report_file_path ：测试报告绝对路径
2. marked_output_file_path ：标记副本绝对路径
3. 使用`common/excel_utils.py/Excel`对象创建 excel 实例接受一个报告路径参数和副本路径参数
4. excel.create_report_result() 创建或打开标记副本
5. target_sheet 定义测试 sheet 页
6. `excel.get_ReportSheet()`函数加载指定的 sheet 工作表数据，接收两个参数：指定 sheet 标题和空数据替换
7. 根据任务 id 获取任务组件列表信息，这里使用 variables 变量文件获取指定场景的任务 id，未获取到则报错返回
8.  all_failed_cells 存储测试失败的单元格位置
9. failed_flag 记录测试失败，未找到匹配行或找多多个匹配行

###### 数据匹配测试
```json
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
```

1. 遍历组件列表单独获取需要测试的组件信息
2. 使用任务 id 和组件信息创建`InfoGet`对象，并使用对应的方法获取测试数据（casedata)
3. 获取组件名称（主要使用在日志打印便于排查）
4. keys_to_match 定义需要匹配的键（确定组件唯一性的字段）
5. 使用`Excel.find_matching_rows()`方法查找到报告中与测试数据的唯一匹配行（接收测试数据和唯一匹配键参数），保存到matching_rows
6. 初步测试判断 matching_rows 是不是只有一个，如果大于两个则测试失败（报告可能存在重复数据）
7. 如果 matching_rows 为 0 则未找到匹配行测试失败

###### 保存测试结果
```json
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
```

1. 将不匹配的单元格同意保存到标记副本中
2. 断言测试用例



## 用例和数据维护
#### sheet 页标题及首行测试
`casedata/供应链场景excel报告测试.xlsx`

1. 使用所属模块字段和用例名称字段作为数据匹配关键字（不可更改）
2. 将提取数据字段中的数据和报告数据进行匹配测试	
    1. 内容不匹配将返回差异
    2. 缺少 sheet 页会返回 not found
    3. 顺序不匹配会返回顺序不匹配（如果不需要测试顺序可以删除断言代码）



#### json 测试数据
1. 只需参照现在的格式填写即可
2. 报告中需要测试的字段为键，使用{}动态获取接口数据



#### 更换测试包
1. 在`Packages`目录中加入测试包
2. 在不同检测接口中替换文件路径即可

```python
file_path = os.path.join(BASE_PATH, r'Packages\curl.zst')
```

【后续可考虑使用配置文件动态切换检测包，或在运行函数中循环读取检测包同时测试多个包】



