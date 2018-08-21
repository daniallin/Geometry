"""
constants
Pi is expressed by using  a float number, and the result is getted by using module 'math'
"""
from sys import float_info

pi = 3.141592653589793
PI_HALF = 1.5707963267948966
PI_DOUBLE = 6.283185307179586
SQRT_2 = 1.4142135623730951
SQRT_3 = 1.7320508075688772
Epsilon = float_info.epsilon


def nearly_eq(a, b, max_f=float_info.max, min_f=float_info.min, epsilon=Epsilon):
    """
    判断浮点数相等
    :param a: value a
    :param b: value b
    :param maxf: max number of float, 1.7976931348623157e+308
    :param minf: min number of float, 2.2250738585072014e-308
    :param epsilon: float number greater than zero, 2.220446049250313e-16
    :return:
    implementation based on:
    http://floating-point-gui.de/errors/comparison/
    """
    abs_a = abs(a)
    abs_b = abs(b)
    delta = abs(a - b)

    if a == b:
        return True
    elif (a == 0) or (b == 0) or (delta < min_f):
        return delta < (epsilon * min_f)
    else:
        return (delta / min(abs_a + abs_b, max_f)) < (epsilon * 2)


def nearly_zero(value, min_f=float_info.min, epsilon=Epsilon):
    abs_v = abs(value)

    if value == 0:
        return True
    else:
        return abs_v < (epsilon * min_f)

