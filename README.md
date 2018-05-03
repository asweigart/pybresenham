# PyBresenham
A Python module of generators that generate x, y coordinates for various vector shapes such as lines, rectangles, etc. Named after Bresenham of line-algorithm fame.

`pip install pybresenham`

If you need the x, y coordinates that make up vector shapes such as lines, circles, etc., this module has generators that yield simple (x, y) tuples of the integer points in these shapes. This has applications anywhere you have a 2D grid of discrete points.

For example:

```python
    >>> import pybresenham
    >>> pybresenham.line(0, 0, 3, 6)
    <generator object line at 0x00000000030923B8>
    >>> list(pybresenham.line(0, 0, 3, 6))
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
```

PyBresenham is currently under development, and is seeking contributors!

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
