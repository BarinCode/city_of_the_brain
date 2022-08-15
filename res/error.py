from enum import Enum


class ResponseError(Exception):
    """
    自定义状态异常
    """
    code: int
    message: str

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def as_dict(self):
        return {'status': self.code, 'message': self.message}


class ResponseCode(Enum):
    normal = 10000

    login_fail = 20100
    user_logined =20101
    user_not_exist = 20101
    user_forbidden = 20102
    user_existed = 20103
    user_password = 20104
    user_register_fail = 20105

    data_update_fail = 30100
    url_error = 20200
    request_frequently = 20201
    request_timeout = 20202
    token_expired = 20203
    token_illegal = 20204
    ip_illegal = 20205
    parameter_not_illegal = 20206
    unauthorized = 20207
    overcommitted = 20208
    paramter_missing = 20209
    parameter_illegal = 20210
    paramter_error = 20211

    resource_unavailable = 20300
    resource_not_found = 20301
    resource_unavailable_temporarily = 20302
    file_ovsersize = 20303
    file_too_small = 20304
    file_wrong_format = 20305
    resource_existed = 20306

    server_error = 20500
    server_busy = 20501
    server_updating = 20502
    server_not_accessible = 20503




error_massage = {
    20000: 'Undefined error',
    20100: 'Login failed',
    20101: 'User not existed',
    20102: 'User forbidden',  # the user is already being forbidden
    20103: 'User is existed',  # add xo

    20200: 'Request URL error',
    20201: 'Request too frequently',
    20202: 'Request timeout',
    20203: 'Token expired',
    20204: 'Token illegal',
    20205: 'IP illegal',
    20206: 'Request parameter not legal',  # the request region is not legal in system
    20207: 'Request unauthorized',
    20208: 'Reqeust overcommitted',  # the count of request is over the limit
    20209: 'Required parameter missing',
    20210: 'Required parameter format illegal',
    20211: 'Required parameter error',

    20300: 'Resource unavailable',  # the resource is not able to access
    20301: 'Resource not found',
    20302: 'Resource unavailable temporarily',
    20303: 'Uploading file is oversize',
    20304: 'Uploading file is too small',
    20305: 'Wrong format',
    20306: 'resource_existed',

    20500: 'Internal server error',
    20501: 'Server busy',
    20502: 'Server updating',
    20503: 'Server not accessible temporarily'
}


def make_error(code: ResponseCode):
    """用以raise对应编码的响应错误
    """
    message = error_massage.get(code.value, '')
    raise ResponseError(code.value, message)
