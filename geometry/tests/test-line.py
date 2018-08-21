from geometry.point import Point
from geometry.line import Line, Ray, Segment, Line2D
import sympy.geometry.point
import sympy.geometry.line
import time

t0 = time.clock()

p1_my = Point(1, 0)
p2_my = Point(0, 1)
p3_my = Point(1, 1)
p4_my = Point(10, 1)
p5_my = Point(1, 0)
p6_my = Point(10, 0)

# p7_my = Point(2, -2)
# print(p7_my)



# --------------test line -----------------#
l1 = Line2D(p1_my, p2_my)
l2 = Line(p3_my, p4_my)
l3 = Line(p5_my, p6_my)

# print(l3)
# print(l2)
# print(l1.args)
# print(l1.direction)
# print(l1.angle_between(l2))
# print(l1.is_parallel(l2))
# print(l3.is_parallel(l2))
# print(l3.is_parallel(l3))
# print(l3.unit)
# print(l3.parallel_line(p3_my))
# print(l1.perpendicular_line(p3_my))
# print(l1.perpendicular_segment(p3_my))
# print(l1.projection(p3_my))
# print(l1.projection((1, 1)))
# print(l1.contains((2, -1)))
# print(l2.length)
# print(l1.slope)
# print(l1.is_vertical)
# print(l1.is_horizontal)
# print(l3.is_vertical)
# print(l3.is_horizontal)
# print(l1.coefficients)
# print(l1.equation())
# print(l1.intersection(l2))
# print(l1.intersection(l2).y)


# -----------------Line End-----------------------#

# ----------------- Segment -------------- #
s1 = Segment(p1_my, p2_my)
s2 = Segment(p3_my, p4_my)
# s3 = Segment(p5_my, p6_my)

# print(type(s1))
# print(s1.length)
# print(p3_my in s1)
# print(s1.equals(s2))
# print(s1.equals(s1))
# print(s1.distance(p1_my))
# print(s1.distance(p3_my))
# print(s1.distance(p4_my))
# print(s1.distance(p6_my))
# print(s1.distance(p7_my))
# print(s1.perpendicular_bisector())
# print(s1.is_parallel(s2))
# print(s1.contains((2, -1)))

# ---------------Segment End --------------#


# ----------------- Ray -------------- #
# r1 = Ray(p1_my, p2_my)
# r2 = Ray(p3_my, p4_my)
# r3 = Ray(p5_my, p6_my)

# print(r1)
# print(r1.perpendicular_line(p7_my))

# ---------------Ray End --------------#

t1 = time.clock()

# print(t1 - t0)

# print(Point.unit(p1_my, p2_my))
# print(p1_my.distance(p2_my))
#
# print(l1.distance(p3_my))
# print(l1.normal.A)
# print(l1.is_horizontal)
# print(l1.is_vertical)




# ---------------Sympy -----------------#

# p1_sym = sympy.geometry.point.Point(1, 0)
# p2_sym = sympy.geometry.point.Point(0, 1)
# p3_sym = sympy.geometry.point.Point(1, 1)
# p4_sym = sympy.geometry.point.Point(10, 0)
#
# l1_sys = sympy.geometry.Line(p1_sym, p2_sym)
# l2_sys = sympy.geometry.Line(p3_sym, p4_sym)
#
# s1_sym = sympy.geometry.line.Segment(p1_sym, p2_sym)
# print(s1_sym.distance(p4_sym))

# print(l1_sys)
# print(l2_sys)
#
# t2 = time.clock()
#
# print(t2 - t1)
#
# print("my time:my_t {0}\nsympy time:sym_t {1}\nratio:sym_t/mt_t {2}"\
#       .format(my_t, sym_t, sym_t/my_t))
