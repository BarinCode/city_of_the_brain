from .model import LngLat
from typing import List


def point_in_line(point, line, tolerence=3 * 1e-4):
    """
    判断point是否在允许的误差范围tolerence内，位于线段line上
    """
    assert len(line) == 2, '线段line必须给定2个端点'

    p1, p2 = line

    # p1必须在p2的左边
    if p1.lng > p2.lng:
        p1, p2 = p2, p1

    x1 = p1.lng
    y1 = p1.lat
    x2 = p2.lng
    y2 = p2.lat

    x = point.lng
    y = point.lat

    # 判断(x, y)是否在分别以(x1, y1)、(x2, y2)为圆心，tolerence为半径的圆内
    if (x - x1) ** 2 + (y - y1) ** 2 < tolerence ** 2:
        return True

    if (x - x2) ** 2 + (y - y2) ** 2 < tolerence ** 2:
        return True

    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        return y1 <= y <= y2

    # 线段两端点之间的斜率
    slope = (y1 - y2) / (x1 - x2)

    delta_x = tolerence / (slope ** 2 + 1)
    delta_y = tolerence * slope / (slope ** 2 + 1)

    lx = x1 + delta_x
    ly = y1 - delta_y
    ux = x1 - delta_x
    uy = y1 + delta_y

    # 根据斜率slope，误差范围tolerence获取的 y 所在的上下界
    y_lower = slope * (x - lx) + ly
    y_upper = slope * (x - ux) + uy
    x_lower = x1 - 2 * delta_x
    x_upper = x2 + 2 * delta_x

    x_in_bound = x_lower <= x <= x_upper
    y_in_bound = y_lower <= y <= y_upper

    return x_in_bound and y_in_bound


def point_in_polyline(point: LngLat, polyline: List[LngLat], tolerence=3 * 1e-4):
    """
    判断point是否在给定的误差tolerence范围内，位于折线polyline上
    """
    for i in range(1, len(polyline)):
        line = polyline[i - 1: i + 1]
        if point_in_line(point, line, tolerence):
            return True

    return False

