from flask import request, g, current_app
from functools import wraps

from config import VERSION
from res import make_error, ResponseCode
from model import User, LoginRecord

def token_check(*args, priority=0):
    """
    验证token与用户权限的装饰器
    """
    def make_decorator(func):
        @wraps(func)
        def wrapper(*a, **b):
            token = request.args.get('token', type=str)
            print(token)
            if token is None:
                make_error(ResponseCode.token_illegal)

            login_record: LoginRecord = LoginRecord.query.filter(
                LoginRecord.lo_token == token,
                LoginRecord.lo_status == 1
            ).scalar()
            if login_record is None:
                make_error(ResponseCode.token_illegal)
            
            # 验证用户身份与权限
            user: User = User.query.filter(
                User.usid == login_record.lo_usid
            ).scalar()
            if user is None:
                make_error(ResponseCode.user_not_exist)
            if user.us_status != 1:
                make_error(ResponseCode.user_forbidden)

            # 验证通过后，将user挂载到g上
            if 'user' not in g:
                g.user = user
            current_app.logger.info('token 检测成功')
            return func(*a, **b)
        
        return wrapper
    
    if args and callable(args[0]):
        return make_decorator(args[0])
    else:
        def decorator(func):
            return make_decorator(func)    

        return decorator
