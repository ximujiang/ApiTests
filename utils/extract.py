from requests import Response
import jsonpath
import jmespath
import re
from . import exceptions


def extract_by_object(response: Response, extract_expression: str):
    """
    从响应对象中提取值。
    :param response: 响应对象，要从中提取值的对象
    :param extract_expression: 表达式，用于提取符合条件的值，可以是以下类型：
        1. 字符串，表示要直接取值的属性名，包括以下属性："status_code", "url", "ok", "encoding", "text"
        2. 表达式字符串，如 "headers['content-type']"，表示从 headers 中提取 "content-type" 的值
        3. JMESPath 表达式，例如 "headers[content-type]"，用于从 headers 和 cookies 中提取值
        4. JSONPath 表达式，例如 "$.data[0].name"，用于从响应 JSON 的数据中提取值
        5. 正则表达式，例如 "re.findall('value=(.*?);', text)"，用于从响应文本中提取值
    :return: 如果符合条件的值存在，返回提取的值，否则返回 None
    """
    if not isinstance(extract_expression, str):
        return extract_expression

    # 将 response 转换为字典
    res = {
        "headers": response.headers if response else {},
        "cookies": dict(response.cookies if response else {})
    }

    # 使用属性名直接取值
    if extract_expression in ["status_code", "url", "ok", "encoding", "text"]:
        return getattr(response, extract_expression)

    # 使用 JMESPath、表达式字符串从 headers 和 cookies 中取值
    elif extract_expression.startswith('headers') or extract_expression.startswith('cookies'):
        return extract_by_jmespath(res, extract_expression)

    # 使用 JSONPath 从响应 JSON 中取值
    elif extract_expression.startswith('body') or extract_expression.startswith('content'):
        try:
            response_parse_dict = response.json()
            return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')

    # 使用 JSONPath 从响应 JSON 中取值
    elif extract_expression.startswith('$.'):
        try:
            response_parse_dict = response.json()
            return extract_by_jsonpath(response_parse_dict, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')

    # 使用正则表达式从响应文本中取值
    elif '.+?' in extract_expression or '.*?' in extract_expression:
        return extract_by_regex(response.text, extract_expression)

    # 其它非取值表达式，直接返回
    else:
        return extract_expression


def extract_by_jsonpath(extract_obj: dict, extract_expression: str):
    """
    通过jsonpath表达式从字典中获取数据
    :param extract_obj: 需要提取数据的字典, eg:{"name":"Alice","age":20,"scores":[60,70,80],"profile":
                                        {"gender":"female","hometown":"New York"}}
    :param extract_expression: jsonpath表达式, eg:"$.profile.gender"/"$.scores[*]"
    :return: 如果符合条件的值存在，返回提取的第一个值或全部,否则返回None ,eg:输出"female"/输出[60, 70, 80]
    """
    # 检查extract_expression是否为字符串类型，如果不是则直接返回extract_expression
    if not isinstance(extract_expression, str):
        return extract_expression

    # 通过jsonpath表达式从字典中获取数据
    extract_value = jsonpath.jsonpath(extract_obj, extract_expression)

    # 如果没有获取到数据，则返回None
    if not extract_value:
        return

    # 如果获取到的数据只有一个，则直接返回该数据
    elif len(extract_value) == 1:
        return extract_value[0]

    # 如果获取到的数据有多个，则返回所有数据
    else:
        return extract_value


def extract_by_jmespath(extract_obj: dict, extract_expression: str):
    """
    根据JMESPath表达式从字典中提取数据
    :param extract_obj: 需要进行数据提取的字典对象, eg:{"name":"John","age":28,"address":
        {"street":"123 Main St","city":"Anytown","state":"CA","zip":"12345"}}
    :param extract_expression: jmespath表达式，用于指定需要提取的数据,eg:address.city
    :return: 表达式提取出的对应数据
    """
    # 如果表达式不是字符串类型，则直接返回该表达式
    if not isinstance(extract_expression, str):
        return extract_expression
    try:
        # 使用jmespath表达式从字典对象中提取出对应数据
        extract_value = jmespath.search(extract_expression, extract_obj)
        return extract_value  # 返回提取出的值
    except Exception as msg:  # 如果表达式提取失败，则抛出异常信息
        raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')


def extract_by_regex(extract_obj: str, extract_expression: str):
    """
    使用正则表达式从extract_obj中提取数据。
    :param extract_obj: 待提取的字符串
    :param extract_expression: 匹配表达式，应为合法的正则表达式字符串
    :return: 若匹配成功，则返回匹配结果。若匹配失败，则返回空字符串。
             若匹配结果有多个，则返回一个列表。
    """
    # 判断extract_expression是否为字符串类型
    # 如果extract_expression不是字符串类型，则直接返回提取表达式
    if not isinstance(extract_expression, str):
        return extract_expression

    extract_value = re.findall(extract_expression, extract_obj, flags=re.S)

    # 调用re模块的findall方法，对extract_obj进行正则匹配
    if not extract_value:  # 如果未匹配到任何结果
        return ''  # 返回空字符串

    # 如果匹配结果只有一个
    elif len(extract_value) == 1:
        # 返回第一个匹配结果
        return extract_value[0]

    # 如果匹配结果有多个
    else:
        # 返回包含所有匹配结果的列表
        return extract_value
