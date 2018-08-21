from geometry.point import Point
import sympy.geometry.point
import time

p1_my = Point(1, 2)
p2_my = Point([1, 3])
# p3_my = Point(x=1, y=2)
p4_my = Point(0, 0)
p5_my = Point(1, 2, 3)
p6_my = Point(1, 2, 4)
p7_my = Point(1, 3, 5)
p1_sym = sympy.geometry.point.Point(1, 2)

start_time = time.clock()

# ----- 测试点 pass------------ #

# print(p1_my)
# print(p5_my)
# print(p3_my.args)
# print(p3_my.x)
# print(p3_my == p1_my)
# print(p3_my + p1_my)
# print(p3_my - p1_my)
# print(p1_my.distance(p2_my))
# print(p1_my.dot(p2_my))
# print(p4_my.is_zero, p1_my.is_zero)
# print(p1_my.unit)
# print(p1_my.rotate(180))
# print(p2_my.project(p1_my))
# print(p1_my.cross(p2_my))
# print(p2_my.dot(p1_my))
print(p5_my.is_collinear(p6_my, p7_my))

end_time1 = time.clock()

# ------------------------------#

# -----------sympy 对比-------- #

# print(p1_my.unit)
# print(p1_sym.rotate(90))

# end_time2 = time.clock()
# ----------------------------- #
# print(end_time1 - start_time)
# print(end_time2 - end_time1)

