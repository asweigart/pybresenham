# NOTE: Many of these functions are just aliases for the polygon() function.
# NOTE: As a design decision, these functions will always yield two-integer tuples (and not floats or other types).
# NOTE: The *Vertices() functions return just the vertices. Drawing the complete shape usually involves just passing these vertices to the lines() function.

# TODO - if we implement the "fill=True" feature for these shapes, doesn't it become necessary to allocate the border's points all at once instead
# of yielding them one at a time? Otherwise we won't have enough info for the flood fill algorithm. Though I suppose we could just save the border
# xy points as we yield them, and then use that list for the flood fill.

__version__ = '0.0.4'

import itertools
import math


# Constants for end cap styles.
ROUNDED_CAP = 1

class Rect(object):
    pass # TODO similar to pygame's Rect class


class PyBresenhamException(Exception):
    pass


def _checkForIntOrFloat(arg):
    if not isinstance(arg, (int, float)):
        raise PyBresenhamException('argument must be int or float, not %s' % (arg.__class__.__name__))


def rotatePoint(x, y, rotationDegrees, pivotx=0, pivoty=0):
    it = rotatePoints([(x, y)], rotationDegrees, pivotx, pivoty)
    return next(it)


def rotatePoints(points, rotationDegrees, pivotx=0, pivoty=0):
    rotationRadians = math.radians(rotationDegrees % 360)

    for x, y in points:
        x -= pivotx
        y -= pivoty
        x, y = x * math.cos(rotationRadians) - y * math.sin(rotationRadians), x * math.sin(rotationRadians) + y * math.cos(rotationRadians)
        x += pivotx
        y += pivoty

        yield int(x), int(y)

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


def lines(points, closed=False, thickness=1, endcap=None, viewport=None, _skipFirst=False):
    if thickness != 1 or endcap is not None or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

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


def polygon(x, y, radius, sides, rotation=0, filled=False, thickness=1, viewport=None):
    if thickness != 1 or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    # TODO - Add stretchx and stretchy parameters

    # Validate sides (x, y, radius, and rotation are validated in polygonVertices())
    _checkForIntOrFloat(sides)
    if sides < 3:
        raise PyBresenhamException('sides argument must be at least 3')

    vertices = list(polygonVertices(x, y, radius, sides, rotation))

    if filled:
        # Run flood fill on the shape, starting from the center.
        borderPoints = list(lines(vertices, closed=True, thickness=thickness, endcap=None, viewport=viewport))
        return iter(floodFill(borderPoints, x, y))
    else:
        return lines(vertices, closed=True, thickness=thickness, endcap=None, viewport=viewport)


def polygonVertices(x, y, radius, sides, rotation=0):
    # TODO - validate x, y, radius, sides

    # Setting the start point like this guarantees a flat side will be on the "bottom" of the polygon.
    if sides % 2 == 1:
        angleOfStartPointDegrees = 90 + rotation
    else:
        angleOfStartPointDegrees = 90 + rotation - (180 / sides)

    #angleOfStartPointRadians = math.radians(angleOfStartPointDegrees)

    # yield the first point
    #yield (int(math.cos(angleOfStartPointRadians) * radius) + x, -(int(math.sin(angleOfStartPointRadians) * radius) + y))

    for sideNum in range(sides):
        angleOfPointRadians = math.radians(angleOfStartPointDegrees + (360 / sides * sideNum))
        yield (int(math.cos(angleOfPointRadians) * radius) + x, -(int(math.sin(angleOfPointRadians) * radius)) + y)


def floodFill(points, startx, starty):

    # Note: We're not going to use recursion here because 1) recursion is
    # overrated 2) on a large enough shape it would cause a stackoverflow
    # 3) flood fill doesn't strictly need recursion because it doesn't require
    # a stack and 4) recursion is overrated.

    # Find the min/max x/y values to get the "boundaries" of this shape, to
    # prevent an infinite loop.
    minx, miny = points[0]
    maxx, maxy = points[0]
    for bpx, bpy in points:
        if bpx < minx:
            minx = bpx
        if bpx > maxx:
            maxx = bpx
        if bpy < miny:
            miny = bpy
        if bpy > maxy:
            maxy = bpy

    allPoints = set(points) # Use a set because the look ups will be faster.
    del points # This might help memory usage, though most likely the caller still has a reference to it.
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



def circle(x, y, radius, filled=False, thickness=1, viewport=None):
    # Mid-point/Bresenham's Circle algorithm from https://www.daniweb.com/programming/software-development/threads/321181/python-bresenham-circle-arc-algorithm
    # and then modified to remove duplicates.

    # The order that the xy points are returned is eccentric due to the optimizations in the code, it is not a simple clockwise/counterclockwise sweep.
    if filled or thickness != 1 or viewport is not None:
        raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

    switch = 3 - (2 * radius)
    cx = 0
    cy = radius
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

    # Generate all the points.
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



def ellipse(rotation=0, filled=False, thickness=1): # TODO rect-based paramters or center xy parameters?
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def ellipseVertices():
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def arc(x, y, radius, startAngle, stopAngle, rotation=0, filled=False, thickness=1, endcap=None, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def arcVertices(x, y, radius, startAngle, stopAngle, numVertices):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def star(x, y, radius, points=5, rotation=0, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')
    # TODO - will call polygonVertices() to get the verticies needed for the star.

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


def necker(left, top, width, height, depth, wireframe=True, rotation=0, filled=False, thickness=1, viewport=None):
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


def roundedBox(left, top, width, height, radius, rotation=0, filled=False, thickness=1, viewport=None):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')


def roundedBoxVertices(left, top, width, height, radius):
    raise NotImplementedError('The pybresenham module is under development. You can contribute at https://github.com/asweigart/pybresenham')

