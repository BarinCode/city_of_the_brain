from panel_app.util.key import lon_lat_to_int
from panel_app.util.tools import gcj02_to_wgs84


class LngLat(object):
    # 经度
    lng: float
    # 纬度
    lat: float

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def __repr__(self):
        return f'<LngLat>(lng={self.lng}, lat={self.lat})'

    def to_list(self):
        return [self.lng, self.lat]
