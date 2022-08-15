from math import cos, sin, asin, sqrt, pi


def get_radian(angle):
    """
    角度制转弧度制
    """
    angle = angle % 360
    return angle * 2 * pi / 360


def get_distance(lng1, lat1, lng2, lat2):
    """
    给定两个[地图点位]的位置信息，计算这两个点位之间的真实距离
    """
    lng1, lat1, lng2, lat2 = map(get_radian, [lng1, lat1, lng2, lat2])
    delta_lng = lng2 - lng1
    delta_lat = lat2 - lat1
    tmp = sin(delta_lng / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_lat/2)**2
    S = 2 * asin(sqrt(tmp)) * 6378.137

    return S * 1000


def get_mileage(path) -> float:
    """
    给定一条[路径]或若干条[路径]，计算其总长度
    """
    mileage = 0

    if isinstance(path[0][0], float):
        path = [path]

    for side in path:
        for i in range(1, len(side)):
            lng1, lat1, *_ = side[i-1]
            lng2, lat2, *_ = side[i]
            mileage += get_distance(lng1, lat1, lng2, lat2)

    return int(mileage)
