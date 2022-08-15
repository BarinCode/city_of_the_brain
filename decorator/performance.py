import time
from functools import wraps

def performance(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()

        print(f'time cost of function {func.__name__}:  {(end - start) * 1000}ms')

        return res
    
    return wrapper


class Performance(object):

    records = {}

    @staticmethod
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()

            print(f'time cost of function {func.__name__}:  {(end - start) * 1000}ms')

            return res
        
        return wrapper
