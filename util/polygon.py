import json


def is_close(path):
    """判断path是否闭合
    """
    p1 = path[0]
    p2 = path[-1]
    lng_diff = abs(p1[0] - p2[0])
    lat_diff = abs(p1[1] - p2[1])

    return lng_diff + lat_diff < 1e-6


class Polygon(object):

    def __init__(self, points):
        if not is_close(points):
            points.append(points[0])
        self.points = points
        lngs = list(map(lambda x: x[0], points))
        lats = list(map(lambda x: x[1], points))

        self.maxLng = max(lngs)
        self.minLng = min(lngs)
        self.maxLat = max(lats)
        self.minLat = min(lats)

    def contains(self, point):
        result: bool = False
        lng = point[0]
        lat = point[1]
        if lng > self.maxLng or lng < self.minLat \
                or lat > self.maxLat or lat < self.minLat:
            return False

        count = 0
        for i in range(1, len(self.points)):
            p1 = self.points[i-1]
            p2 = self.points[i]
            isIntersect = self._intersect(point, p1, p2)
            if isIntersect:
                count += 1
        if count % 2 == 1:
            result = True
        return result

    def _intersect(self, p0, p1, p2):
        middleH = (self.maxLng + self.minLng) / 2
        middleL = (self.maxLat + self.minLat) / 2

        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        toward_right = x0 < middleH

        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if middleH == x0:
            middleH += 1e-2
        k0 = (middleL - y0) / (middleH - x0)

        # p1 p2 垂直于x轴
        if x2 == x1:
            if toward_right and x1 < x0:
                return False
            if not toward_right and x1 > x0:
                return False
            Y = k0 * (x1 - x0) + y0
            if y1 > y2:
                y1, y2 = y2, y1

            if y1 <= Y <= y2:
                return True
            else:
                return False

        k1 = (y2 - y1) / (x2 - x1)

        if abs(k0) == abs(k1):
            return False

        X = (k0 * x0 - k1 * x1 + y1 - y0) / (k0 - k1)
        if toward_right and X < x0:
            return False
        if not toward_right and X > x0:
            return False
        if x1 <= X and X <= x2:
            return True

        return False


def inside_boundary(point, boundary):
    if isinstance(boundary, str):
        boundary = json.loads(boundary)
    
    if not boundary:
        return False
    if isinstance(boundary[0][0], float):
        boundary = [boundary]
    
    for path in boundary:
        polygon = Polygon(path)
        if polygon.contains(point):
            return True
    
    return False
