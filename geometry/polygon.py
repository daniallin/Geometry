import math
from functools import reduce

from .settings import pi
from .point import Point
from .line import Line, Ray, Segment
from .basic import GeometryEntity


class Polygon(GeometryEntity):

    def __new__(cls, *args, **kwargs):
        vertices = [Point._convert(a) for a in args]

        # remove same points
        nsp = []
        for p in vertices:
            if nsp and p == nsp[-1]:
                continue
            nsp.append(p)

        if len(nsp) > 1 and nsp[0] == nsp[-1]:
            nsp.pop()

        # remove collinear points
        i = -3
        while i < len(nsp) - 3 and len(nsp) > 2:
            a, b, c = nsp[i], nsp[i + 1], nsp[i + 2]
            if a.is_collinear(b, c):
                nsp[i] = a
                nsp[i + 1] = None
                nsp.pop(i + 1)
            i += 1

        vertices = list(nsp)

        if len(vertices) > 3:
            return GeometryEntity.__new__(cls, *vertices, **kwargs)
        elif len(vertices) == 3:
            return Triangle(*vertices, **kwargs)
        elif len(vertices) == 2:
            return Segment(*vertices, **kwargs)
        else:
            return Point(*vertices, **kwargs)

    def __hash__(self):
        return super(Polygon, self).__hash__()

    def __eq__(self, other):
        if not isinstance(other, Polygon) or len(self.args) != len(other.args):
            return False

        args = self.args
        oargs = other.args
        n = len(args)
        o0 = oargs[0]
        for i0 in range(n):
            if args[i0] == o0:
                if all(args[(i0 + i) % n] == oargs[i] for i in range(1, n)):
                    return True
                if all(args[(i0 - i) % n] == oargs[i] for i in range(1, n)):
                    return True
        return False

    def __contains__(self, o):
        """
        Return True if o is contained within the boundary lines of self.altitudes

        Para:
        other : GeometryEntity
        """

        if isinstance(o, Polygon):
            return self == o
        elif isinstance(o, Segment):
            return any(o in s for s in self.sides)
        elif isinstance(o, Point):
            if o in self.vertices:
                return True
            for side in self.sides:
                if o in side:
                    return True

        return False

    @staticmethod
    def _isright(a, b, c):
        """Return True/False for cw/ccw orientation."""
        ab = b - a
        ac = c - a
        t_cross = ab.cross(ac)
        return t_cross < 0

    @property
    def vertices(self):
        return list(self.args)

    @property
    def bounds(self):
        verts = self.args
        xs = [p.x for p in verts]
        ys = [p.y for p in verts]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def ambient_dimension(self):
        """Return dimention of polygon"""
        return len(self.vertices[0])

    @property
    def angles(self):
        """The internal angle at each vertex.
            For concave polygon, angle may > pi !"""

        angle = {}
        args = self.args
        # 这里不严谨，如果初始 cw_sign 就取到了多边形的 > 180° 的顶点
        # 那接下来可能会导致其他本身 < 180°的内角变为 >180°
        cw_sign = self._isright(args[-1], args[0], args[1])

        for i in range(len(args)):
            a, b, c = args[i - 2], args[i - 1], args[i]
            agn = Line(b, a).angle_between(Line(b, c))

            # if Point doesn't have __hash__(), it will appear an error
            if cw_sign ^ self._isright(a, b, c):
                angle[b] = (360-agn/pi * 180)
            else:
                angle[b] = agn / pi * 180
        return angle

    @property
    def perimeter(self):
        """The perimeter of polygon"""
        p = 0
        args = self.args
        for i in range(len(args)):
            p += args[i - 1].distance(args[i])
        return p

    @property
    def area(self):
        """The area of polygon"""
        a = 0
        args = self.args
        for i in range(len(args)):
            x1, y1 = args[i-1].args
            x2, y2 = args[i].args
            a += x1*y2 - x2*y1
        return a/2

    @property
    def sides(self):
        """The directed line segments that form the sides of the polygon."""
        s = []
        args = self.args
        for i in range(-len(args), 0):
            s.append(Segment(args[i], args[i + 1]))
        return s

    def is_convex(self):
        """Return whether the polygon is convex"""
        args = self.vertices
        cw_sign = self._isright(args[-2], args[-1], args[0])
        for i in range(1, len(args)):
            if cw_sign ^ self._isright(args[i - 2], args[i - 1], args[i]):
                return False
        # sides intersecting check
        sides = self.sides
        for i, si in enumerate(sides):
            pts = si.args
            # exclude the sides connected to si
            for j in range(1 if i == len(sides) - 1 else 0, i - 1):
                sj = sides[j]
                if sj.p1 not in pts and sj.p2 not in pts:
                    hit = si.intersection(sj)
                    if hit:
                        return False

        return True

    def encloses_point(self, p):
        """Return whether the point p is enclosed by self"""
        p = Point._convert(p)
        if any(p in s for s in self.sides):
            return False
        # Still need to complement !!!

        return True

    def distance(self, other):
        """
        Returns the shortest distance between self and o.
        """
        raise NotImplementedError()

    def intersection(self, other):
        """the intersection of polygon and other geometry entity"""
        intersection_result = []
        k = other.sides if isinstance(other, Polygon) else [other]
        for side in self.sides:
            for side1 in k:
                intersection_result.extend(side.intersection(side1))

        intersection_result = list(set(intersection_result))
        points = [entity for entity in intersection_result if isinstance(entity, Point)]
        segments = [entity for entity in intersection_result if isinstance(entity, Segment)]

        if points and segments:
            points_in_segments = list(set([point for point in points for segment in segments if point in segment]))
            if points_in_segments:
                for i in points_in_segments:
                    points.remove(i)
            return list(segments + points)
        else:
            return list(intersection_result)

    @property
    def centroid(self):
        """Return the centroid of th polygon"""
        v = self.vertices
        d = reduce(lambda x, y: x+y, ((a.x * a.y) for a in v))
        dx = reduce(lambda x, y: x+y, ((a.x) for a in v))
        dy = reduce(lambda x, y: x+y, ((a.y) for a in v))
        return Point(d/dy, d/dx)

    def second_moment_of_area(self, point=None):
        """Returns the second moment and product moment of area of a two dimensional polygon."""
        raise NotImplementedError()


class RegularPolygon(Polygon):


    @property
    def area(self):
        raise NotImplementedError()

    @property
    def length(self):
        raise NotImplementedError()

    @property
    def center(self):
        raise NotImplementedError()

    @property
    def radius(self):
        """Radius of the RegularPolygon"""
        raise NotImplementedError()

    @property
    def circumcircle(self):
        """The circumcircle of the RegularPolygon."""
        raise NotImplementedError()

    @property
    def incircle(self):
        """The incircle of the RegularPolygon."""
        raise NotImplementedError()

    @property
    def vertices(self):
        raise NotImplementedError()


class Triangle(Polygon):
    def __new__(cls, *args, **kwargs):
        vertices = [Point._convert(a) for a in args]

        # remove same points
        nsp = []
        for p in vertices:
            if nsp and p == nsp[-1]:
                continue
            nsp.append(p)

        if len(nsp) > 1 and nsp[0] == nsp[-1]:
            nsp.pop()

        # remove collinear points
        i = -3
        while i < len(nsp) - 3 and len(nsp) > 2:
            a, b, c = nsp[i], nsp[i + 1], nsp[i + 2]
            if a.is_collinear(b, c):
                nsp[i] = a
                nsp[i + 1] = None
                nsp.pop(i + 1)
            i += 1

        vertices = list(filter(lambda x: x is not None, nsp))

        if len(vertices) == 3:
            return GeometryEntity.__new__(cls, *vertices, **kwargs)
        elif len(vertices) == 2:
            return Segment(*vertices, **kwargs)
        else:
            return Point(*vertices, **kwargs)