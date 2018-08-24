import math
from functools import reduce

from .basic import GeometryEntity
from .exception import filldedent
from .settings import pi


class Point(GeometryEntity):
    """A 2D or 3D point. A n-dimensional point in the future
    """
    def __new__(cls, *args, **kwargs):
        coords = args[0] if len(args) == 1 else args
        if isinstance(coords, Point):
            return coords

        coords = tuple(coords)

        if len(coords) < 2:
            raise ValueError(filldedent('''Point coordinates can't less than 2'''))

        if len(coords) == 2:
            return Point2D(*coords, **kwargs)
        elif len(coords) == 3:
            return Point3D(*coords, **kwargs)

    def __len__(self):
        return len(self.args)

    def __abs__(self):
        """Return the distance between self point and origin(0, 0)"""
        origin = Point(0, 0)
        return self.distance(origin)

    def __add__(self, other):
        """Add two points' coordinates"""
        p1 = Point._convert(self)
        p2 = Point._convert(other)
        coords = [(a + b) for a, b in zip(p1, p2)]
        return Point(coords)

    def __sub__(self, other):
        """subtract two points' coordinates"""
        coords = [(a - b) for a, b in zip(self, other)]
        return Point(coords)

    def __mul__(self, factor):
        """Multiply point's coordinates by a factor."""
        coords = [(x*factor) for x in self.args]
        return Point(coords)

    def __contains__(self, item):
        return item in self.args

    def __eq__(self, other):
        if not isinstance(other, Point) or len(self.args) != len(other.args):
            return False
        return self.args == other.args

    def __neg__(self):
        """Negate the point."""
        ps = [-x for x in self.args]
        return Point(ps)

    def __iter__(self):
        return self.args.__iter__()

    def __getitem__(self, item):
        return self.args[item]

    def __hash__(self):
        return hash(self.args)

    @classmethod
    def _convert(cls, p):
        """Convert other to a Point object"""
        return cls(p) if not issubclass(type(p), cls) else p

    @property
    def length(self):
        return 0.0

    def distance(self, p=(0, 0)):
        """reduce() is a very useful function."""
        p1 = Point._convert(self)
        p2 = Point._convert(p)
        return math.sqrt(reduce(lambda x, y: x + y, ((a-b)**2 for a, b in zip(p1, p2))))

    def dot(self, p):
        """Return dot product of self with p"""
        return reduce(lambda x, y: x + y, ((a * b) for a, b in zip(self, p)))

    def equals(self, p):
        """Return whether self and p are the same point"""
        if not isinstance(p, Point) or len(self) != len(p):
            return False
        return all(a == b for a,b in zip(self, p))

    @property
    def is_zero(self):
        """
        Return whether the point is the origin
        :return: True if every coordinate is zero, False if any coordinate is not zero
        """
        # return self == self.origin
        # the previous statement is slower than the next.
        # because function origin() build a Point object
        return [x for x in self.args] == [0] * len(self)

    @property
    def origin(self):
        return Point([0]*len(self))

    def midpoint(self, p):
        """Return midpoint between self and p"""
        p1 = Point._convert(self)
        p2 = Point._convert(p)
        return Point([(a + b)/2 for a, b in zip(p1, p2)])

    @property
    def orthogonal_direction(self):
        """Returns a non-zero point orthogonal to the line containing `self` and the origin."""
        dim = len(self)
        if self[0] == 0:
            return Point([1] + (dim - 1)*[0])
        if self[1] == 0:
            return Point([0, 1] + (dim - 2)*[0])
        return Point([-self[1], self[0]] + (dim - 2)*[0])

    def taxicab_distance(self, p):
        """Return the Taxicab Distance from self to point p."""
        p1 = Point._convert(self)
        p2 = Point._convert(p)
        return reduce(lambda x, y: x + y, (abs(a - b) for a, b in zip(p1, p2)))

    def project(self, p):
        """Get the mapping point of p1 on the line between p2 and origin"""

        p1 = Point._convert(self)
        p2 = Point._convert(p)
        return p2*(p1.dot(p2) / p2.dot(p2))

    def unit(self):
        """Return the normalized line of the line between self and origin(0, 0)"""
        return Point(x / abs(self) for x in self.args)

    @classmethod
    def are_coplanar(cls, *points):
        """Return True if there exists a plane in which all the points
        lie."""
        raise NotImplementedError()

    def is_concyclic(self, *pts):
        """Return whether `self` and the given sequence of points lie in a circle"""

        raise NotImplementedError()


class Point2D(Point):

    def __new__(cls, *args, **kwargs):
        return GeometryEntity.__new__(cls, *args)

    def cross(self, point):
        """Return cross product of self with another Point"""
        return self.x*point.y - self.y*point.x

    def rotate(self, angle, pt=(0, 0)):
        """Rotate a point counterclockwise about Point ``pt``

        :param angle: arc system
        :return:
        """
        # 未解决：使用 math 浮点数计算，会有小数位的误差
        pt = Point(pt)
        s, c = math.sin(angle), math.cos(angle)
        rotated_pt = self - pt
        x, y = rotated_pt.args
        rotated_pt = Point(round(x * c - y * s, 6), round(x * s + y * c, 6))
        return rotated_pt

    def translate(self, x=0, y=0):
        return Point(self.x + x, self.y + y)

    @property
    def bounds(self):
        return (self.x, self.y, self.x, self.y)

    def is_collinear(self, *args):
        if len(args) == 1:
            return True
        else:
            slope_x = self.x - args[0].x
            slope_y = self.y - args[0].y
            flag = True
            for i in args[1:]:
                # 平行线斜率 叉乘 为零
                if not slope_x * (self.y - i.y) == slope_y * (self.x - i.x):
                    flag = False
                    break
            return flag

    @property
    def x(self):
        return self.args[0]

    @property
    def y(self):
        return self.args[1]

    def scale(self, x=1, y=1):
        return Point(self.x*x, self.y*y)


class Point3D(Point):
    def __new__(cls, *args, **kwargs):
        return GeometryEntity.__new__(cls, *args)

    @property
    def x(self):
        return self.args[0]

    @property
    def y(self):
        return self.args[1]

    @property
    def z(self):
        return self.args[2]

    def scale(self, x=1, y=1, z=1):
        return Point(self.x*x, self.y*y, self.z*z)

    def is_collinear(self, *args):
        # 判断点是否为同一维度，不必要，可以不用
        # for p in args:
        #     if not len(self.args) == len(p.args):
        #         raise ValueError("points are not same dimentional")
        if len(args) == 1:
            return True
        else:
            slope_x = self.x - args[0].x
            slope_y = self.y - args[0].y
            slope_z = self.z - args[0].z
            flag = True
            for i in args[1:]:
                # 平行线斜率 叉乘 为零
                if not slope_x * (self.y - i.y) == slope_y * (self.x - i.x):
                    flag = False
                    break
                elif not slope_x * (self.z - i.z) == slope_z * (self.x - i.x):
                    flag = False
                    break
                elif not slope_y * (self.z - i.z) == slope_z * (self.y - i.y):
                    flag = False
                    break
            return flag
