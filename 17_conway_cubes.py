from collections import defaultdict
from itertools import product

def read_data(data, dim):
    actives = set()
    for (i, row) in enumerate(data.split()):
        for (j, val) in enumerate(row):
            if val == '#':
                coords = [i, j] + [0] * (dim - 2)
                actives.add(tuple(coords))
    return actives


def add_tuples(a, b):
    return tuple(x + y for (x, y) in zip(a, b))


def cycle(actives):
    result = set()
    inactives = defaultdict(int)
    deltas = list(product((-1, 0, 1), repeat=len(next(iter(actives)))))
    for cube in actives:
        neighborhood = set(add_tuples(cube, d) for d in deltas)
        if len(neighborhood.intersection(actives)) in [3, 4]:
            result.add(cube)
        for inactive in neighborhood.difference(actives):
            inactives[inactive] += 1
    result.update(k for k, v in inactives.items() if v == 3)
    return result

testdata = """\
.#.
..#
###
"""

cube3 = read_data(testdata, 3)
for _ in range(6):
    cube3 = cycle(cube3)
part_1 = len(cube3)
# 112
# took 15 msec

cube4 = read_data(testdata, 4)
for _ in range(6):
    cube4 = cycle(cube4)
part_2 = len(cube4)
# 848
# took 163 msec

cube5 = read_data(testdata, 5)
for _ in range(6):
    cube5 = cycle(cube5)
d5 = len(cube5)
# 5760
# took 4.9 sec

cube2 = read_data(testdata, 2)
for _ in range(6):
    cube2 = cycle(cube2)
flatland = len(cube2)
# 5
# took 850 microsec

import time
t0 = time.time()
cube6 = read_data(testdata, 6)
for _ in range(6):
    cube6 = cycle(cube6)
    print(len(cube6), time.time() - t0)
d6 = len(cube6)
# 245 0.007897377014160156
# 464 0.2726321220397949
# 15744 0.8170702457427979
# 2240 19.55064821243286
# 103552 22.021578788757324
# 35936 144.75871062278748

