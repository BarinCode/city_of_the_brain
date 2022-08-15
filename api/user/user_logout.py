# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 4:15 PM
# @Author  : Barin
# @FileName: user_logout.py
# @Software: PyCharm

from flask import request, g

from . import bp
from res import make_res
from decorator import token_check
from control.v1 import UserControl

@bp.route('/logout', methods=['GET'])
@token_check
def user_logout():
    """
    用户退出
    """
    token = request.args.get("token", '', type=str)

    UserControl._logout(token)

    res = {
        "name": g.user.us_name
    }
    return make_res(res)
