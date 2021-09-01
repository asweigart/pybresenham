# PyBresenham
A Python module of generators that generate x, y coordinates for various vector shapes such as lines, rectangles, etc. Named after Bresenham of line-algorithm fame.

For example:

```python
    >>> import pybresenham
    >>> pybresenham.line(0, 0, 3, 6)
    <generator object line at 0x00000000030923B8>
    >>> list(pybresenham.line(0, 0, 3, 6))
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
```

PyBresenham is currently under development, and is seeking contributors!


Installation
============

    pip install pybresenham

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
    >>> pybresenham._drawPoints(pybresenham.circle(0, 0, 3), bg=' ')
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
    >>> pybresenham._drawPoints(pybresenham.square(0, 0, 4), bg=' ')
    OOOO
    O  O
    O  O
    OOOO
    >>> pybresenham._drawPoints(pybresenham.rectangle(0, 0, 15, 4), bg=' ')
    OOOOOOOOOOOOOOO
    O             O
    O             O
    OOOOOOOOOOOOOOO

    >>> drawPoints(polygon(10, 10, 8, 5), bg=' ')
           O
          O O
         O   OO
        O      O
      OO        O
     O           O
    O             O
    O             O
     O           O
     O           O
     O           O
      O         O
      O         O
       O       O
       OOOOOOOOO

    >>> drawPoints(polygon(10, 10, 8, 5, rotationDegrees=20), bg=' ')
         OO
        O  OOO
        O     OO
       O        OO
      O          O
     O           O
     O           O
    O            O
     O           O
     O           O
      O          O
       O        OO
        O     OO
        O  OOO
         OO


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

The `thickness`, `filled`, `endcap`, and `viewport` parameters are still unimplemented. (Except for square() and rectangle(), which do implement the `filled` parameter.)

Support
-------

If you find this project helpful and would like to support its development, [consider donating to its creator on Patreon](https://www.patreon.com/AlSweigart).
