from .area import get_block_bounds
from functools import reduce
import json


def compare_area(parent, child) -> bool:
    """判断行政区b是否在a的管辖范围内

    Args:

        parent(int): 上级行政区编码

        child(int): 下级行政区编码
    
    Example:

        >>> compare_area(330100, 330103)
        ...True
        >>> compare_area(330000, 330103002)
        ...True
        >>> compare_area(330300, 330100)
        ...False

    """
    a_left, a_right = get_block_bounds(parent)
    b_left, b_right = get_block_bounds(child)
    return a_left <= b_left and b_right <= a_right


def in_charge(user, road_code=None, area_code=None):
    """判断指定道路或区域是否在用户user的管辖范围内
    """
    # 避免循环引入
    from panel_app.model import PanelSession
    manage_area = user.us_manage_area
    codes = set(item.get('code') for item in manage_area)
    if area_code is not None:
        _compare_area = lambda code: compare_area(code, area_code)
        return reduce(lambda prev, curr: prev or _compare_area(curr), codes, False)
    
    if road_code is not None:
        session = PanelSession()
        result = session.query(AreaRoad.ar_area_code) .filter(
            AreaRoad.ar_road_code == road_code
        ) .all()
        areas = set(item[0] for item in result)
        return bool(areas & codes)


def in_charge_v3(user, area_code=None):
    """
        判断指定区域 是否在用户user 管辖范围内
    """
    manage_area = user.us_manage_area
    codes = set(item.get('code') for item in manage_area)

    if area_code is not None:
        _compare_area = lambda code: compare_area(code, area_code)
        return reduce(lambda prev, curr: prev or _compare_area(curr), codes, False)
    else:
        return False
