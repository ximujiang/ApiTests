import fnmatch
import os
import yaml
import configparser

from utils import extract

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


def read_config(section, key):
    """
    读取config.ini文件中指定section和key的值
    """
    config_path = search_file_in_project_folder('config.ini')[0]
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get(section, key)


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
