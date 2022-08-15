import random


def generate_random_code(length):
    '''
    随机生成字符串从字母和数字列表，随机选取`length`个字符
    '''
    if not isinstance(length, int):
        length = 32

    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))

    while len(code_list) < length:
        code_list *= 2

    myslice = random.sample(code_list, length)
    random_code = ''.join(myslice)
    return random_code