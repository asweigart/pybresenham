
# NOTE: This module is under development and the API could rapidly change with no deprecation warning period.

# TODO - circle() has a problem where it doesn't send off the point for the leftmost side.



# NOTE: Many of these functions are just aliases for the polygon() function.
# NOTE: As a design decision, these functions will always yield two-integer tuples (and not floats or other types).
# NOTE: The *Segments() functions return just the line segments. Drawing the complete shape usually involves just passing these segments to the segments() function.
# NOTE: The *Vertices() functions return just the line vertices. Drawing the complete shape usually involves just passing these vertices to the lines() function.

# NOTE: The *Vertices() functions return a list of (x, y) coordinates that form a single, snakey line, while *Segments functions return a list of (x1, y1, x2, y2) line segments, which don't necessarily connect with each other.

# TODO - if we implement the "fill=True" feature for these shapes, doesn't it become necessary to allocate the border's points all at once instead
# of yielding them one at a time? Otherwise we won't have enough info for the flood fill algorithm. Though I suppose we could just save the border
# xy points as we yield them, and then use that list for the flood fill.

__version__ = '0.0.4'

import doctest
import itertools
import math


# Constants for end cap styles.
ROUNDED_CAP = 1
SQUARE_CAP = 2


class PyBresenhamException(Exception):
    """
    This class exists to be raised for any expected exceptional cases in PyBresenham.
    If the PyBresenham module raises any other exception, you can assume this is
    caused by a bug in PyBresenham.
    """
    pass


def _checkForIntOrFloat(arg, minVal=None, maxVal=None):
    if not isinstance(arg, (int, float)):
        raise PyBresenhamException('argument must be int or float, not %s' % (arg.__class__.__name__))
    if minVal is not None and arg < minVal:
        raise PyBresenhamException('argument must be at least %s or greater' % (minVal))
    if maxVal is not None and arg > maxVal:
        raise PyBresenhamException('argument must be at most %s or less' % (maxVal))


def rotatePoint(x, y, rotationDegrees, pivotx=0, pivoty=0):
    """
    Rotates the point at `x` and `y` by `rotationDegrees`. The point is rotated
    around the origin by default, but can be rotated around another pivot point
    by specifying `pivotx` and `pivoty`.

    The points are rotated counterclockwise.

    Returns an x and y tuple.

    Since the final result will be integers, there is a large amount of
    rounding error that can take place.

    >>> rotatePoint(10, 0, 90)
    (0, 10)
    >>> rotatePoint(10, 0, 180)
    (-10, 0)
    >>> rotatePoint(10, 0, 45)
    (7, 7)
    """

    # Reuse the code in rotatePoints()
    return list(rotatePoints([(x, y)], rotationDegrees, pivotx, pivoty))[0]


def rotatePoints(points, rotationDegrees, pivotx=0, pivoty=0):
    """
    Rotates each x and y tuple in `points`` by `rotationDegrees`. The points
    are rotated around the origin by default, but can be rotated around another
    pivot point by specifying `pivotx` and `pivoty`.

    The points are rotated counterclockwise.

    Returns a generator that produces an x and y tuple for each point in `points`.

    >>> list(rotatePoints([(10, 0), (7, 7)], 45))
    [(7, 7), (0, 9)]
    """

    rotationRadians = math.radians(rotationDegrees % 360)

    for x, y in points:
        _checkForIntOrFloat(x)
        _checkForIntOrFloat(y)
        x -= pivotx
        y -= pivoty
        x, y = x * math.cos(rotationRadians) - y * math.sin(rotationRadians), x * math.sin(rotationRadians) + y * math.cos(rotationRadians)
        x += pivotx
        y += pivoty

        yield int(x), int(y)


def translatePoints(points, movex, movey):
    """
    Returns a generator that produces all of the (x, y) tuples in `points` moved over by `movex` and `movey`.

    >>> points = [(0, 0), (5, 10), (25, 25)]
    >>> list(translatePoints(points, 1, -3))
    [(1, -3), (6, 7), (26, 22)]
    """

    # Note: There is no translatePoint() function because that's trivial.
    _checkForIntOrFloat(movex)
    _checkForIntOrFloat(movey)
    try:
        for x, y in points:
            _checkForIntOrFloat(x)
            _checkForIntOrFloat(y)
            yield x + movex, y + movey
    except:
        raise PyBresenhamException('`points` argument must be an iterable of (x, y) points.')


def line(x1, y1, x2, y2, thickness=1, endcap=None, _skipFirst=False):
    """
    Returns a generator that produces all of the points in a line between `x1`, `y1` and `x2`, `y2`.

    (Note: The `thickness` and `endcap` parameters are not yet implemented.)

    >>> list(line(0, 0, 10, 3))
    [(0, 0), (1, 0), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 2), (8, 2), (9, 3), (10, 3)]
    >>> drawPoints(line(0, 0, 20, 3))
    OOOO,,,,,,,,,,,,,,,,,
    ,,,,OOOOOOO,,,,,,,,,,
    ,,,,,,,,,,,OOOOOO,,,,
    ,,,,,,,,,,,,,,,,,OOOO
    """

    if (thickness != 1) or (endcap is not None):
        raise NotImplementedError('The pybresenham module is under development and the filled and thickness parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

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


def lines(points, closed=False, thickness=1, endcap=None, _skipFirst=False):
    """
    Returns a generator that produces all of the points in the lines connecting the (x, y) tuples in `points`.

    If `closed` is `True`, then the last point will connect to the first point.

    (Note: The `thickness` and `endcap` parameters are not yet implemented.)

    >>> list(lines([(0, 0), (10, 3), (5, 5)]))
    [(0, 0), (1, 0), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 2), (8, 2), (9, 3), (10, 3), (9, 4), (8, 4), (7, 4), (6, 5), (5, 5)]
    >>> drawPoints(lines([(0, 0), (10, 3), (5, 5)]))
    OO,,,,,,,,,
    ,,OOOO,,,,,
    ,,,,,,OOO,,
    ,,,,,,,,,OO
    ,,,,,,,OOO,
    ,,,,,OO,,,,
    """

    if thickness != 1 or endcap is not None:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate points argument
    try:
        iter(points)
    except TypeError:
        raise PyBresenhamException('points must be an iterable')

    # Check that all the xy coordinates are either ints or floats.
    for i, point in enumerate(points):
        try:
            _checkForIntOrFloat(point[0])
            _checkForIntOrFloat(point[1])
        except:
            raise PyBresenhamException('point at index %s is not a tuple of two int/float values' % (i))

    if closed:
        # Validate the points argument for a closed multi-line shape.
        try:
            points[2] # Make sure there are at least three points for this closed irregular polygon.
            points = list(points)
            points.append(points[0]) # The final point connects back to the starting point.
        except:
            raise PyBresenhamException('points argument must have at least three points if closed==True')
        _skipFirst=True
    else:
        # Validate that there are at least two points.
        try:
            points[1]
        except:
            raise PyBresenhamException('points argument must have at least two points')

    # Technically, we're allocating all of the iterators for each line segment
    # at once, which isn't the most efficient way to do it but is the most
    # direct. And even this direct way still produces kind of unreadable code.
    # ("Line segment" means the line between two adjacent points in the points
    # parameter.)
    # We are using itertools.chain() to create one iterator from several
    # iterables (one iterable per line segment).
    if _skipFirst:
        return itertools.chain.from_iterable([line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], _skipFirst=True) for i in range(len(points) - 1)])
    else:
        return itertools.chain([(points[0][0], points[0][1])], # the first point in points
                               itertools.chain.from_iterable([line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], _skipFirst=True) for i in range(len(points) - 1)]))


'''
# TODO - Do we really need this function? Why can't the user just call line() multiple times?
def segments(segments, thickness=1, endcap=None):
    if thickness != 1 or endcap is not None:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate segments argument
    try:
        iter(segments)
    except TypeError:
        raise PyBresenhamException('segments must be an iterable')

    # Check that all the xy coordinates are either ints or floats.
    for i, segment in enumerate(segments):
        try:
            _checkForIntOrFloat(segment[0])
            _checkForIntOrFloat(segment[1])
            _checkForIntOrFloat(segment[2])
            _checkForIntOrFloat(segment[3])
        except:
            raise PyBresenhamException('segment at index %s is not a tuple of four int/float values' % (i))

    return itertools.chain.from_iterable([line(segments[i][0], segments[i][1], segments[i][2], segments[i][3]) for i in range(len(segments))])
'''


def polygon(x, y, radius, sides, rotationDegrees=0, stretchHorizontal=1.0, stretchVertical=1.0, filled=False, thickness=1):
    """
    Returns a generator that produces the (x, y) points of a regular polygon.
    `x` and `y` mark the center of the polygon, `radius` indicates the size,
    `sides` specifies what kind of polygon it is.

    Odd-sided polygons have a pointed corner at the top and flat horizontal
    side at the bottom. The `rotationDegrees` argument will rotate the polygon
    counterclockwise.

    The polygon can be stretched by passing `stretchHorizontal` or `stretchVertical`
    arguments. Passing `2.0` for `stretchHorizontal`, for example, will double with
    width of the polygon.

    If `filled` is set to `True`, the generator will also produce the interior
    (x, y) points.

    (Note: The `thickness` parameter is not yet implemented.)

    >>> list(polygon(10, 10, 8, 5))
    [(9, 3), (8, 4), (7, 5), (6, 6), (5, 6), (4, 7), (3, 8), (3, 9), (4, 10), (4, 11), (4, 12), (5, 13), (5, 14), (6, 15), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (14, 15), (15, 14), (15, 13), (16, 12), (16, 11), (16, 10), (17, 9), (17, 8), (16, 7), (15, 6), (14, 5), (13, 4), (12, 4), (11, 3), (10, 2)]
    >>> drawPoints(polygon(10, 10, 8, 5))
    ,,,,,,,O,,,,,,,
    ,,,,,,O,O,,,,,,
    ,,,,,O,,,OO,,,,
    ,,,,O,,,,,,O,,,
    ,,OO,,,,,,,,O,,
    ,O,,,,,,,,,,,O,
    O,,,,,,,,,,,,,O
    O,,,,,,,,,,,,,O
    ,O,,,,,,,,,,,O,
    ,O,,,,,,,,,,,O,
    ,O,,,,,,,,,,,O,
    ,,O,,,,,,,,,O,,
    ,,O,,,,,,,,,O,,
    ,,,O,,,,,,,O,,,
    ,,,OOOOOOOOO,,,
    >>> drawPoints(polygon(10, 10, 8, 5, rotationDegrees=20))
    ,,,,,OO,,,,,,,
    ,,,,O,,OOO,,,,
    ,,,,O,,,,,OO,,
    ,,,O,,,,,,,,OO
    ,,O,,,,,,,,,,O
    ,O,,,,,,,,,,,O
    ,O,,,,,,,,,,,O
    O,,,,,,,,,,,,O
    ,O,,,,,,,,,,,O
    ,O,,,,,,,,,,,O
    ,,O,,,,,,,,,,O
    ,,,O,,,,,,,,OO
    ,,,,O,,,,,OO,,
    ,,,,O,,OOO,,,,
    ,,,,,OO,,,,,,,
    """
    if thickness != 1:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate sides (x, y, radius, and rotationDegrees are validated in polygonVertices())
    _checkForIntOrFloat(sides)
    if sides < 3:
        raise PyBresenhamException('sides argument must be at least 3')

    vertices = list(polygonVertices(x, y, radius, sides, rotationDegrees, stretchHorizontal, stretchVertical))

    if filled:
        # Run flood fill on the shape, starting from the center.
        borderPoints = list(lines(vertices, closed=True, thickness=thickness, endcap=None))
        return iter(floodFill(borderPoints, x, y))
    else:
        return lines(vertices, closed=True, thickness=thickness, endcap=None)


def polygonVertices(x, y, radius, sides, rotationDegrees=0, stretchHorizontal=1.0, stretchVertical=1.0):
    """
    Returns a generator that produces the (x, y) points of the vertices of a regular polygon.
    `x` and `y` mark the center of the polygon, `radius` indicates the size,
    `sides` specifies what kind of polygon it is.

    Odd-sided polygons have a pointed corner at the top and flat horizontal
    side at the bottom. The `rotationDegrees` argument will rotate the polygon
    counterclockwise.

    The polygon can be stretched by passing `stretchHorizontal` or `stretchVertical`
    arguments. Passing `2.0` for `stretchHorizontal`, for example, will double with
    width of the polygon.

    If `filled` is set to `True`, the generator will also produce the interior
    (x, y) points.

    (Note: The `thickness` parameter is not yet implemented.)

    >>> list(polygonVertices(10, 10, 8, 5))
    [(10, 2.0), (3, 8.0), (6, 16.0), (14, 16.0), (17, 8.0)]
    >>> drawPoints(polygonVertices(10, 10, 8, 5))
    ,,,,,,,O,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    O,,,,,,,,,,,,,O
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,
    ,,,O,,,,,,,O,,,
    >>> drawPoints(polygonVertices(10, 10, 8, 5, rotationDegrees=20))
    ,,,,,O,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,O
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    O,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,O
    ,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,
    ,,,,,O,,,,,,,,
    """

    # TODO - validate x, y, radius, sides

    # Setting the start point like this guarantees a flat side will be on the "bottom" of the polygon.
    if sides % 2 == 1:
        angleOfStartPointDegrees = 90 + rotationDegrees
    else:
        angleOfStartPointDegrees = 90 + rotationDegrees - (180 / sides)

    for sideNum in range(sides):
        angleOfPointRadians = math.radians(angleOfStartPointDegrees + (360 / sides * sideNum))

        yield (  int(math.cos(angleOfPointRadians) * radius  * stretchHorizontal) + x,
               -(int(math.sin(angleOfPointRadians) * radius) * stretchVertical)   + y)


def floodFill(points, startx, starty):
    """
    Returns a set of the (x, y) points of a filled in area.

    `points` is an iterable of (x, y) tuples of an arbitrary shape.

    `startx` and `starty` mark the starting point (likely inside the
    arbitrary shape) to begin filling from.

    >>> drawPoints(polygon(5, 5, 4, 5))
    ,,,O,,,
    ,,O,O,,
    ,O,,,O,
    O,,,,,O
    O,,,,,O
    O,,,,,O
    ,O,,,O,
    ,OOOOO,
    >>> pentagonOutline = list(polygon(5, 5, 4, 5))
    >>> floodFill(pentagonOutline, 5, 5)
    {(7, 3), (4, 7), (4, 8), (5, 6), (6, 6), (7, 7), (6, 2), (5, 1), (3, 7), (2, 5), (8, 5), (5, 8), (6, 7), (3, 3), (5, 5), (7, 6), (4, 4), (6, 3), (3, 6), (3, 4), (8, 6), (6, 4), (5, 4), (2, 6), (4, 5), (5, 2), (7, 5), (4, 2), (6, 5), (5, 3), (3, 5), (6, 8), (4, 6), (5, 7), (3, 8), (7, 4), (4, 3), (7, 8), (2, 4), (8, 4)}
    >>> drawPoints(floodFill(pentagonOutline, 5, 5))
    ,,,O,,,
    ,,OOO,,
    ,OOOOO,
    OOOOOOO
    OOOOOOO
    OOOOOOO
    ,OOOOO,
    ,OOOOO,
    """

    # Note: We're not going to use recursion here because 1) recursion is
    # overrated 2) on a large enough shape it would cause a stackoverflow
    # 3) flood fill doesn't strictly need recursion because it doesn't require
    # a stack and 4) recursion is overrated.

    allPoints = set(points) # Use a set because the look ups will be faster.

    # Find the min/max x/y values to get the "boundaries" of this shape, to
    # prevent an infinite loop.
    minx = miny = maxx = maxy = None
    for bpx, bpy in points:
        if minx is None:
            # This is the first point, so set all the min/max to it.
            minx = maxx = bpx
            miny = maxy = bpy
            continue
        if bpx < minx:
            minx = bpx
        if bpx > maxx:
            maxx = bpx
        if bpy < miny:
            miny = bpy
        if bpy > maxy:
            maxy = bpy

    pointsToProcess = [(startx, starty)]
    while pointsToProcess:
        x, y = pointsToProcess.pop()

        # Process point to right left of x, y.
        if x + 1 < maxx and (x + 1, y) not in allPoints:
            pointsToProcess.append((x + 1, y))
            allPoints.add((x + 1, y))
        # Process point to the left of x, y.
        if x - 1 > minx and (x - 1, y) not in allPoints:
            pointsToProcess.append((x - 1, y))
            allPoints.add((x - 1, y))
        # Process point below x, y.
        if y + 1 < maxy and (x, y + 1) not in allPoints:
            pointsToProcess.append((x, y + 1))
            allPoints.add((x, y + 1))
        # Process point above x, y.
        if y - 1 > miny and (x, y - 1) not in allPoints:
            pointsToProcess.append((x, y - 1))
            allPoints.add((x, y - 1))
    return allPoints



def circle(x, y, radius, filled=False, thickness=1):
    """
    Returns a generator that produces the (x, y) tuples for the outline of a circle.

    `x` and `y` are the center of the circle, `radius` is the size.

    (Note: The `filled` and `thickness` parameter is not yet implemented.)

    >>> list(circle(0, 0, 7))
    [(-6, 3), (0, 7), (4, -6), (-7, 0), (7, -1), (7, -2), (2, -7), (5, -5), (-5, 5), (-1, -7), (-2, -7), (-4, 6), (7, 2), (5, 5), (-5, -5), (6, -4), (6, 3), (-6, 4), (3, 6), (-3, 6), (6, 4), (1, -7), (6, -3), (7, 1), (-6, -4), (-7, 2), (-4, -6), (-2, 7), (-1, 7), (2, 7), (7, 0), (-7, -1), (-7, -2), (4, 6), (0, -7), (-6, -3), (-7, 1), (1, 7), (3, -6), (-3, -6)]
    >>> drawPoints(circle(0, 0, 7))
    ,,,,,OOOOO,,,,,
    ,,,OO,,,,,OO,,,
    ,,O,,,,,,,,,O,,
    ,O,,,,,,,,,,,O,
    ,O,,,,,,,,,,,O,
    O,,,,,,,,,,,,,O
    O,,,,,,,,,,,,,O
    O,,,,,,,,,,,,,O
    O,,,,,,,,,,,,,O
    O,,,,,,,,,,,,,O
    ,O,,,,,,,,,,,O,
    ,O,,,,,,,,,,,O,
    ,,O,,,,,,,,,O,,
    ,,,OO,,,,,OO,,,
    ,,,,,OOOOO,,,,,
    """
    # Mid-point/Bresenham's Circle algorithm from https://www.daniweb.com/programming/software-development/threads/321181/python-bresenham-circle-arc-algorithm
    # and then modified to remove duplicates.

    # The order that the xy points are returned is rather unconventional due to the optimizations in the code, it is not a simple clockwise/counterclockwise sweep.
    if filled or thickness != 1:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    switch = 3 - (2 * radius)
    cx = 0
    cy = radius
    """
    # NOTE - This code leaves a point missing from the final circle on the left side. Until I can figure it out, I'm usin the old algorithm, which unforuntately defeats the purpose of having a generator.
    # 1st quarter/octant starts clockwise at 12 o'clock
    while cx <= cy:
        # Duplicates are formed whenever cx or cy is 0, or when cx == cy.
        # I've rearranged the original code to minimize if statements,
        # though it makes the code a bit inscrutable.
        yield ( cx + x, -cy + y) # 1st quarter 1st octant
        if cx != cy:
            yield ( cy + x, -cx + y) # 1st quarter 2nd octant
        if cx != 0:
            yield ( cy + x,  cx + y) # 2nd quarter 3rd octant
            if cy != 0:
                yield (-cx + x,  cy + y) # 3rd quarter 5th octant
                yield (-cy + x, -cx + y) # 4th quarter 7th octant
                if cx != cy:
                    yield (-cy + x,  cx + y) # 3rd quarter 6th octant
                    yield (-cx + x, -cy + y) # 4th quarter 8th octant
        if cy != 0 and cx != cy:
            yield ( cx + x,  cy + y) # 2nd quarter 4th octant

        if switch < 0:
            switch += (4 * cx) + 6
        else:
            switch += (4 * (cx - cy)) + 10
            cy -= 1
        cx += 1
    """
    points = set()
    while cx <= cy:
        # first quarter first octant
        points.add((cx + x,-cy + y))
        # first quarter 2nd octant
        points.add((cy + x,-cx + y))
        # second quarter 3rd octant
        points.add((cy + x,cx + y))
        # second quarter 4.octant
        points.add((cx + x,cy + y))
        # third quarter 5.octant
        points.add((-cx + x,cy + y))
        # third quarter 6.octant
        points.add((-cy + x,cx + y))
        # fourth quarter 7.octant
        points.add((-cy + x,-cx + y))
        # fourth quarter 8.octant
        points.add((-cx + x,-cy + y))
        if switch < 0:
            switch = switch + (4 * cx) + 6
        else:
            switch = switch + (4 * (cx - cy)) + 10
            cy = cy - 1
        cx = cx + 1
    return iter(points)





def square(left, top, length, filled=False, thickness=1):
    """Returns a generator that produces (x, y) tuples for a square.
    This function is an alias for the rectangle() function, with `length` passed for both the
    `width` and `height` parameters.

    The `left` and `top` arguments are the x and y coordinates for the topleft corner of the square.

    If `filled` is `True`, the interior points are also returned.

    NOTE: The `thickness` argument is not yet implemented.

    >>> list(square(0, 0, 5))
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1)]
    >>> drawPoints(square(0, 0, 5))
    OOOOO
    O,,,O
    O,,,O
    O,,,O
    OOOOO
    >>> drawPoints(square(0, 0, 5, filled=True))
    OOOOO
    OOOOO
    OOOOO
    OOOOO
    OOOOO
    """
    if thickness != 1:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    return rectangle(left, top, length, length, filled, thickness)


def rectangle(left, top, width, height, filled=False, thickness=1):
    """
    Returns a generator that produces (x, y) tuples for a rectangle.

    The `left` and `top` arguments are the x and y coordinates for the topleft corner of the square.

    If `filled` is `True`, the interior points are also returned.

    NOTE: The `thickness` argument is not yet implemented.

    >>> list(rectangle(0, 0, 10, 4))
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (9, 2), (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]
    >>> drawPoints(rectangle(0, 0, 10, 4))
    OOOOOOOOOO
    O,,,,,,,,O
    O,,,,,,,,O
    OOOOOOOOOO
    >>> drawPoints(rectangle(0, 0, 10, 4, filled=True))
    OOOOOOOOOO
    OOOOOOOOOO
    OOOOOOOOOO
    OOOOOOOOOO
    """

    # Note: For perfomance, this function does not rely on line() to generate its points.

    if thickness != 1:
        # TODO - should the original left and top be for the thick border, or should thick borders go to the left and above of the left and top coordinates?
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    # Validate arguments
    _checkForIntOrFloat(left)
    _checkForIntOrFloat(top)
    _checkForIntOrFloat(width)
    _checkForIntOrFloat(height)

    left, top, width, height = int(left), int(top), int(width), int(height)

    if width < 1 or height < 1:
        raise PyBresenhamException('width and height must be positive integers')

    # Generate all the points.
    if filled:
        for y in range(top, top + height):
            for x in range(left, left + width):
                yield (x, y)
    else:
        # Note: The `- 1` adjustments here are to prevent duplicate coordinates of the corners being returned.

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


def diamond(x, y, radius, filled=False, thickness=1):
    """
    Returns a generator that produces (x, y) tuples in a diamond shape.
    It is easier to predict the size of the diamond that this function
    produces, as opposed to creatinga 4-sided polygon with `polygon()`
    and rotating it 45 degrees.

    The `left` and `top` arguments are the x and y coordinates for the topleft corner of the square.

    The width and height of the diamond will be `2 * radius + 1`.

    If `filled` is `True`, the interior points are also returned.

    In this example diamond shape, the D characters represent the
    drawn diamond, the . characters represent the "outside spaces",
    and the ' characters represent the "inside spaces".
    (The radius of this example diamond is 3.)

    ...D
    ..D'D
    .D'''D
    D'''''D
    .D'''D
    ..D'D
    ...D

    >>> list(diamond(0, 0, 3))
    [(4, 0), (3, 1), (5, 1), (2, 2), (6, 2), (1, 3), (7, 3), (2, 4), (6, 4), (3, 5), (5, 5), (4, 6)]
    >>> drawPoints(diamond(0, 0, 3))
    ,,,O,,,
    ,,O,O,,
    ,O,,,O,
    O,,,,,O
    ,O,,,O,
    ,,O,O,,
    ,,,O,,,
    >>> drawPoints(diamond(0, 0, 3, filled=True))
    ,,,O,,,
    ,,OOO,,
    ,OOOOO,
    OOOOOOO
    ,OOOOO,
    ,,OOO,,
    ,,,O,,,
    """

    if thickness != 1:
        raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')

    outsideSpaces = radius
    insideSpaces = 1 # We'll only start incrementing insidesSpaces on the 2nd row.

    for row in range(radius * 2 + 1):
        # Yield the leftside point in this row.
        yield (outsideSpaces + 1 + x, row + y)

        if row != 0 and row != radius * 2:
            # (The first and last rows only have one point per row.)

            if filled:
                # Yield all the interior spaces in this row.
                for interiorx in range(outsideSpaces + 2 + x, outsideSpaces + insideSpaces + 2 + x):
                    yield (interiorx, row + y) # No need for "+ x" here, we did that in the range() call.

            # Yield the rightside point in this row.
            yield (outsideSpaces + insideSpaces + 2 + x, row + y)

        # Modify outsideSpaces/insideSpaces as we move down the rows.
        if row < radius:
            outsideSpaces -= 1
            if row != 0:
                insideSpaces += 2
        else:
            outsideSpaces += 1
            insideSpaces -= 2

'''
# TODO The following functions still need implementing.

def ellipse(rotation=0, filled=False, thickness=1): # TODO rect-based paramters or center xy parameters?
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def ellipseVertices():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def arc(x, y, radius, startAngle, stopAngle, rotation=0, filled=False, thickness=1, endcap=None):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def arcVertices(x, y, radius, startAngle, stopAngle, numVertices):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def star(x, y, radius, points=5, rotation=0, filled=False, thickness=1):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')
    # TODO - will call polygonVertices() to get the verticies needed for the star.

def starVertices(x, y, radius, points=5):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')
'''

def grid(gridLeft, gridTop, numBoxesWide, numBoxesHigh, boxWidth, boxHeight, thickness=1):
    """
    Returns a generator that produces (x, y) tuples for a grid.

    The `gridLeft` and `gridTop` arguments are the x and y coordinates for the topleft corner of the grid.

    The `numBoxesWide` and `numBoxesHigh` arguments are the number of boxes (or, cells) in the grid.

    The `boxWidth` and `boxHeight` are the size of each box (or, cell). This is the size of the box's
    interior, and doesn't include the lines of the grid.

    The `thickness` argument is how the thick the grid lines are.

    The width of the grid is `(numBoxesWide * boxWidth) + (thickness * (numBoxesWide + 1))`.

    The height of the grid is `(numBoxesHeight * boxheight) + (thickness * (numBoxesHeight + 1))`.


    >>> list(grid(0, 0, 3, 2, 5, 4))
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7), (0, 8), (0, 9), (6, 1), (6, 2), (6, 3), (6, 4), (6, 6), (6, 7), (6, 8), (6, 9), (12, 1), (12, 2), (12, 3), (12, 4), (12, 6), (12, 7), (12, 8), (12, 9), (18, 1), (18, 2), (18, 3), (18, 4), (18, 6), (18, 7), (18, 8), (18, 9)]

    >>> drawPoints(grid(0, 0, 3, 2, 5, 4))
    OOOOOOOOOOOOOOOOOOO
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    OOOOOOOOOOOOOOOOOOO
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    O,,,,,O,,,,,O,,,,,O
    OOOOOOOOOOOOOOOOOOO
    >>> drawPoints(grid(0, 0, 3, 2, 5, 4, thickness=2))
    OOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OO,,,,,OO,,,,,OO,,,,,OO
    OOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOO
    """

    # Validate arguments.
    _checkForIntOrFloat(gridLeft)
    _checkForIntOrFloat(gridTop)
    _checkForIntOrFloat(numBoxesWide)
    _checkForIntOrFloat(numBoxesHigh)
    _checkForIntOrFloat(boxWidth)
    _checkForIntOrFloat(boxHeight)
    _checkForIntOrFloat(thickness)

    numBoxesWide = int(numBoxesWide)
    numBoxesHigh = int(numBoxesHigh)
    boxWidth = int(boxWidth)
    boxHeight = int(boxHeight)
    thickness = int(thickness)

    if numBoxesWide < 1:
        raise PyBresenhamException('numBoxesWide must be 1 or greater')
    if numBoxesHigh < 1:
        raise PyBresenhamException('numBoxesHigh must be 1 or greater')
    if boxWidth < 1:
        raise PyBresenhamException('boxWidth must be 1 or greater')
    if boxHeight < 1:
        raise PyBresenhamException('boxHeight must be 1 or greater')
    if thickness < 1:
        raise PyBresenhamException('thickness must be 1 or greater')


    # Record the y coordinates so we don't repeat the points at the intersections
    # of the grid.
    intersectiony = set()

    """Generate the points for the horizontal lines of the grid.
    i.e. the - characters in this diagram:
    ----------
    |  |  |  |
    |  |  |  |
    ----------
    |  |  |  |
    |  |  |  |
    ----------
    |  |  |  |
    |  |  |  |
    ----------"""
    for gridRow in range(numBoxesHigh + 1):
        for thicknessIndex in range(thickness): # thicknessIndex isn't a great name, but each "grid row" can be multiple points tall if thickness > 1
            y = (boxHeight * gridRow) + (thickness * gridRow) + thicknessIndex
            intersectiony.add(y)
            for x in range(numBoxesWide * boxWidth + (thickness * (numBoxesWide + 1))):
                yield (x + gridLeft, y + gridTop)

    """Generate the points for the vertical lines in between the horizontal lines of the grid.
    i.e. the | characters in this diagram:
    ----------
    |  |  |  |
    |  |  |  |
    ----------
    |  |  |  |
    |  |  |  |
    ----------
    |  |  |  |
    |  |  |  |
    ----------"""
    for gridColumn in range(numBoxesWide + 1):
        for thicknessIndex in range(thickness): # thicknessIndex isn't a great name, but each "grid row" can be multiple points tall if thickness > 1
            x = (boxWidth * gridColumn) + (thickness * gridColumn) + thicknessIndex
            for y in range(numBoxesHigh * boxHeight + (thickness * (numBoxesHigh + 1))):

                # Additionally, we don't want to yield xy points we've yielded before.
                """ i.e. These would be the points at the intersections of the grid,
                at the + characters in this diagram:
                    +--+--+--+
                    |  |  |  |
                    |  |  |  |
                    +--+--+--+
                    |  |  |  |
                    |  |  |  |
                    +--+--+--+
                    |  |  |  |
                    |  |  |  |
                    +--+--+--+"""
                if y not in intersectiony:
                    yield (x + gridLeft, y + gridTop)

'''
def gridInterior(gridLeft, gridTop, numBoxesWide, numBoxesHigh, boxWidth, boxHeight, thickness=1):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def hexGrid():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def hexGridVertices():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def hexGridInterior():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def necker(left, top, width, height, depth, wireframe=True, rotation=0, filled=False, thickness=1):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')
    """
    The axii look like:        Positive width looks like:

    height
    |
    |  /depth
    | /
    |/_____width
    """


def neckerSegments(left, top, width, height, depth, wireframe=True):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def bezier():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def bezierSegments():
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def roundedBox(left, top, width, height, radius, rotation=0, filled=False, thickness=1):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')


def roundedBoxSegments(left, top, width, height, radius):
    raise NotImplementedError('The pybresenham module is under development and the filled, thickness, and endcap parameters are not implemented. You can contribute at https://github.com/asweigart/pybresenham')
'''

def drawPoints(points, bg=','):
    """A small debug function that takes an iterable of (x, y) integer tuples
    and draws them to the screen."""

    # Note: I set bg to ',' instead of '.' because using ... in the docstrings
    # confuses doctest and makes it think it's Python's secondary ... prompt,
    # causing doctest errors.
    import sys
    points = list(points)
    try:
        points = [(int(x), int(y)) for x, y in points]
    except:
        raise PyBresenhamException('points must only contains (x, y) numeric tuples')

    # Calculate size of the character grid from the given points.
    minx = min([x for x, y in points])
    maxx = max([x for x, y in points])
    miny = min([y for x, y in points])
    maxy = max([y for x, y in points])

    charGrid = [[' '] * (maxy - miny + 1) for i in range(maxx - minx + 1)]

    # Draw O characters to the grid at the given points.
    for x, y in points:
        charGrid[x - minx][y - miny] = 'O'

    # Print out the character grid.
    for y in range(len(charGrid[0])):
        for x in range(len(charGrid)):
            if charGrid[x][y] in (None, ' '):
                charToDraw = bg
            else:
                charToDraw = charGrid[x][y]
            sys.stdout.write(charToDraw)
        print()


if __name__ == '__main__':
    print(doctest.testmod())