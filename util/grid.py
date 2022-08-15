from math import ceil, cos, sin, sqrt, asin, pi
import panel_app
import os
import json

base_dir = panel_app.__path__[0]

with open(os.path.join(base_dir, 'city.json')) as f:
    GRID_ANCHOR = json.load(f)

def get_radian(angle):
    """
    角度制转弧度制
    """
    angle = angle % 360
    return angle * 2 * pi / 360

def sphere_to_cartesian(lng, lat):
    """球坐标转直角坐标，球的半径为地球半径

    Args:
        lng(float): 经度，例如120.021
        lat(float): 维度，例如30.029
    
    Returns:
        x, y, z: 直角坐标
    """
    r = 6378.137 * 1000

    lng = get_radian(lng)
    lat = get_radian(lat)

    x = r * cos(lat) * cos(lng)
    y = r * cos(lat) * sin(lng)
    z = r * sin(lat)
    return x, y, z

def distance(p1, p2):
    """计算两个经纬度坐标点之间的最短距离

    Args:
        p1(list): 经纬度构成的列表，[lng, lat]
        p2(list): 经纬度构成的列表，[lng, lat]
    
    Returns:
        d(float): 距离，以米为单位
    """
    lng1, lat1 = p1
    lng2, lat2 = p2
    r = 6378.137 * 1000

    x1, y1, z1 = sphere_to_cartesian(lng1, lat1)
    x2, y2, z2 = sphere_to_cartesian(lng2, lat2)

    d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    theta = asin(d / 2 / r)
    d = 2 * theta * r

    return d

class GridKey:

    @staticmethod
    def grid_key(lng, lat, city_code):
        """将给定坐标的经纬度转为网格点key

        Args:
            lng(float): 经度
            lat(float): 纬度
            city_code(int): 坐标点所属城市的区域编码，例如杭州市：330100
        
        Returns:
            key(str): key值
        """
        city_code = f'{city_code}'
        if city_code not in GRID_ANCHOR:
            raise KeyError(f'city code {city_code} not found in anchor map')
        min_lng, min_lat = GRID_ANCHOR.get(city_code).get('bottom_left')
        y = ceil(distance([min_lng, lat], [min_lng, min_lat]) // 3)

        theta = get_radian(lng - min_lng)
        phi = get_radian(lat)
        x = 6378.137 * 1000 * theta * cos(phi)
        x = ceil(x // 3)

        return x, y

    @staticmethod
    def grid_to_lnglat(x, y, city_code):
        city_code = f'{city_code}'
        if city_code not in GRID_ANCHOR:
            raise KeyError(f'city code {city_code} not found in anchor map')
        min_lng, min_lat = GRID_ANCHOR.get(city_code).get('bottom_left')
        x *= 3
        y *= 3
        r = 6378.137 * 1000
        # lat = y / r
        # lng = 1 - 2 * sin(x / 2 / r)**2 / cos(lat)**2
        # lng = acos(lng)

        lat = (y / r + min_lat / 180 * pi)
        lng = x / (r * cos(lat))

        return lng * 180 / pi + min_lng, lat * 180 / pi
