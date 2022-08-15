from flask import request

from . import bp
from res import make_res, ResponseCode
from control.v1 import UserControl

@bp.route('/register', methods=['POST'])
def user_register():
    """
    用户注册
    """
    args = request.form

    username = args.get('username', type=str)
    password = args.get('password', type=str)

    if not UserControl._register(username, password):
        make_res(ResponseCode.user_register_fail)

    return make_res(res={"username": username})
