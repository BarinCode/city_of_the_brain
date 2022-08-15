# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:51 PM
# @Author  : Barin
# @FileName: user.py
# @Software: PyCharm

from model import User, LoginRecord, PanelSession
from util import validation, md5, get_salt
from res import make_error, ResponseCode


class UserControl:
    """
    用户接口相关逻辑
    """
    @classmethod
    def _login(cls, username: str, password: str):
        """
        用户登入验证处理
        """
        if validation(username, password):
            make_error(ResponseCode.paramter_missing)

        user = User.query.filter(
            User.us_name == username.strip()
        ).first()
        if user is None:
            make_error(ResponseCode.user_not_exist)

        cls._vali_password(password, user.us_salt, user.us_password)
        cls._activate(user)
        token = cls._add_session(user)

        return user, token

    @classmethod
    def _vali_password(cls, password: str, salt: str, old_password: str):
        """
        用户密码的验证
        """
        if old_password != md5(salt, password):
            make_error(ResponseCode.user_password)

    @classmethod
    def _activate(cls, user):
        """
        账号可用性验证
        """
        if user.us_status == 0:
            make_error(ResponseCode.user_forbidden)


    @classmethod
    def _add_session(cls, user):
        """
        保存登入的 sessison 信息
        """
        _temp_dict = {
            "usid": user.usid,
            "token": get_salt()
        }

        login_record = LoginRecord.new(**_temp_dict)
        PanelSession.add(login_record)
        PanelSession.commit()

        return _temp_dict["token"]

    @classmethod
    def _register(cls, username: str, password: str):
        """
        注册
        """
        user = User.query.filter(
            User.us_name == username,
        ).first()

        if user:
            make_error(ResponseCode.user_existed)

        salt = get_salt()
        user = User.new(**{
            "level": 1,
            "name": username,
            "salt": salt,
            "password": md5(salt, password)
        })

        PanelSession.add(user)
        PanelSession.commit()

        return True

    @classmethod
    def _logout(cls, token: str):
        """
        用户退出
        """
        login_record: LoginRecord = LoginRecord.query.filter(
            LoginRecord.lo_token == token,
            LoginRecord.lo_status == 1
        ).scalar()

        if login_record is None:
            make_error(ResponseCode.token_illegal)

        login_record.lo_status = 0
        PanelSession.commit()

