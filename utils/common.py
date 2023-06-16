import fnmatch
import functools
import os

import pytest
import yaml
import configparser

from utils import extract, render_template_obj
import inspect
from typing import Dict

# from utils.base import Tenant
from utils.log import log

# 获取当前脚本文件所在目录的完整路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录的完整路径
root_path = os.path.abspath(os.path.join(current_path, ".."))

# 获取项目根目录的名称
root_folder_name = os.path.basename(root_path)


def read_yaml(file_path):
    """
    读取yaml格式文件
    :param file_path: 文件路径
    :return: 字典类型的文件内容
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        return content


def update_yaml_file(file_path, key, value):
    with open(file_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
    yaml_data[key] = value
    with open(file_path, 'w') as f:
        yaml.safe_dump(yaml_data, f, default_flow_style=False)


def read_config(section, config_path=None, options=None):
    """
    从配置文件中读取指定section下的配置信息。

    Args:
        section: str
            要读取的section名称。
        config_path: str
            要读取的config配置路径。
        options: list of str or str, optional
            要读取的配置项名称列表或单个配置项名称。如果为None则返回整个section的配置信息。

    Returns:
        dict or str
        如果传入的options为None，则返回整个section配置信息的字典；否则，如果options为单个配置项名，则返回该配置项的值；否则返回指定配置项信息的字典。

    Raises:
        TypeError：如果传入的options既不是str也不是list。

    Examples:
        >>> read_config('server', 'host')
        'localhost'
        >>> read_config('database', ['user', 'pass'])
        {'user': 'root', 'pass': '123456'}
    """
    if config_path is None:
        config_path = search_file_in_project_folder('config.ini')[0]  # 搜索config.ini文件的路径
    config = configparser.ConfigParser()
    config.read(config_path)  # 读取config文件
    if options is None:
        # 如果options为None，则返回整个section的配置
        return dict(config.items(section))
    else:
        if isinstance(options, str):
            # 如果options为单个配置项名，则返回该配置项的值
            return config.get(section, options)
        elif isinstance(options, list):
            # 如果options为配置项名的列表，则返回对应配置项的字典
            return {option: config.get(section, option) for option in options}
        else:
            # 如果options既不是str也不是list，则抛出TypeError异常
            raise TypeError("'options' must be a string or a list of strings.")


def write_config(section, key, value):
    """
    写入config.ini文件中指定section和key的值
    """
    config_path = search_file_in_project_folder('config.ini')[0]
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set(section, key, value)
    with open(config_path, 'w') as f:
        config.write(f)


def check_dir(path):
    if not path:
        return ""
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def check_file(path):
    if not path:
        return ""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist.")
    return path


def search_file_in_project_folder(file_name: str):
    """
    在整个Python项目文件夹下搜索指定名称的文件，并返回文件路径。
    :param file_name: 指定文件名称，如：'target_file.txt'
    :return: 文件路径列表，如：['project_folder/sub_folder/target_file.txt']
    """
    result = []  # 存储文件路径列表

    # 遍历整个根目录下的所有子文件夹，找到指定名称的文件并返回路径
    for root, dirnames, filenames in os.walk(root_path):
        for filename in fnmatch.filter(filenames, file_name):
            result.append(os.path.join(root, filename))

    return result


def extract_response(response, extract_obj: dict):
    """
    从response中提取数据，并以字典形式返回提取结果
    :param response: 请求响应对象
    :param extract_obj: 字典类型参数，用于指定提取规则。字典中每个键值对对应一个需要提取的变量和对应的提取表达式。
                        格式示例：{'变量名': '提取表达式'}
    :return: 字典类型，包含提取的结果。格式示例：{'变量名': '提取结果'}
    """
    extract_result = {}  # 存储提取结果的字典，初始化为空字典
    if isinstance(extract_obj, dict):  # 判断extract_obj是否为字典类型
        for extract_var, extract_expression in extract_obj.items():  # 遍历extract_obj中的每个键值对
            extract_var_value = extract.extract_by_object(response, extract_expression)
            # 调用一个名为extract的模块/函数，# 对response按照指定表达式进行提取，返回提取结果
            extract_result[extract_var] = extract_var_value  # 将提取结果以键值对的形式存储到extract_result字典中
        return extract_result  # 返回提取结果
    else:
        return extract_result  # 如果extract_obj不是字典类型，返回空字典


# def get_test_step_data(step, man) -> Dict:
#     """
#     从yaml文件中获取测试数据
#     :param get_test_data:
#     :param step:
#     :param step_name:
#     :return: 测试数据字典
#     """
#     log.debug(step)
#     log.debug(get_test_data)
#     # 获取调用该函数的模块
#     return get_test_data/


def get_test_data(step):
    """
    获取测试数据
    :param step: 测试步骤
    :return: 测试步骤
    """
    # 获取当前测试数据文件和测试函数名
    test_data_file, func_name = get_test_data_file()
    # 检查测试数据文件是否存在
    check_file(test_data_file)
    # 读取测试数据
    data = read_yaml(test_data_file)
    # 获取测试用例数据
    case_data = data[func_name]
    # 对测试数据进行模板渲染
    render_template_data = render_template_obj.rend_template_any(case_data, case_data)
    # 获取指定步骤的测试数据
    step_data = render_template_data[step]
    return step_data


def update_test_data(step, value):
    """
    更新测试数据
    :param step: 测试步骤
    :param value: 更新的值
    :return: 无返回值
    """
    # 获取当前测试数据文件和测试函数名
    test_data_file, func_name = get_test_data_file()
    # 读取测试数据
    data = read_yaml(test_data_file)
    # 更新需要提取值的步骤
    data[func_name][step]['extract'].update(value)
    # 将更新后的数据重新写入测试数据文件
    with open(test_data_file, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)


def get_test_data_file():
    """
    获取当前运行测试用例的文件名和测试方法名，构造测试数据文件的路径
    :return: 返回测试数据文件路径和测试方法名
    """
    frame = inspect.currentframe()
    filename = None
    func_name = None
    while frame:
        filename = frame.f_code.co_filename  # 获取当前运行测试用例的文件名
        if is_test_file(filename):  # 判断文件名以 "test" 开头或者以 "test" 结尾
            func_name = frame.f_code.co_name  # 获取当前运行的测试方法名
            break
        frame = frame.f_back
    if filename is None:
        raise ValueError("Cannot find test data file.")
    dirname = os.path.dirname(filename)
    # 构造测试数据文件路径，文件名为当前运行测试用例的文件名去除扩展名后加上'_data.yaml'
    test_data_file = os.path.join(dirname, f"{os.path.splitext(os.path.basename(filename))[0]}_data.yaml")
    return test_data_file, func_name


def is_test_file(file_path):
    """
    判断传入的文件路径是否为测试文件
    """
    file_name = os.path.basename(file_path)
    return file_name.startswith('test') or file_name.endswith('test')
