import os
import pytest
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pybresenham


def test_rotatePoint():
    assert pybresenham.rotatePoint(10, 0, 90) == (0, 10)
    assert pybresenham.rotatePoint(10, 0, 180) == (-10, 0)
    assert pybresenham.rotatePoint(10, 0, 270) == (0, -10)
    assert pybresenham.rotatePoint(10, 0, 360) == (10, 0)

    # TODO add more tests, including with pivot values.


def test_rotatePoints():
    assert list(pybresenham.rotatePoints([(0, 10), (0, 20)], 90)) == [(-10, 0), (-20, 0)]

    # TODO add more tests, including with pivot values.


def test_line():
    assert list(pybresenham.line(0, 0, 5, 5))  == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    assert list(pybresenham.line(0, 0, 5, 15)) == [(0, 0), (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (3, 10), (4, 11), (4, 12), (4, 13), (5, 14), (5, 15)]
    assert list(pybresenham.line(5, 5, 0, 0))  == [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
    assert list(pybresenham.line(5, 15, 0, 0)) == [(5, 15), (5, 14), (4, 13), (4, 12), (4, 11), (3, 10), (3, 9), (3, 8), (2, 7), (2, 6), (2, 5), (1, 4), (1, 3), (1, 2), (0, 1), (0, 0)]
    assert list(pybresenham.line(0, 0, 5, -15)) == [(0, 0), (0, -1), (1, -2), (1, -3), (1, -4), (2, -5), (2, -6), (2, -7), (3, -8), (3, -9), (3, -10), (4, -11), (4, -12), (4, -13), (5, -14), (5, -15)]
    assert list(pybresenham.line(5, -15, 0, 0)) == [(5, -15), (5, -14), (4, -13), (4, -12), (4, -11), (3, -10), (3, -9), (3, -8), (2, -7), (2, -6), (2, -5), (1, -4), (1, -3), (1, -2), (0, -1), (0, 0)]

    # Make sure no duplicate points are in the returned generators.
    for x1, y1, x2, y2 in [(17, 9, 5, -15), (21, 14, 18, -8), (-18, -26, -29, 9), (28, 24, 3, 8), (-15, 4, 22, -3), (9, 3, -9, -30), (-23, -21, -11, 27), (5, 16, 13, -24), (-6, -2, 22, -8), (3, 1, 16, -3)]:
        linePoints = list(pybresenham.line(x1, y1, x2, y2))
        assert len(linePoints) == len(frozenset(linePoints))

    # Test the _skipFirst parameter.
    assert list(pybresenham.line(0, 0, 5, 5, _skipFirst=True))  == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    assert list(pybresenham.line(0, 0, 5, 15, _skipFirst=True)) == [(0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (3, 10), (4, 11), (4, 12), (4, 13), (5, 14), (5, 15)]
    assert list(pybresenham.line(5, 5, 0, 0, _skipFirst=True))  == [(4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
    assert list(pybresenham.line(5, 15, 0, 0, _skipFirst=True)) == [(5, 14), (4, 13), (4, 12), (4, 11), (3, 10), (3, 9), (3, 8), (2, 7), (2, 6), (2, 5), (1, 4), (1, 3), (1, 2), (0, 1), (0, 0)]
    assert list(pybresenham.line(0, 0, 5, -15, _skipFirst=True)) == [(0, -1), (1, -2), (1, -3), (1, -4), (2, -5), (2, -6), (2, -7), (3, -8), (3, -9), (3, -10), (4, -11), (4, -12), (4, -13), (5, -14), (5, -15)]
    assert list(pybresenham.line(5, -15, 0, 0, _skipFirst=True)) == [(5, -14), (4, -13), (4, -12), (4, -11), (3, -10), (3, -9), (3, -8), (2, -7), (2, -6), (2, -5), (1, -4), (1, -3), (1, -2), (0, -1), (0, 0)]

    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.line(0, 0, 5, 5, _skipFirst='invalid'))

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        list(pybresenham.line(0,0,0,0, thickness=2))
    with pytest.raises(NotImplementedError):
        list(pybresenham.line(0,0,0,0,endcap=2))
    with pytest.raises(NotImplementedError):
        list(pybresenham.line(0,0,0,0, viewport=2))

def test_lines():
    assert list(pybresenham.lines([(0, 0), (2, 0), (2, 2)])) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

    # TODO Make sure no duplicate points are in the returned generators.
    result1 = [(1, 0), (2, 0), (2, 1), (2, 2), (1, 1), (0, 0)]
    assert list(pybresenham.lines([(0, 0), (2, 0), (2, 2)], closed=True)) == result1
    assert list(pybresenham.lines([(0, 0), (2, 0), (2, 2)], True)) == result1 # test the positional argument

    result2 = [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (2, 6), (2, 5), (1, 4), (1, 3), (0, 2), (0, 1), (-1, 0), (-1, -1), (-2, -2), (-2, -3), (-3, -4), (-3, -5), (-4, -6), (-4, -7), (-5, -8), (-5, -9), (-4, -8), (-4, -7), (-3, -6), (-3, -5), (-2, -4), (-2, -3), (-1, -2), (-1, -1), (0, 0)]
    assert list(pybresenham.lines([(0, 0), (3, 7), (-5, -9)], closed=True)) == result2
    assert list(pybresenham.lines([(0, 0), (3, 7), (-5, -9)], True)) == result2 # test the positional argument

    # Test invalid points arguments.
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines(42)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([(0, 0)]) # only 1 point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([(0, 0), (10, 10)], closed=True) # only 2 points for a closed set of points
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([]) # zero points
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([42]) # not iterable argument
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([('invalid', 0), (0, 0)]) # not a int/floats at first point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([(0, 'invalid'), (0, 0)]) # not a int/floats at first point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([(0, 0), (0, 0), ('invalid', 0)]) # not a int/floats at last point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.lines([(0, 0), (0, 0), (0, 'invalid')]) # not a int/floats at last point

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        pybresenham.lines([(0,0),(0,0)], thickness=2)
    with pytest.raises(NotImplementedError):
        pybresenham.lines([(0,0),(0,0)],endcap=2)
    with pytest.raises(NotImplementedError):
        pybresenham.lines([(0,0),(0,0)], viewport=2)


def test_polygon():
    # TODO Make sure no duplicate points are in the returned generators.

    # TODO There are slight differences between Python 3.7 and Python 3.6 here:
    #assert list(pybresenham.polygon(10, 10, 9, 5, filled=False)) == [(9, 2), (8, 3), (7, 4), (6, 5), (5, 5), (4, 6), (3, 7), (2, 8), (2, 9), (3, 10), (3, 11), (3, 12), (4, 13), (4, 14), (4, 15), (5, 16), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17), (14, 17), (15, 17), (15, 16), (16, 15), (16, 14), (16, 13), (17, 12), (17, 11), (17, 10), (18, 9), (18, 8), (17, 7), (16, 6), (15, 5), (14, 4), (13, 4), (12, 3), (11, 2), (10, 1)]
    #assert list(pybresenham.polygon(10, 10, 9, 5, filled=True))  == [(16, 6), (14, 17), (6, 9), (11, 11), (10, 17), (17, 7), (7, 12), (14, 4), (13, 4), (12, 12), (16, 9), (13, 17), (3, 7), (8, 5), (5, 8), (10, 8), (6, 7), (5, 5), (11, 5), (10, 7), (7, 6), (6, 10), (12, 6), (15, 11), (13, 7), (12, 17), (18, 9), (8, 15), (4, 10), (9, 14), (5, 11), (10, 13), (9, 3), (9, 16), (7, 5), (14, 15), (12, 11), (15, 14), (13, 10), (3, 12), (8, 12), (4, 15), (9, 9), (5, 14), (10, 14), (6, 13), (11, 15), (16, 13), (7, 8), (15, 16), (6, 16), (11, 16), (12, 8), (14, 8), (15, 13), (17, 8), (13, 13), (3, 11), (8, 9), (4, 12), (9, 4), (10, 3), (16, 7), (6, 14), (11, 10), (7, 15), (14, 5), (16, 10), (12, 13), (17, 11), (13, 16), (8, 6), (10, 9), (9, 7), (11, 4), (10, 4), (6, 11), (5, 17), (12, 7), (11, 9), (15, 10), (14, 6), (13, 6), (15, 7), (4, 11), (9, 13), (8, 3), (5, 10), (4, 6), (10, 10), (9, 2), (5, 7), (11, 3), (7, 4), (14, 12), (12, 4), (17, 12), (7, 17), (15, 9), (13, 9), (8, 13), (4, 8), (2, 8), (9, 8), (5, 13), (10, 15), (11, 14), (16, 14), (6, 17), (7, 11), (12, 9), (14, 9), (15, 12), (13, 12), (3, 10), (8, 10), (4, 13), (9, 11), (8, 16), (6, 15), (12, 3), (11, 13), (7, 14), (14, 10), (16, 11), (12, 14), (17, 10), (13, 15), (3, 9), (8, 7), (9, 6), (6, 5), (11, 7), (10, 5), (6, 8), (5, 16), (14, 16), (11, 8), (10, 16), (7, 13), (14, 7), (13, 5), (16, 8), (15, 6), (9, 12), (8, 4), (5, 9), (4, 7), (10, 11), (6, 6), (5, 6), (11, 2), (10, 6), (7, 7), (14, 13), (12, 5), (7, 16), (15, 8), (13, 8), (12, 16), (18, 8), (15, 5), (8, 14), (4, 9), (2, 9), (9, 15), (5, 12), (10, 12), (9, 17), (16, 15), (7, 10), (14, 14), (12, 10), (15, 15), (13, 11), (8, 11), (4, 14), (9, 10), (5, 15), (10, 1), (8, 17), (6, 12), (11, 12), (7, 9), (15, 17), (14, 11), (12, 15), (11, 17), (16, 12), (17, 9), (13, 14), (3, 8), (8, 8), (9, 5), (11, 6), (10, 2)]
    #assert list(pybresenham.polygon(10,10,4,5,0,2)) == [(9, 7), (8, 7), (7, 7), (6, 8), (5, 8), (4, 9), (3, 9), (4, 10), (4, 11), (5, 12), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 12), (16, 11), (16, 10), (17, 9), (16, 8), (15, 8), (14, 8), (13, 7), (12, 7), (11, 6), (10, 6)]
    #assert list(pybresenham.polygon(10,10,4,5,0,1,2)) == [(10, 3), (9, 4), (9, 5), (8, 6), (8, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (8, 13), (8, 14), (8, 15), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (12, 15), (12, 14), (12, 13), (13, 12), (13, 11), (13, 10), (13, 9), (13, 8), (12, 7), (12, 6), (11, 5), (11, 4), (10, 3), (10, 2)]

    # Test invalid points arguments.
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon('invalid x', 0, 10, 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 'invalid y', 10, 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 'invalid radius', 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 10, 'invalid rotation')
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 10, 0, 'invalid stretchHorizontal')
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 10, 0, 1, 'invalid stretchVertical')

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        pybresenham.polygon(0, 0, 10, 0, thickness=2)
    with pytest.raises(NotImplementedError):
        pybresenham.polygon(0, 0, 10, 0, viewport=2)


def test_circle():
    c1 = list(pybresenham.circle(0, 0, 10))
    assert c1 == [(0, -10), (10, 0), (0, 10), (1, -10), (10, -1), (10, 1), (-1, 10), (-10, -1), (-10, 1), (-1, -10), (1, 10), (2, -10), (10, -2), (10, 2), (-2, 10), (-10, -2), (-10, 2), (-2, -10), (2, 10), (3, -10), (10, -3), (10, 3), (-3, 10), (-10, -3), (-10, 3), (-3, -10), (3, 10), (4, -9), (9, -4), (9, 4), (-4, 9), (-9, -4), (-9, 4), (-4, -9), (4, 9), (5, -9), (9, -5), (9, 5), (-5, 9), (-9, -5), (-9, 5), (-5, -9), (5, 9), (6, -8), (8, -6), (8, 6), (-6, 8), (-8, -6), (-8, 6), (-6, -8), (6, 8), (7, -7), (7, 7), (-7, 7), (-7, -7)]
    assert len(c1) == len(set(c1)) # test for duplicate points

    c2 = list(pybresenham.circle(7, -7, 10))
    assert c2 == [(7, -17), (17, -7), (7, 3), (8, -17), (17, -8), (17, -6), (6, 3), (-3, -8), (-3, -6), (6, -17), (8, 3), (9, -17), (17, -9), (17, -5), (5, 3), (-3, -9), (-3, -5), (5, -17), (9, 3), (10, -17), (17, -10), (17, -4), (4, 3), (-3, -10), (-3, -4), (4, -17), (10, 3), (11, -16), (16, -11), (16, -3), (3, 2), (-2, -11), (-2, -3), (3, -16), (11, 2), (12, -16), (16, -12), (16, -2), (2, 2), (-2, -12), (-2, -2), (2, -16), (12, 2), (13, -15), (15, -13), (15, -1), (1, 1), (-1, -13), (-1, -1), (1, -15), (13, 1), (14, -14), (14, 0), (0, 0), (0, -14)]
    assert len(c2) == len(set(c2)) # test for duplicate points

    c3 = list(pybresenham.circle(-7, 7, 10))
    assert c3 == [(-7, -3), (3, 7), (-7, 17), (-6, -3), (3, 6), (3, 8), (-8, 17), (-17, 6), (-17, 8), (-8, -3), (-6, 17), (-5, -3), (3, 5), (3, 9), (-9, 17), (-17, 5), (-17, 9), (-9, -3), (-5, 17), (-4, -3), (3, 4), (3, 10), (-10, 17), (-17, 4), (-17, 10), (-10, -3), (-4, 17), (-3, -2), (2, 3), (2, 11), (-11, 16), (-16, 3), (-16, 11), (-11, -2), (-3, 16), (-2, -2), (2, 2), (2, 12), (-12, 16), (-16, 2), (-16, 12), (-12, -2), (-2, 16), (-1, -1), (1, 1), (1, 13), (-13, 15), (-15, 1), (-15, 13), (-13, -1), (-1, 15), (0, 0), (0, 14), (-14, 14), (-14, 0)]
    assert len(c3) == len(set(c3)) # test for duplicate points

    c4 = list(pybresenham.circle(-77, 77, 13))
    assert c4 == [(-77, 64), (-64, 77), (-77, 90), (-76, 64), (-64, 76), (-64, 78), (-78, 90), (-90, 76), (-90, 78), (-78, 64), (-76, 90), (-75, 64), (-64, 75), (-64, 79), (-79, 90), (-90, 75), (-90, 79), (-79, 64), (-75, 90), (-74, 64), (-64, 74), (-64, 80), (-80, 90), (-90, 74), (-90, 80), (-80, 64), (-74, 90), (-73, 65), (-65, 73), (-65, 81), (-81, 89), (-89, 73), (-89, 81), (-81, 65), (-73, 89), (-72, 65), (-65, 72), (-65, 82), (-82, 89), (-89, 72), (-89, 82), (-82, 65), (-72, 89), (-71, 65), (-65, 71), (-65, 83), (-83, 89), (-89, 71), (-89, 83), (-83, 65), (-71, 89), (-70, 66), (-66, 70), (-66, 84), (-84, 88), (-88, 70), (-88, 84), (-84, 66), (-70, 88), (-69, 67), (-67, 69), (-67, 85), (-85, 87), (-87, 69), (-87, 85), (-85, 67), (-69, 87), (-68, 68), (-68, 86), (-86, 86), (-86, 68)]
    assert len(c4) == len(set(c4)) # test for duplicate points

    with pytest.raises(NotImplementedError):
        list(pybresenham.circle(0,0,0,filled=True))
    with pytest.raises(NotImplementedError):
        list(pybresenham.circle(0,0,0,thickness =2))
    with pytest.raises(NotImplementedError):
        list(pybresenham.circle(0,0,0,viewport=1))


def test_diamond():
    assert list(pybresenham.diamond(0,0,3)) == [(4, 0), (3, 1), (5, 1), (2, 2), (6, 2), (1, 3), (7, 3), (2, 4), (6, 4), (3, 5), (5, 5), (4, 6)]
    assert list(pybresenham.diamond(2,3,5)) == [(8, 3), (7, 4), (9, 4), (6, 5), (10, 5), (5, 6), (11, 6), (4, 7), (12, 7), (3, 8), (13, 8), (4, 9), (12, 9), (5, 10), (11, 10), (6, 11), (10, 11), (7, 12), (9, 12), (8, 13)]
    assert list(pybresenham.diamond(0,0,3, True)) == [(4, 0), (3, 1), (4, 1), (5, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (3, 5), (4, 5), (5, 5), (4, 6)]


def test_square():
    assert list(pybresenham.square(0, 0, 3)) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    assert list(pybresenham.square(-3, -3, 3)) == [(-3, -3), (-2, -3), (-1, -3), (-1, -2), (-1, -1), (-2, -1), (-3, -1), (-3, -2)]
    assert list(pybresenham.square(-3, -3, 4)) == [(-3, -3), (-2, -3), (-1, -3), (0, -3), (0, -2), (0, -1), (0, 0), (-1, 0), (-2, 0), (-3, 0), (-3, -1), (-3, -2)]

    assert list(pybresenham.square(0, 0, 3, True)) == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    assert list(pybresenham.square(0, 0, 3, filled=True)) == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    assert list(pybresenham.square(-1, -1, 3, filled=True)) == [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    # Make sure invalid lengths are caught.
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.square(0, 0, 0))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.square(0, 0, -1))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.square(0, 0, 'invalid'))

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        list(pybresenham.square(0,0,1, thickness=2))
    with pytest.raises(NotImplementedError):
        list(pybresenham.square(0,0,1, viewport=2))


def test_rectangle():
    assert list(pybresenham.rectangle(0, 0, 3, 3)) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    assert list(pybresenham.rectangle(0, 0, 5, 3)) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 1)]
    assert list(pybresenham.rectangle(0, 0, 3, 5)) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1)]
    assert list(pybresenham.rectangle(-2, -2, 3, 5)) == [(-2, -2), (-1, -2), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2), (-2, 1), (-2, 0), (-2, -1)]

    assert list(pybresenham.rectangle(0, 0, 3, 3, True)) == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    assert list(pybresenham.rectangle(0, 0, 3, 3, filled=True)) == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    assert list(pybresenham.rectangle(0, 0, 3, 5, filled=True)) == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4)]
    assert list(pybresenham.rectangle(0, 0, 5, 3, filled=True)) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]

    # Make sure invalid widths and heights are caught.
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, 0, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, -1, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, 0, 'invalid'))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, 2, 0))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, 2, -1))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.rectangle(0, 0, 'invalid', 2))


    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        list(pybresenham.rectangle(0,0,1,1, thickness=2))
    with pytest.raises(NotImplementedError):
        list(pybresenham.rectangle(0,0,1,1, viewport=2))


def test_ellipse():
    with pytest.raises(NotImplementedError):
        pybresenham.ellipse(0,0)


def test_ellipseVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.ellipseVertices()


def test_arc():
    with pytest.raises(NotImplementedError):
        pybresenham.arc(0,0,0,0,0,0,0,0,0)


def test_arcVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.arcVertices(0,0,0,0,0,0)


def test_star():
    with pytest.raises(NotImplementedError):
        pybresenham.star(0,0,0,0,0,0,0)


def test_starVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.starVertices(0,0,0,0)


def test_grid():
    # Test a few different grid configurations.
    points = list(pybresenham.grid(0, 0, 3, 3, 3, 3))
    assert points == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (0, 7), (0, 9), (0, 10), (0, 11), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 9), (4, 10), (4, 11), (8, 1), (8, 2), (8, 3), (8, 5), (8, 6), (8, 7), (8, 9), (8, 10), (8, 11), (12, 1), (12, 2), (12, 3), (12, 5), (12, 6), (12, 7), (12, 9), (12, 10), (12, 11)]
    points = list(pybresenham.grid(5, 7, 3, 3, 3, 3))
    assert points == [(5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (17, 7), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19), (11, 19), (12, 19), (13, 19), (14, 19), (15, 19), (16, 19), (17, 19), (5, 8), (5, 9), (5, 10), (5, 12), (5, 13), (5, 14), (5, 16), (5, 17), (5, 18), (9, 8), (9, 9), (9, 10), (9, 12), (9, 13), (9, 14), (9, 16), (9, 17), (9, 18), (13, 8), (13, 9), (13, 10), (13, 12), (13, 13), (13, 14), (13, 16), (13, 17), (13, 18), (17, 8), (17, 9), (17, 10), (17, 12), (17, 13), (17, 14), (17, 16), (17, 17), (17, 18)]
    points = list(pybresenham.grid(0, 0, 1, 2, 3, 4))
    assert points == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7), (0, 8), (0, 9), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (4, 9)]
    points = list(pybresenham.grid(0, 0, 1, 2, 3, 4, 2))
    assert points == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (0, 13), (1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (0, 2), (0, 3), (0, 4), (0, 5), (0, 8), (0, 9), (0, 10), (0, 11), (1, 2), (1, 3), (1, 4), (1, 5), (1, 8), (1, 9), (1, 10), (1, 11), (5, 2), (5, 3), (5, 4), (5, 5), (5, 8), (5, 9), (5, 10), (5, 11), (6, 2), (6, 3), (6, 4), (6, 5), (6, 8), (6, 9), (6, 10), (6, 11)]
    points = list(pybresenham.grid(0, 0, 1, 2, 3, 4, 4))
    assert points == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (0, 16), (1, 16), (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (0, 17), (1, 17), (2, 17), (3, 17), (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (0, 18), (1, 18), (2, 18), (3, 18), (4, 18), (5, 18), (6, 18), (7, 18), (8, 18), (9, 18), (10, 18), (0, 19), (1, 19), (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19), (0, 4), (0, 5), (0, 6), (0, 7), (0, 12), (0, 13), (0, 14), (0, 15), (1, 4), (1, 5), (1, 6), (1, 7), (1, 12), (1, 13), (1, 14), (1, 15), (2, 4), (2, 5), (2, 6), (2, 7), (2, 12), (2, 13), (2, 14), (2, 15), (3, 4), (3, 5), (3, 6), (3, 7), (3, 12), (3, 13), (3, 14), (3, 15), (7, 4), (7, 5), (7, 6), (7, 7), (7, 12), (7, 13), (7, 14), (7, 15), (8, 4), (8, 5), (8, 6), (8, 7), (8, 12), (8, 13), (8, 14), (8, 15), (9, 4), (9, 5), (9, 6), (9, 7), (9, 12), (9, 13), (9, 14), (9, 15), (10, 4), (10, 5), (10, 6), (10, 7), (10, 12), (10, 13), (10, 14), (10, 15)]

    # TODO - add test that uses negative values for gridLeft and gridTop

    # Test several grid configurations to make sure duplicate points aren't returned.
    for numBoxesWide in range(1, 5):
        for numBoxesHigh in range(1, 5):
            for boxWidth in range(1, 5):
                for boxHeight in range(1, 5):
                    for thickness in range(1, 5):
                        points = list(pybresenham.grid(0, 0, numBoxesWide, numBoxesHigh, boxWidth, boxHeight, thickness))
                        assert len(points) == len(frozenset(points))


    # Test invalid arguments
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid('invalid gridLeft', 2, 2, 2, 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 'invalid gridTop', 2, 2, 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 'invalid numBoxesWide', 2, 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 0, 2, 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 'invalid numBoxesHigh', 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 0, 2, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 'invalid boxWidth', 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 0, 2))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 2, 'invalid boxHeight'))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 2, 0))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 2, 2, 'invalid thickness'))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.grid(2, 2, 2, 2, 2, 2, 0))

    with pytest.raises(NotImplementedError):
        list(pybresenham.grid(2, 2, 2, 2, 2, 2, viewport=1))


def test_gridInterior():
    with pytest.raises(NotImplementedError):
        pybresenham.gridInterior(0,0,0,0,0,0,0,0)


def test_hexGrid():
    with pytest.raises(NotImplementedError):
        pybresenham.hexGrid()


def test_hexGridVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.hexGridVertices()


def test_hexGridInterior():
    with pytest.raises(NotImplementedError):
        pybresenham.hexGridInterior()


def test_necker():
    with pytest.raises(NotImplementedError):
        pybresenham.necker(0,0,0,0,0,0,0,0)


def test_neckerVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.neckerVertices(0,0,0,0,0)


def test_bezier():
    with pytest.raises(NotImplementedError):
        pybresenham.bezier()


def test_bezierVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.bezierVertices()


def test_roundedBox():
    with pytest.raises(NotImplementedError):
        pybresenham.roundedBox(0,0,0,0,0,0,0,0)


def test_roundedBoxVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.roundedBoxVertices(0,0,0,0,0)


def test_translatePoints():
    assert list(pybresenham.translatePoints([(0, 0), (10, 0), (0, 10), (10, 10)], 0, 0)) == [(0, 0), (10, 0), (0, 10), (10, 10)]
    assert list(pybresenham.translatePoints([(0, 0), (10, 0), (0, 10), (10, 10)], 3, 0)) == [(3, 0), (13, 0), (3, 10), (13, 10)]

    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.translatePoints('invalid points', 0, 0))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.translatePoints([(0, 0), (10, 0), (0, 10), (10, 10)], 'invalid', 0))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.translatePoints([(0, 0), (10, 0), (0, 10), (10, 10)], 0, 'invalid'))
    with pytest.raises(pybresenham.PyBresenhamException):
        list(pybresenham.translatePoints([(0, 0), (10, 0), (0, 'invalid'), (10, 10)], 0, 0))


if __name__ == '__main__':
    pytest.main()
