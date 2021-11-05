import numpy as np
from numpy.linalg import det, norm
import drawSvg

def circumcircle(X):
    L = np.array([norm(X[(k + 2) % 3] - X[(k + 1) % 3]) for k in range(3)])
    p = sum([L[k] ** 2 * (sum(L ** 2) - 2 * L[k] ** 2) * X[k] for k in range(3)])
    area = 0.5 * abs(det(np.column_stack([np.ones(3), X])))
    return p / (16 * area ** 2)

scale = 200
points = scale * 0.5 * np.array([
    [-0.5, +0.5],
    [-0.75, -0.75],
    [+0.75, +0.75],
    [+0.5, -0.25],
])

cc1 = circumcircle(points[:3, :])
r1 = norm(points[0] - cc1)
cc2 = circumcircle(points[1:, :])
r2 = norm(points[1] - cc2)

drawing = drawSvg.Drawing(int(2.05 * scale), int(2.05 * scale), origin="center")
lkwargs = {"stroke_width": 2, "stroke": "blue", "fill_opacity": 0, "close": True}
ckwargs = {"stroke_width": 2, "stroke": "green", "fill_opacity": 0}
lines1 = drawSvg.Lines(*points[0], *points[1], *points[2], **lkwargs)
lines2 = drawSvg.Lines(*points[1], *points[2], *points[3], **lkwargs)
ccircle1 = drawSvg.Circle(*cc1, r1, **ckwargs)
ccircle2 = drawSvg.Circle(*cc2, r2, **ckwargs)
pts = [drawSvg.Circle(*p, 4, fill="black") for p in points]
[drawing.append(elt) for elt in [lines1, lines2, ccircle1, ccircle2, *pts]]
drawing.saveSvg("drawing1.svg")

points = scale * 0.5 * np.array([
    [-0.75, -0.75],
    [+0.5, -0.25],
    [-0.5, +0.5],
    [+0.75, +0.75],
])

cc1 = circumcircle(points[:3, :])
r1 = norm(points[0] - cc1)
cc2 = circumcircle(points[1:, :])
r2 = norm(points[1] - cc2)

drawing = drawSvg.Drawing(int(2.05 * scale), int(2.05 * scale), origin="center")
lines1 = drawSvg.Lines(*points[0], *points[1], *points[2], **lkwargs)
lines2 = drawSvg.Lines(*points[1], *points[2], *points[3], **lkwargs)
ccircle1 = drawSvg.Circle(*cc1, r1, **ckwargs)
ccircle2 = drawSvg.Circle(*cc2, r2, **ckwargs)
pts = [drawSvg.Circle(*p, 4, fill="black") for p in points]
[drawing.append(elt) for elt in [lines1, lines2, ccircle1, ccircle2, *pts]]
drawing.saveSvg("drawing2.svg")
