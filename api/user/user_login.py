import time

from flask import request, current_app

from . import bp
from res import make_res
from control.v1 import UserControl

@bp.route('/login', methods=['POST'])
def user_login():
    """
    用户登入接口
    """
    args = request.form
    username = args.get("username", type=str)
    password = args.get("password", type=str)

    user, token = UserControl._login(username.strip(), password.strip())
    current_app.logger.info("登入成功")

    res = {
        "token": token,
        "username": user.us_name,
        "update": time.time()
    }

    return make_res(res)

