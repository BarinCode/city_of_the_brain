# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 10:16 AM
# @Author  : Barin
# @FileName: params_validation.py
# @Software: PyCharm
from typing import List, Union

def validation(*args, **kwargs):
    """
    进行参数的验证处理
    """
    if args:
        return None in args
    if kwargs:
        return None in kwargs.values()

