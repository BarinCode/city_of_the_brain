from .random_code import generate_random_code


def get_salt(num=32):
    """
    token 令牌信息
    """
    return generate_random_code(num)