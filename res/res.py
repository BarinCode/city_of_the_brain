
def make_res(res=None):
    if res is None:
        res = {}
    return {
        'status': 10000,
        'message': 'ok',
        'response': res
    }