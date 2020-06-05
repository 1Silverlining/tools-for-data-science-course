# -*- coding: utf-8 -*- 
"""
    招聘清洗中的 通用方法
"""
import sys
import time
import re
import emoji


def compileFour(text):
    """
        去掉4字节utf8字符 和emoji符号
    """
    text = emoji.demojize(text)
    try:
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return highpoints.sub(u'',text)
    except:
        return text