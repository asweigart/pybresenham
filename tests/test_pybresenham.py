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

    # Test invalid points arguments.
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon('invalid x', 0, 10, 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 'invalid y', 10, 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 'invalid radius', 0)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(0, 0, 10, 'invalid rotation')

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        pybresenham.polygon(0, 0, 10, 0, filled=True)
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
    with pytest.raises(NotImplementedError):
        pybresenham.grid(0,0,0,0,0,0,0,0)


def test_gridVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.gridVertices(0,0,0,0,0,0)


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


def test_chevron():
    with pytest.raises(NotImplementedError):
        pybresenham.chevron()


def test_chevronVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.chevronVertices()


def test_diamond():
    with pytest.raises(NotImplementedError):
        pybresenham.diamond()


def test_diamondVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.diamondVertices()


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





if __name__ == '__main__':
    pytest.main()
