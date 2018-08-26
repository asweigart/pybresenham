# PyBresenham
A Python module of generators that generate x, y coordinates for various vector shapes such as lines, rectangles, etc. Named after Bresenham of line-algorithm fame.

Installation
============

    pip install pybresenham

If you need the x, y coordinates that make up vector shapes such as lines, circles, etc., this module has generators that yield simple (x, y) tuples of the integer points in these shapes. This has applications anywhere you have a 2D grid of discrete points.

For example:

```python
    >>> import pybresenham
    >>> pybresenham.line(0, 0, 3, 6)
    <generator object line at 0x00000000030923B8>
    >>> list(pybresenham.line(0, 0, 3, 6))
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
```

The coordinates are screen coordinates, with the (0, 0) origin in the upper left, the x-axis increases going right, and the y-axis increases going down.

PyBresenham is currently under development, and is seeking contributors!



Example Usage
=============

Get the points of a line from (0, 0) to (5, 10):

    >>> import pybresenham
    >>> for x, y in pybresenham.line(0, 0, 5, 10):
    ...     print('(%s, %s)' % (x, y))
    ...
    (0, 0)
    (0, 1)
    (1, 2)
    (1, 3)
    (2, 4)
    (2, 5)
    (3, 6)
    (3, 7)
    (4, 8)
    (4, 9)
    (5, 10)
    >>> list(pybresenham.line(0, 0, 5, 10))
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10)]

Get the points of a multiline from (0, 0) to (2, 0) to (2, 2):

>>> import pybresenham
>>> list(pybresenham.lines([(0, 0), (2, 0), (2, 2)]))
[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

Get the points of a circle, centered on (0, 0), with radius 3:

    >>> list(pybresenham.circle(0, 0, 3))
    [(0, -3), (3, 0), (0, 3), (1, -3), (3, -1), (3, 1), (-1, 3), (-3, -1), (-3, 1), (-1, -3), (1, 3), (2, -2), (2, 2), (-2, 2), (-2, -2)]

Get a quick drawing of the above circle:

    >>> import pybresenham
    >>> pybresenham._drawPoints(pybresenham.circle(0, 0, 3))
      OOO
     O   O
    O     O
    O     O
    O     O
     O   O
      OOO

Get a quick drawing of a square and rectangle:

    >>> import pybresenham
    >>> list(pybresenham.square(0, 0, 4))
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]
    >>> pybresenham._drawPoints(pybresenham.square(0, 0, 4))
    OOOO
    O  O
    O  O
    OOOO
    >>> pybresenham._drawPoints(pybresenham.rectangle(0, 0, 15, 4))
    OOOOOOOOOOOOOOO
    O             O
    O             O
    OOOOOOOOOOOOOOO

Road Map
========

The following functions aren't yet implemented:

* ellipse()
* ellipseVertices()
* arc()
* arcVertices()
* star()
* starVertices()
* hexGrid()
* hexGridVertices()
* hexGridInterior()
* bezier()
* bezierVertices()
* roundedBox()
* roundedBoxVertices()

The thickness, `filled`, `endcap`, and `viewport` parameters are still unimplemented. (Except for square() and rectangle(), which do implement the `filled` parameter.)
