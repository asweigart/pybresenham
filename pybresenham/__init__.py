# NOTE: Many of these functions are just aliases for the polygon() function.
# NOTE: As a design decision, these functions will always yield two-integer tuples (and not floats or other types).
# NOTE: The *Vertices() functions return just the vertices. Drawing the complete shape usually involves just passing these vertices to the lines() function.


import itertools


# Constants for end cap styles.
ROUNDED_CAP = 1

class Rect(object):
    pass # TODO similar to pygame's Rect class


class PyBresenhamException(Exception):
    pass


def _checkForIntOrFloat(arg):
    if not isinstance(arg, (int, float)):
        raise PyBresenhamException('argument must be int or float, not %s' % (arg.__class__.__name__))


def rotatePoints(points, originx, originy):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def line(x1, y1, x2, y2, thickness=1, endcap=None, viewport=None, _skipFirst=False):
    if (thickness != 1) or (endcap is not None) or (viewport is not None):
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    _checkForIntOrFloat(x1)
    _checkForIntOrFloat(y1)
    _checkForIntOrFloat(x2)
    _checkForIntOrFloat(y2)
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # TODO - Do we want this line?

    if not isinstance(_skipFirst, bool):
        raise PyBresenhamException('_skipFirst argument must be a bool')

    isSteep = abs(y2-y1) > abs(x2-x1)
    if isSteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    isReversed = x1 > x2

    if isReversed:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y2
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x2, x1 - 1, -1):
            if isSteep:
                if not (_skipFirst and (x, y) == (x2, y2)):
                    yield (y, x)
            else:
                if not (_skipFirst and (x, y) == (x2, y2)):
                    yield (x, y)
            error -= deltay
            if error <= 0:
                y -= ystep
                error += deltax
    else:
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if isSteep:
                if not (_skipFirst and (x, y) == (x1, y1)):
                    yield (y, x)
            else:
                if not (_skipFirst and (x, y) == (x1, y1)):
                    yield (x, y)
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax


def lines(points, thickness=1, endcap=None, viewport=None):
    if thickness != 1 or endcap is not None or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate points argument
    try:
        iter(points)
    except TypeError:
        raise PyBresenhamException('points must be an iterable')

    for i, point in enumerate(points):
        try:
            _checkForIntOrFloat(point[0])
            _checkForIntOrFloat(point[1])
        except:
            raise PyBresenhamException('point at index %s is not a tuple of two int/float values' % (i))

    if len(points) < 2:
        raise PyBresenhamException('points argument must have at least two points')

    return itertools.chain([(points[0][0], points[0][1])], # the first point in points
                           itertools.chain.from_iterable([line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], _skipFirst=True) for i in range(len(points) - 1)]))


def polygon(points, filled=False, thickness=1, viewport=None):
    if filled or thickness != 1 or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    try:
        points[2] # Make sure there are at least three points for this polygon.
        points.append(points[0]) # Polygons are lines that connect back to their starting point.
    except:
        raise PyBresenhamException('points argument must have at least three points')

    return lines(points, thickness, None, viewport)


def triangle(x1, y1, x2, y2, x3, y3, filled=False, thickness=1, viewport=None):
    """An alias for the polygon() function, with simplified parameters."""
    return polygon(((x1, y1), (x2, y2), (x3, y3)), filled, thickness, viewport)


def hexagon(x, y, radius, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def hexgonVertices(x, y, radius):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def circle(x, y, radius, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def circleVertices(x, y, radius, numVertices):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def square(left, top, length, filled=False, thickness=1, viewport=None):
    """An alias for the rectangle() function, with simplified parameters."""
    if thickness != 1 or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    return rectangle(left, top, length, length, filled, thickness, viewport)


def rectangle(left, top, width, height, filled=False, thickness=1, viewport=None):

    # Note: For perfomance, this function does not rely on line() to generate its points.

    if thickness != 1 or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate arguments
    _checkForIntOrFloat(left)
    _checkForIntOrFloat(top)
    _checkForIntOrFloat(width)
    _checkForIntOrFloat(height)

    left, top, width, height = int(left), int(top), int(width), int(height)

    if width < 1 or height < 1:
        raise PyBresenhamException('width and height must be positive integers')

    # Return points.
    if filled:
        for y in range(top, top + height):
            for x in range(left, left + width):
                yield (x, y)
    else:
        # Note: The -1 nad +2 adjustments here are to prevent duplicate coordinates of the corners being returned.

        # Top side.
        y = top
        for x in range(left, left + width - 1):
            yield (x, y)

        # Right side.
        x = left + width - 1
        for y in range(top, top + height - 1):
            yield (x, y)

        # Bottom side.
        y = top + height - 1
        for x in range(left + width - 1, left, -1):
            yield (x, y)

        # Left side.
        x = left
        for y in range(top + height - 1, top, -1):
            yield (x, y)



def ellipse(filled=False, thickness=1): # TODO rect-based paramters or center xy parameters?
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def ellipseVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def arc(x, y, radius, startAngle, stopAngle, filled=False, thickness=1, endcap=None, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def arcVertices(x, y, radius, startAngle, stopAngle, numVertices):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def star(x, y, radius, points=5, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def starVertices(x, y, radius, points=5):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def grid(gridLeft, gridTop, numBoxesWide, numBoxesHigh, boxWidth, boxHeight, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def gridVertices(gridLeft, gridTop, numBoxesWide, numBoxesHigh, boxWidth, boxHeight):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def gridInterior(gridLeft, gridTop, numBoxesWide, numBoxesHigh, boxWidth, boxHeight, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def hexGrid():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def hexGridVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def hexGridInterior():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def necker(left, top, width, height, depth, wireframe=True, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def neckerVertices(left, top, width, height, depth, wireframe=True):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def chevron():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def chevronVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def diamond():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def diamondVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def bezier():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def bezierVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def roundedBox(left, top, width, height, radius, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def roundedBoxVertices(left, top, width, height, radius):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

