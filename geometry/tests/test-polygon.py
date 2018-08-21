from geometry.polygon import Polygon
from geometry.point import Point

import sympy.geometry.point
import sympy.geometry.polygon

import time
start_time = time.clock()

p1_my = Point(1, 0)
p2_my = Point(0, 1)
p3_my = Point(2, 1)
p4_my = Point(2, 0)
p5_my = Point(1, 0)
p6_my = Point(10, 0)

poly1 = Polygon(p1_my, p2_my, p3_my, p4_my)
poly2 = Polygon(p1_my, p2_my, p3_my, p6_my)

# print(poly1)
# print(poly1.area)
# print(poly1.vertices)
# print(poly1.bounds)
# print(poly1.angles)
# print(poly1.perimeter)
# print(poly1 == poly2)
# print(poly1.encloses_point(p4_my))
print(poly1.encloses_point((6, 7)))
# print(p4_my in poly1)
# print(Polygon._isright(p1_my, p2_my, p3_my))
# print(Polygon._isright(p2_my, p3_my, p1_my))
# print(Polygon._isright(p3_my, p1_my, p2_my))
# print(Polygon._isright(p2_my, p1_my, p3_my))

end_time = time.clock()

# print(end_time - start_time)



# -------------sympy-------------------#
p1_sym = Point(1, 0)
p2_sym = Point(0, 1)
p3_sym = Point(1, 1)
p4_sym = Point(2, 0)
p5_sym = Point(1, 0)
p6_sym = Point(10, 0)


poly1_sym = sympy.geometry.polygon.Polygon(p1_sym, p2_sym, p3_sym, p4_sym)

# print(poly1_sym.area)


# ------------------------------------#