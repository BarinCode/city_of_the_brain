import hashlib


def md5(*args):
    """计算所有参数组合的md5
    """
    s = ''.join(str(arg) for arg in args)
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()
