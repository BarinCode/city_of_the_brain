def lon_lat_to_int(lon, lat):
    """
    lon 和 lat 转int
    :param lon:
    :param lat:
    :return:
    """
    if lon and lat:
        return int(lon * (10 ** 6)), int(lat * (10 ** 6)), get_key(lon, lat)
    
    return 0, 0, 0


def lon_lat_to_dou(lon, lat):
    """
    lon 和 lat 转double
    """
    if lon and lat:
        return lon / (10 ** 6), lat / (10 ** 6)
    
    return 0, 0


def get_key(lon, lat):
    """
    通过longitude和latitude获取key

    对应为decode_key
    :param lon:
    :param lat:
    :return:
    """
    int_lon = int(lon * 1e6) + 25 if isinstance(lon, float) else lon
    int_lat = int(lat * 1e6) + 25 if isinstance(lat, float) else lat

    res_lon = int_lon % 100
    res_lat = int_lat % 100

    if res_lon >= 50:
        int_lon = (int_lon - res_lon + 50) // 10
    else:
        int_lon = (int_lon - res_lon) // 10

    if res_lat >= 50:
        int_lat = (int_lat - res_lat + 50) // 10
    else:
        int_lat = (int_lat - res_lat) // 10

    key = int_lon * (10 ** 9) + int_lat * 10 + 1

    return key


def decode_key(key):
    lon = key // (10 ** 9)
    lat = (key % (10 ** 9)) // 10
    return lon, lat
