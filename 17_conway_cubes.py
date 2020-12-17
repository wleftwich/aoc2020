from itertools import product

def read_data(data, dim):
    """Origin at sw corner"""
    D = {}
    for (y, row) in enumerate(reversed(data.split())):
        for (x, val) in enumerate(row):
            coords = [x, y] + [0] * (dim - 2)
            D[tuple(coords)] = val
    return D

def make_deltas(dim):
    origin = tuple([0] * dim)
    return [x for x in product((-1, 0, 1), repeat=dim) if x != origin]

def add_tuples(a, b):
    return tuple(x + y for (x, y) in zip(a, b))

def apply_deltas(p, deltas):
    return (add_tuples(p, d) for d in deltas)

def next_coords(D):
    ks = list(D)
    dim = len(ks[0])
    ranges = []
    for d in range(dim):
        a = min(x[d] for x in ks) - 1
        z = max(x[d] for x in ks) + 2
        ranges.append(range(a, z))
    return product(*ranges)

def cycle(cube):
    deltas = make_deltas(len(next(iter(cube))))
    D = {}
    for k in next_coords(cube):
        v = cube.get(k, '.')
        active_nabe_count = 0
        for nk in apply_deltas(k, deltas):
            nv = cube.get(nk)
            if nv == '#':
                active_nabe_count += 1
        if v == '#':
            if active_nabe_count in [2, 3]:
                D[k] = '#'
            else:
                D[k] = '.'
        else:
            if active_nabe_count == 3:
                D[k] = '#'
            else:
                D[k] = '.'
    return D
   
testdata = """\
.#.
..#
###
"""

cube3 = read_data(testdata, 3)
for _ in range(6):
    cube3 = cycle(cube3)
part_1 = sum(v == '#' for v in cube3.values())
# 112
# took 164 msec

cube4 = read_data(testdata, 4)
for _ in range(6):
    cube4 = cycle(cube4)
part_2 = sum(v == '#' for v in cube4.values())
# 848
# took 5.23 sec

cube5 = read_data(testdata, 5)
for _ in range(6):
    cube5 = cycle(cube5)
bonus = sum(v == '#' for v in cube5.values())
# 5760
# took 3 min 13 sec

cube2 = read_data(testdata, 2)
for _ in range(6):
    cube2 = cycle(cube2)
flatland = sum(v == '#' for v in cube2.values())
# 5
# took 6.66 msec


