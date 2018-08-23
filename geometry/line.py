import math

from .settings import pi, PI_HALF, nearly_eq
from .point import Point
from .basic import GeometryEntity


class LinearEntity(GeometryEntity):
    def __new__(cls, p1, p2=None, **kwargs):

        if p1 == p2:
            raise ValueError(
                "%s.__new__ requires two unique Points." % cls.__name__)
        if len(p1) != len(p2):
            raise ValueError(
                "%s.__new__ requires two Points of equal dimension." % cls.__name__)

        return GeometryEntity.__new__(cls, p1, p2, **kwargs)

    def __len__(self):
        """
        Treat a line as a two item container with length '2'.
        :return: 2
        """
        return 2

    def __contains__(self, other):
        """Return a definitive answer or else raise an error if it cannot
        be determined that other is on the boundaries of self."""
        result = self.contains(other)

        if result is not None:
            return result
        else:
            return ("can't decide whether '%s' contains '%s'" % (self, other))

    def __eq__(self, other):
        result = self.equals(other)

        if result is not None:
            return result
        return ("can't decide whether '%s' equals '%s'" % (self, other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.args)

    def contains(self, other):
        raise NotImplementedError()

    def _span_test(self, other):
        """Test whether the point `other` lies in the positive span of `self`."""
        if self.p1 == other:
            return 0

        rel_pos = other - self.p1
        d = self.direction
        if d.dot(rel_pos) > 0:
            return 1
        return -1

    @property
    def ambient_dimention(self):
        """Return the dimention of self line"""
        return len(self.p1)

    def angle_between(self, line):
        """
        get the angle between 'self' and 'line' in radians
        :param line: Line
        :return: angle in radians
        """
        a = self.direction
        b = line.direction
        return math.acos(a.dot(b)/(abs(a)*abs(b)))

    def smallest_angle_between(self, line):
        """Return the smallest angle between two lines.
            if angle > pi/2, return angle = angle - pi/2
        """
        angle = self.angle_between(line)
        if angle > PI_HALF:
            return angle - PI_HALF
        else:
            return angle

    def is_parallel(self, line):
        """
        whether two linear are parallel
        :param line:  Line
        """
        # 这里的平行包含共线，使用时需注意
        if not isinstance(self, LinearEntity) and not isinstance(line, LinearEntity):
            raise TypeError('Must pass only LinearEntity objects')

        a = self.direction
        b = line.direction

        if isinstance(line, LinearEntity2D):
            return a.cross(b) == 0

        d1 = abs(a) * math.sqrt(b.x**2 + b.y**2)
        d2 = abs(b) * math.sqrt(a.x**2 + a.y**2)
        return d1 == d2

    def is_perpendicular(self, line):
        """
        whether two linear are perpendicular
        :param line:  Line
        """
        if not isinstance(line, LinearEntity) and not isinstance(self, LinearEntity):
            raise TypeError('Must pass only LinearEntity objects')

        return self.direction.dot(line.direction) == 0


    def is_intersection(self, line):
        """Are lines intersect?

        Parameters
        ==========
        other : Point or LinearEntity
        """
        return not self.is_parallel(line)

    def is_similar(self, line):
        """
        Return True if self and other are contained in the same line.
        :param line: Line
        :return:
        """
        return line in self

    @property
    def direction(self):
        """Return the direction of line"""
        return self.p2 - self.p1
    
    @property
    def normal_direction(self):
        """Return the normal direction of a line

            The normal direction here is the right hand direction
        """
        d = self.direction
        # to get the left hand direction: return Point(-d.y, d.x)
        return Point(d.y, -d.x)

    @property
    def p1(self):
        """The first point of the line

        :return: Point object
        """
        return self.args[0]

    @property
    def p2(self):
        return self.args[1]

    @property
    def points(self):
        return (self.p1, self.p2)

    @property
    def unit(self):
        """Translates the vector self to the origin and scales the length
        of the vector to 1.
        :return Returns a Point() whose distance from the origin is 1.
        """
        dis = self.direction
        return dis * (1/abs(dis))

    def parallel_line(self, pt):
        """
        Create a new Line parallel to this linear entity which passes
        through the point `p`.
        :param pt:  Point
        :return:
        """
        pt = Point._convert(pt)
        return Line(pt, pt + self.direction)

    def perpendicular_line(self, pt):
        """Create a new line that perpendicular to self
            and through the point pt
        """
        pt = Point._convert(pt)
        return Line(pt, pt + self.normal_direction)

    def perpendicular_segment(self, p):
        """Create a perpendicular line segment from `p` to this line.
            The segment's other point on the line.
        """
        p = Point._convert(p)
        if p in self:
            return ("the point {} on line".format(p))
        p2 = self.projection(p)

        return Segment(p, p2)

    def projection(self, other):
        """Project a point, line, ray, or segment onto this linear entity.

        :param other: point, line, ray, segment
        :return:  projection : Point or LinearEntity (Line, Ray, Segment)
        """
        other = Point._convert(other)
            # caution : project is not from (0, 0), so must add self.p1.
        return (other - self.p1).project(self.direction) + self.p1

    def are_concurrent(self, *lines):
        """Are two or more linear entities are concurrent?

        Concurrent means lines all intersect at a single point.
        """
        raise NotImplementedError()

    # def intersection(self, other):
    #     # 以后需要补充，将所有的相交行为都移植到该函数下，使得3D也可用
    #     def intersect_parallel_segments(seg1, seg2):
    #         if seg1.contains(seg2):
    #             return [seg2]
    #         if seg2.contains(seg1):
    #             return [seg1]
    #
    #         # direct the segments so they're oriented the same way
    #         if seg1.direction.dot(seg2.direction) < 0:
    #             seg2 = Segment(seg2.p2, seg2.p1)
    #         # order the segments so seg1 is "behind" seg2
    #         if seg1._span_test(seg2.p1) < 0:
    #             seg1, seg2 = seg2, seg1
    #         if seg2._span_test(seg1.p2) < 0:
    #             return []
    #         return [Segment(seg2.p1, seg1.p2)]
    #
    #     if not isinstance(other, GeometryEntity):
    #         other = Point._convert(other)
    #         if self.contains(other):
    #             return [other]
    #         else:
    #             return []
    #     elif isinstance(other, LinearEntity):
    #         if self.p1.is_collinear(self.p2, other.p1, other.p2):
    #             if isinstance(other, Line):
    #                 return [self]
    #             if isinstance(self, Line):
    #                 return [other]
    #             if isinstance(other, Segment) and isinstance(self, Segment):
    #                 return intersect_parallel_segments(self, other)
    #         else:
    #             if self.is_parallel(other):
    #                 return []



class Line(LinearEntity):
    """A 2D or 3D Line. A n-dimensional line in the future
    """
    def __new__(cls, p1, p2=None, **kwargs):
        if isinstance(p1, LinearEntity):
            if p2:
                raise ValueError(r"p1 is a Linear Entity, can't have p2")
            dim = len(p1.p1)
        else:
            p1, p2 = Point._convert(p1), Point._convert(p2)
            dim = len(p1)

        if dim == 2:
            return Line2D(p1, p2, **kwargs)
        elif dim == 3:
            return Line3D(p1, p2, **kwargs)
        return LinearEntity.__new__(cls, p1, p2, **kwargs)

    def contains(self, item):
        if not isinstance(item, GeometryEntity):
            item = Point._convert(item)
        if isinstance(item, Point):
            return self.p1.is_collinear(item, self.p2)
        if isinstance(item, Line):
            if not self.p1.is_collinear(item.p1, item.p2):
                return False
            return self.p2.is_collinear(item.p1, item.p2)

    @property
    def length(self):
        return ("A line doesn't have length.")

    def equals(self, other):
        """Return whether two lines are collinear"""
        if not isinstance(other, Line):
            return False
        return self.p1.is_collinear(self.p2, other.p1, other.p2)

    def distance(self, p):
        """
        Distance between a line and a point
        :param p: Point-(0, 1)
        :return:
        """
        p = Point._convert(p)

        if self.contains(p):
            return 0.0
        d = self.direction
        A_point = p - self.p1
        n = d.cross(A_point) / self.p1.distance(self.p2)
        return abs(n)


class LinearEntity2D(Line):

    @property
    def bounds(self):
        """Return a tuple (xmin, ymin, xmax, ymax) representing the bounding
        rectangle for the geometric figure.
        """
        verts = self.args
        xs = [p.x for p in verts]
        ys = [p.y for p in verts]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def slope(self):
        """
        Get the slope of a line. if the line is vertical, return "line is vertical"
        :return: float. slope of a line
        """
        d_x, d_y = self.direction.args
        if d_x == 0:
            return ("line is vertical!", self.is_vertical)
        return d_y/d_x

    @property
    def normal(self):
        """
        Get the normal line of self(a line)
        :return: the normal line of a line
        """
        d = self.direction
        return Line([-d.y, d.x], [d.y, -d.x])

    @property
    def is_vertical(self):
        """
        Determine whether the line is vertical.
        :return: True or False
        """
        return self.p1.x == self.p2.x

    @property
    def is_horizontal(self):
        """
        Determine whether the line is parallel.
        :return: True or False
        """
        return self.p1.y == self.p2.y


class Line2D(LinearEntity2D, Line):
    def __new__(cls, p1, p2=None, **kwargs):
        """No need to judge p1, p2. Then have been judged in class LinearEntity
        No judgement will accelerate several even 10 times!!!
        """

        return LinearEntity.__new__(cls, p1, p2, **kwargs)

    @property
    def coefficients(self):
        """The coefficients (`a`, `b`, `c`) for a standard linear equation `ax + by + c = 0`."""
        p1, p2 = self.args
        p1_x, p1_y = p1.args
        p2_x, p2_y = p2.args
        if p1_x == p2_x:
            return (1, 0, -p1_x)
        elif p1_y == p2_y:
            return (0, 1, -p1_y)
        return (p1_y - p2_y, p2_x - p1_x, p1_x*p2_y - p1_y*p2_x)

    def equation(self, x='x', y='y'):
        """Return the equation of 'ax + by +c'

        :return: equation that data type is string.
        """
        # I think this function is useless.
        # The function coefficients() is enough
        # But I written it to keep consistent with sympy
        a, b, c = self.coefficients
        if b < 0 & c < 0:
            return ("{0} {1} {2}".
                    format(str(a) + x, str(b) + y, str(c)))
        elif b < 0:
            return ("{0} {1} + {2}".
                    format(str(a) + x, str(b) + y, str(c)))
        elif c < 0:
            return ("{0} + {1} {2}".
                    format(str(a) + x, str(b) + y, str(c)))
        return ("{0} + {1} + {2}".
                format(str(a) + x, str(b) + y, str(c)))

    def intersection(self, line):
        """
        Get intersection point of two line
        :param line:
        :return: Point. intersection point
        """
        if not isinstance(line, LinearEntity2D):
            raise ValueError("{} is not a Line object".format(line))

        a1, b1, c1 = self.coefficients
        a2, b2, c2 = line.coefficients

        # Here nearly_eq() function can be used to get higher precision
        d = a1*b2 - a2*b1
        if d == 0:
            return ("These two lines are parallel or coincident")
        return Point((b1*c2 - b2*c1)/d, (a2*c1 - a1*c2)/d)


class Segment(LinearEntity):
    def __new__(cls, p1, p2=None, **kwargs):
        if isinstance(p1, LinearEntity):
            if p2:
                raise ValueError(r"p1 is a Linear Entity, can't have p2")
            dim = len(p1.p1)
        else:
            p1, p2 = Point._convert(p1), Point._convert(p2)
            dim = len(p1)

        if dim == 2:
            return Segment2D(p1, p2, **kwargs)
        elif dim == 3:
            return Segment3D(p1, p2, **kwargs)
        return LinearEntity.__new__(cls, p1, p2, **kwargs)

    def contains(self, item):
        if not isinstance(item, GeometryEntity):
            item = Point._convert(item)
        if isinstance(item, Point):
            if self.p1.is_collinear(item, self.p2):
                d = self.direction
                d1, d2 = self.p1 - item, self.p2 - item
                return (abs(d) - abs(d1) - abs(d2)) == 0

        if isinstance(item, Segment):
            return item.p1 in self and item.p2 in self

        return False

    def equals(self, other):
        if not isinstance(other, Segment):
            raise ValueError("{} is not a segment".format(other))

        sp1, sp2, op1, op2 = self.p1, self.p2, other.p1, other.p2

        if op1 == sp1 and op2 == op2:
            return True
        if op1 == sp2 and op2 == sp1:
            return True
        return False

    @property
    def length(self):
        return self.p1.distance(self.p2)

    @property
    def midpoint(self):
        return self.p1.midpoint(self.p2)

    def distance(self, p):
        """Return the shortest distance from a point to a segment"""
        p = Point._convert(p)
        d = self.direction
        op1, op2 = self.p1 - p, self.p2 - p
        sign1, sign2 = op1.dot(d), op2.dot(d)

        if sign1 >= 0 and sign2 > 0:
            return abs(op1)
        if sign1 < 0:
            if sign2 <= 0:
                return abs(op2)
            else:
                return Line(self.p1, self.p2).distance(p)

        return ("Can't get distace")

    def perpendicular_bisector(self):
        """The perpendicular bisector of this segment."""
        return self.perpendicular_line(self.midpoint)


class Segment2D(Segment, LinearEntity2D):
    def __new__(cls, p1, p2, **kwargs):

        p1 = Point._convert(p1)
        p2 = Point._convert(p2)

        if p1 == p2:
            return p1

        return LinearEntity.__new__(cls, p1, p2, **kwargs)

    def intersection(self, other):
        def intersect_parallel_segments(seg1, seg2):
            if seg1.contains(seg2):
                return [seg2]
            if seg2.contains(seg1):
                return [seg1]

        if not isinstance(other, LinearEntity2D):
            raise ValueError("{} isn't segment2D".format(other))

        if self.p1.is_collinear(self.p2, other.p1, other.p2):
            return intersect_parallel_segments(self, other)
        elif self.is_parallel(other):
                return []
        else:
            l1 = Line(self.p1, self.p2)
            l2 = Line(other.p1, other.p2)
            p = l1.intersection(l2)
            if p in self and p in other:
                return [p]
            return []


class Ray(LinearEntity):
    def __new__(cls, p1, p2=None, **kwargs):
        if isinstance(p1, LinearEntity):
            if p2:
                raise ValueError(r"p1 is a Linear Entity, can't have p2")
            dim = len(p1.p1)
        else:
            p1, p2 = Point._convert(p1), Point._convert(p2)
            dim = len(p1)

        if dim == 2:
            return Ray2D(p1, p2, **kwargs)
        elif dim == 3:
            return Ray3D(p1, p2, **kwargs)
        return LinearEntity.__new__(cls, p1, p2, **kwargs)

    @property
    def source(self):
        return self.p1

    def equals(self, other):
        if not isinstance(other, Ray):
            return False
        return self.source == other.source and other.p2 in self

    def contains(self, other):
        if not isinstance(other, GeometryEntity):
            other = Point._convert(other)
        if isinstance(other, Point):
            if self.p1.is_collinear(self.p2, other):
                return self.direction.dot(other - self.p1) >= 0
            return False
        if isinstance(other, Ray):
            if self.p1.is_collinear(self.p2, other.p1, other.p2):
                return self.direction.dot(other.direction) > 0
            return False
        if isinstance(other, Segment):
            return other.p1 in self and other.p2 in self


class Ray2D(Ray, LinearEntity2D):
    def __new__(cls, p1, p2, **kwargs):

        return LinearEntity.__new__(cls, p1, p2, **kwargs)


class Line3D(Line):
    def __new__(cls, p1, p2, **kwargs):

        return LinearEntity.__new__(cls, p1, p2, **kwargs)


class Ray3D(Ray):
    def __new__(cls, p1, p2, **kwargs):

        return LinearEntity.__new__(cls, p1, p2, **kwargs)


class Segment3D(Segment):
    def __new__(cls, p1, p2, **kwargs):

        return LinearEntity.__new__(cls, p1, p2, **kwargs)


