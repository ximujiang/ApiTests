from jinja2 import Template
import re
from utils.log import log


class NewDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = NewDict(value)
        return value


# 将模板字符串中的变量解析为字符串，用实际的值替换
def replace_template_str(template_str, *args, **kwargs):
    def _replace_match(match) -> str:
        res = match.group()
        res_ = str(res).lstrip('${').rstrip('}')

        # 如果模板字符串嵌套了变量，则需要先将嵌套的变量解析为字符串，再用实际值替换
        if res_.count('${') > res_.count('}'):
            return res
        instance = Template(res_, variable_start_string='${', variable_end_string='}')
        return '${' + instance.render(*args, **kwargs) + '}'

    return re.sub('\$\{(.+?)\}', _replace_match, template_str)


# 渲染模板字符串
def rend_template_str(template_str, *args, **kwargs):
    # 重新解析可能嵌套了变量的模板字符串
    def _render_template(template_str):
        instance = Template(template_str, variable_start_string='${', variable_end_string='}')
        return instance.render(**kwargs)

    # 判断模板字符串是否为单个变量，并且变量名为数字
    def _is_numeric_variable(template_str):
        # 如果模板字符串不是单个变量，则不是数字变量
        if not _is_single_variable(template_str):
            return False
        variable_name = template_str.lstrip('${').rstrip('}')
        # 如果变量名不以点开头，或者点后面不是数字，则不是数字变量
        if not variable_name.startswith('.') or not variable_name[1:].isdigit():
            return False
        return True

    # 用数字变量名解析出对应的实际值
    def _resolve_numeric_variable(template_str):
        variable_name = template_str.lstrip('${').rstrip('}')
        index = int(variable_name[1:])
        value = args[0][index]
        return value

    # 判断模板字符串是否为单个变量
    def _is_single_variable(template_str):
        stripped = template_str.strip()
        return stripped.startswith('${') and stripped.endswith('}') and stripped.count('${') == 1

    # 如果模板字符串为数字变量，则使用相应的值替换它
    if _is_numeric_variable(template_str):
        value = _resolve_numeric_variable(template_str)
        log.debug(f"resolved {template_str} to {value}")
        return value

    # 如果模板字符串不是数字变量，则需进一步解析
    else:
        # 先将嵌套变量解析为字符串，得到一个新的模板字符串
        rendered = replace_template_str(template_str, *args, **kwargs)
        # 使用新的模板字符串渲染出最终结果
        result = _render_template(rendered)
        log.debug(f"rendered {template_str} to {result}")
        return result


def rend_template_obj(t_obj: dict, *args, **kwargs):
    """
    渲染模板对象，将其中的占位符替换为实际的值

    :param t_obj: dict类型，需要渲染的模板对象
    :param args: 传递给渲染模板字符串的位置参数
    :param kwargs: 传递给渲染模板字符串的关键字参数
    :return: 渲染后的模板对象
    """
    if isinstance(t_obj, dict):
        for key, value in t_obj.items():
            if isinstance(value, str):
                # 如果value为字符串，则调用rend_template_str渲染模板字符串
                t_obj[key] = rend_template_str(value, *args, **kwargs)
            elif isinstance(value, dict):
                # 如果value为字典，则递归调用rend_template_obj渲染模板对象
                rend_template_obj(value, *args, **kwargs)
            elif isinstance(value, list):
                # 如果value为列表，则调用rend_template_array渲染模板列表
                t_obj[key] = rend_template_array(value, *args, **kwargs)
            else:
                pass
    return t_obj


def rend_template_array(t_array, *args, **kwargs):
    """
       传 list 对象，通过模板字符串递归查找模板字符串
    """
    if isinstance(t_array, list):
        new_array = []
        for item in t_array:
            if isinstance(item, str):
                new_array.append(rend_template_str(item, *args, **kwargs))
            elif isinstance(item, list):
                new_array.append(rend_template_array(item, *args, **kwargs))
            elif isinstance(item, dict):
                new_array.append(rend_template_obj(item, *args, **kwargs))
            else:
                new_array.append(item)
        return new_array
    else:
        return t_array


def rend_template_any(any_obj, *args, **kwargs):
    """渲染模板对象:str, dict, list"""
    if isinstance(any_obj, str):
        return rend_template_str(any_obj, *args, **kwargs)
    elif isinstance(any_obj, dict):
        return rend_template_obj(any_obj, *args, **kwargs)
    elif isinstance(any_obj, list):
        return rend_template_array(any_obj, *args, **kwargs)
    else:
        return any_obj


