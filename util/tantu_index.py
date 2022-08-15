from typing import Dict, List
from math import sqrt, exp


def default_stat():
    return {
        idx: 0
        for idx in range(4)
    }


class TantuIndex(object):
    """计算坦途指数
    """
    
    @staticmethod
    def gaussian(sigma, minimum, x):
        """高斯分布

        Args:
            sigma (float): 高斯分布标准差
            minimum (int): 坦途指数最低分
            x (float): x

        Returns:
            score: 坦途指数
        """
        rv = exp(-1 * x**2 / 2 / sigma**2) * (100 - minimum) + minimum
        return int(rv)
    
    @staticmethod
    def count_levels(data: Dict[int, int]):
        nums = [0, 0, 0, 0]
        for level, num in data.items():
            if level < 0 or level > 3:
                continue
            nums[level] = num
        return nums
    
    @staticmethod
    def normalize(nums):
        """归一化处理
        """
        min_val = min(nums)
        max_val = max(nums)
        diff = (max_val - min_val) or 1
        nums = [(n - min_val) / diff for n in nums]
        # 由于不同病害、道路、区域的病害数量相差极大，因此计算坦途指数前先做归一化处理
        return TantuIndex.normalize(nums)
    
    @staticmethod
    def index(data: Dict[int, int], params: List[int]=None):
        """给定不同等级下病害数量时，计算对应坦途指数

        Args:
            data(Dict[int, int]): 字典结构的统计数据，key为病害等级level，value为对应等级下病害数量

            params(List[int]): 不同等级影响坦途指数的权重，数量与病害等级数量相同，目前所有
                类型下参数个数均为4, 一般情况下等级越高，占比越高

        Returns:
            score(int): 坦途指数得分
        """
        if params is None:
            params = [0, 0.1, 0.2, 0.3]
        nums = TantuIndex.count_levels(data)
        sigma = 4
        minimum = 54
        x = sum(params[i] * nums[i] for i in range(4))
        return TantuIndex.gaussian(sigma, minimum, x)
