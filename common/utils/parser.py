import re
import base64
import imghdr


def regex(pattern):
    """
    正则检验
    :param pattern: str 正则表达式
    :return:  检验函数
    """
    def validate(value_str):
        """
        检验字符串格式
        :param value_str: str 被检验字符串
        :return: bool 检验是否通过
        """
        if re.match(pattern, value_str):
            return value_str
        else:
            raise ValueError('Invalid params.')

    return validate


def email(email_str):
    """
    检验邮箱格式
    :param email_str: str 被检验字符串
    :return: email_str
    """
    if re.match(r'^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$', email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))


def image_base64(value):
    """
    检查是否是base64图片文件
    :param value:
    :return:
    """
    stri = value.split(',')[0]
    if not re.match(r'data:image/(.+);base64', stri):
        raise ValueError('Invalid image.')
    else:
        print('base64格式正确')


def image_file(value):
    """
    检查是否是图片文件
    :param value:
    :return:
    """
    try:
        file_type = imghdr.what(value)
    except Exception:
        raise ValueError('Invalid image.')
    else:
        if not file_type:
            raise ValueError('Invalid image.')
        else:
            return value


def article_state(value):
    """
    检查是否是文章状态信息
    :param value:
    :return:
    """
    if value not in ['已发布', '草稿']:
        raise ValueError('{} is not a valid article status'.format(value))
    else:
        return value
