import fnmatch
import os
import sys

# 获取当前脚本文件所在目录的完整路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录的完整路径
root_path = os.path.abspath(os.path.join(current_path, ".."))

# 获取项目根目录的名称
root_folder_name = os.path.basename(root_path)


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


if __name__ == '__main__':
    path = search_file_in_project_folder('config.ini')[0]
    print(path)
