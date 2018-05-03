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
    assert list(pybresenham.polygon([(0, 0), (2, 0), (2, 2)])) == [(1, 0), (2, 0), (2, 1), (2, 2), (1, 1), (0, 0)]
    assert list(pybresenham.polygon([(0, 0), (3, 7), (-5, -9)])) == [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (2, 6), (2, 5), (1, 4), (1, 3), (0, 2), (0, 1), (-1, 0), (-1, -1), (-2, -2), (-2, -3), (-3, -4), (-3, -5), (-4, -6), (-4, -7), (-5, -8), (-5, -9), (-4, -8), (-4, -7), (-3, -6), (-3, -5), (-2, -4), (-2, -3), (-1, -2), (-1, -1), (0, 0)]

    # TODO Make sure no duplicate points are in the returned generators.

    # Test invalid points arguments.
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon(42)
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([(0, 0)]) # only 1 point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([]) # zero points
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([42]) # not iterable argument
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([('invalid', 0), (0, 0)]) # not a int/floats at first point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([(0, 'invalid'), (0, 0)]) # not a int/floats at first point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([(0, 0), (0, 0), ('invalid', 0)]) # not a int/floats at last point
    with pytest.raises(pybresenham.PyBresenhamException):
        pybresenham.polygon([(0, 0), (0, 0), (0, 'invalid')]) # not a int/floats at last point

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        pybresenham.polygon([(0,0),(0,0),(0,0)], filled=True)
    with pytest.raises(NotImplementedError):
        pybresenham.polygon([(0,0),(0,0),(0,0)], thickness=2)
    with pytest.raises(NotImplementedError):
        pybresenham.polygon([(0,0),(0,0),(0,0)], viewport=2)

def test_triangle():
    assert list(pybresenham.triangle(0, 0, 2, 4, 4, 0)) == [(0, 1), (1, 2), (1, 3), (2, 4), (3, 3), (3, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

    # Make sure no duplicate points are in the returned generators.
    for x1, y1, x2, y2, x3, y3 in [(-3, 19, -24, -9, 20, 8), (-20, -26, 28, -26, 7, 26), (1, 26, 3, 17, -10, 18)]:
        linePoints = list(pybresenham.triangle(x1, y1, x2, y2, x3, y3))
        assert len(linePoints) == len(frozenset(linePoints))

    # Test unimplemented parts.
    with pytest.raises(NotImplementedError):
        pybresenham.triangle(0,0,0,0,0,0, filled=True)
    with pytest.raises(NotImplementedError):
        pybresenham.triangle(0,0,0,0,0,0, thickness=2)
    with pytest.raises(NotImplementedError):
        pybresenham.triangle(0,0,0,0,0,0, viewport=2)

def test_hexagon():
    with pytest.raises(NotImplementedError):
        pybresenham.hexagon(0,0,0)


def test_hexgonVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.hexgonVertices(0,0,0)


def test_circle():
    with pytest.raises(NotImplementedError):
        pybresenham.circle(0,0,0,0,0,0)


def test_circleVertices():
    with pytest.raises(NotImplementedError):
        pybresenham.circleVertices(0,0,0,0)


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
