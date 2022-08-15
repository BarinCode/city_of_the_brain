# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:10 PM
# @Author  : Barin
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint

from config import VERSION

bp = Blueprint('user', __name__, url_prefix=f'/{VERSION}/user')

from .user_login import user_login

from .user_register import user_register

from .user_logout import user_logout