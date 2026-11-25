import math
DESIGNS = [
    ("D1", 2.00, "vertical", 0.6, 0.001),
    ("D2", 2.00, "diagonal", 0.6, 0.001),
    ("D3", 1.75, "horizontal", 0.5, 0.001),
    ("D4", 1.75, "vertical", 0.5, 0.001),
    ("D8", 2.75, "horizontal", 1.0, 0.001),
]
def layout(r0, orient):
    c = 5.0
    if orient == "horizontal": d = (r0/2, 0.0)
    elif orient == "vertical": d = (0.0, r0/2)
    else: d = (r0/2/math.sqrt(2), r0/2/math.sqrt(2))
    return [[c-d[0], c-d[1]], [c+d[0], c+d[1]]], [[0.0, 0.0], [0.0, 0.0]]
