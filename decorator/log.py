
# from panel_app.shared import TOKEN_EXPIRE_TIME
# import traceback
# from functools import wraps
# from enum import Enum
# from panel_app.config import APP_DEBUG
# from typing import List
# from flask import request, g, make_response
# from panel_app.res import ResponseError, ResponseCode
# from panel_app.util import now, ip_to_int
# from panel_app.model import Log, PanelSession, User
# import pprint
# import json
#
#
# class LogPart(Enum):
#
#     args = "args"
#     form = "form"
#     res = "res"
#     error = "error"
#
#     def __get__(self, a, b):
#         return self.value
#
#
# def log_wrapper(*args, exclude: List[LogPart] = None, ignore=False):
#     """生成日志记录的装饰器
#
#     Args:
#
#         exclude(List(LogPart)): 禁止记录的部分
#     """
#     if exclude is None:
#         exclude = []
#
#     def make_decorator(func):
#         @wraps(func)
#         def wrapper(*a, **b):
#             res = {}
#             log_info = {
#                 "create": now(),
#             }
#             ip_addr = request.headers.get("X-Forwarded-For")
#             log_info["ip"] = ip_to_int(ip_addr) if ip_addr else 0
#
#             try:
#                 req_args = request.args.deepcopy()
#                 req_form = request.form.deepcopy()
#
#                 log_info["path"] = request.path
#                 log_info["user_name"] = "unknown"
#                 log_info["user_id"] = 0
#                 log_info['req_method'] = request.method.capitalize()
#
#                 if not LogPart.args in exclude:
#                     log_info["req_args"] = json.dumps(req_args)
#                 if not LogPart.form in exclude:
#                     log_info["req_form"] = json.dumps(req_form)
#
#                 res = func(*a, **b)
#
#                 if "user" in g:
#                     user: User = g.user
#                     log_info["user_name"] = user.us_name
#                     log_info["user_id"] = user.usid
#
#             except ResponseError as e:
#                 log_info["error"] = str(e)
#                 res = e.as_dict()
#
#             except LookupError as e:
#                 log_info["error"] = str(e)
#                 traceback.print_stack(e)
#                 res = {
#                     "status": ResponseCode.resource_not_found.value,
#                     "message": "Resource not found"
#                 }
#
#             except Exception as e:
#                 # if APP_DEBUG:
#                 traceback.print_stack(e)
#                 log_info["error"] = str(e)
#                 res = {
#                     "status": ResponseCode.server_error.value,
#                     "message": "Internal server error"
#                 }
#
#             if not LogPart.res in exclude:
#                 log_info["res"] = json.dumps(res)
#
#             if not ignore:
#                 new_log = Log.new(**log_info)
#                 PanelSession.add(new_log)
#                 PanelSession.commit()
#                 PanelSession.remove()
#
#             debug_info = {
#                 "path": log_info.get("path"),
#                 "args": log_info.get("req_args"),
#                 "form": log_info.get("req_form"),
#                 "res": log_info.get("res") if not ignore else []
#             }
#             if APP_DEBUG:
#                 pprint.pprint(debug_info)
#
#             response = make_response(json.dumps(res))
#             response.content_type = 'application/json'
#             return response
#
#         return wrapper
#
#     if args and callable(args[0]):
#         return make_decorator(args[0])
#     else:
#         def decorator(func):
#             return make_decorator(func)
#
#         return decorator
