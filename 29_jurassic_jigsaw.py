import math
from collections import defaultdict, deque, Counter

import numpy as np
from scipy import ndimage

datafile = 'data/20-1.txt'

NESW = [0+1j, 1+0j, 0-1j, -1+0j]


def parse_data(txt):
    recs = [y for y in (x.strip() for x in txt.split('\n\n')) if y]
    return [parse_rec(rec) for rec in recs]


def parse_rec(rec):
    lines = [y for y in (x.strip() for x in rec.split('\n')) if y]
    label = lines[0].split()[1][:-1]
    tile = [
        [int(x) for x in line.replace('#', '1').replace('.', '0')]
            for line in lines[1:]
    ]
    return (label, np.array(tile))


def tile_orientations(tile):
    for r in range(4):
        a = np.rot90(tile, r)
        yield a
        yield np.fliplr(a)
        yield np.flipud(a)
        yield np.flipud(np.fliplr(a))


def encode_edges(tile):
    return [
        int(''.join(map(str, x)), 2)
        for x in [tile[0, :], tile[:, -1], tile[-1, :], tile[:, 0]] # N, E, S, W
    ]


def all_tile_edges(tile_data):
    labels = []
    a = np.empty((len(tile_data), 16, 4), dtype=int)
    for i, tile_rec in enumerate(tile_data):
        label, tile = tile_rec
        labels.append(label)
        for j, orient in enumerate(tile_orientations(tile)):
            for k, edge in enumerate(encode_edges(orient)):
                a[i, j, k] = edge
    return labels, a


def place_tile(pos, i, j, grid, tiles):
    sides = {c: v for (c, v) in zip(NESW, tiles[i, j])}
    grid[pos] = (i, j, sides)


def open_positions(grid, n):
    if not grid:
        return []
    
    sidelen = math.sqrt(n)
    xs = [int(k.real) for k in grid]
    ys = [int(k.imag) for k in grid]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
   
    openpos = defaultdict(set)
    for k in grid:
        for drxn in NESW:
            newk = k + drxn
            if newk in grid:
                continue

            # stay in bounds
            x, y = newk.real, newk.imag
            if max(x, xmax) - min(x, xmin) + 1 > sidelen:
                continue
            if max(y, ymax) - min(y, ymin) + 1 > sidelen:
                continue
            
            for drxn2 in NESW:
                nabe = newk + drxn2
                if nabe in grid:
                    openpos[newk].add(nabe)
                    
    ## Fill inside corners first. Doing a dfs, so push them on the stack last.
    return [e for (e, v) in sorted(openpos.items(), key=lambda x: len(x[1]))]


def possible_tiles(pos, grid, tiles):
    already_placed = set(i for (i, j, s) in grid.values())
    if not already_placed:
        return set()

    filters = []
    for drxn in NESW:
        nabe_pos = pos + drxn
        nabe = grid.get(nabe_pos)
        if nabe is None:
            continue
        ni, nj, nsides = nabe
        filters.append((NESW.index(drxn), nsides[-drxn]))
    if not filters:
        return set()

    tilesets = (set((i, j) for (i, j, k) in zip(*np.where(tiles == val))
                       if k == slot and i not in already_placed)
                for slot, val in filters)
    try:
        tileset_intersect = next(tilesets)
    except StopIteration:
        return set()
    for ts in tilesets:
        tileset_intersect.intersection_update(ts)
    
    return tileset_intersect


def save_grid(grid):
    return frozenset((complex(k), a, b) for (k, (a, b, _)) in grid.items())


def load_grid(state, tiles):
    grid = {}
    for pos, i, j in state:
        place_tile(pos, i, j, grid, tiles)
    return grid


def dfs(tiles, initial_state=None, n=None):
    initial_state = initial_state or [(0, 0, 0)]
    n = n or len(tiles)
    grid = load_grid(initial_state, tiles)
    initial = save_grid(grid)
    frontier = [initial]
    explored = {initial}
    
    while frontier:
        state = frontier.pop()
        if len(state) == n:
            return state
        grid = load_grid(state, tiles)
        for pos in open_positions(grid, n):
            for (i, j) in possible_tiles(pos, grid, tiles):
                place_tile(pos, i, j, grid, tiles)
                newstate = save_grid(grid)
                del grid[pos]
                if newstate not in explored:
                    explored.add(newstate)
                    frontier.append(newstate)
    print("failure")
    return state


def list_corners(state, labels):
    D = {pos: i for (pos, i, j) in state}
    keys = set(D)
    c = Counter()
    for k in keys:
        for delta in NESW:
            if k + delta in keys:
                c[k] += 1
    corner_keys = [k for (k, v) in c.items() if v == 2]
    return [labels[D[k]] for k in corner_keys]


with open(datafile) as fh:
    datatxt = fh.read()
data = parse_data(datatxt)

labels, tiles = all_tile_edges(data)

endstate = dfs(tiles)

prod = 1
for c in list_corners(endstate, labels):
    prod *= int(c)
part_1 = prod


# Part 2


def build_image(endstate, data):
    tiles = np.array([list(tile_orientations(tile)) for (label, tile) in data])
    image_tiles = np.array([tiles[i, j] for (pos, i, j) in sorted(endstate, key=lambda x: (-x[0].imag, x[0].real))])
    trimmed = image_tiles[:, 1:-1, 1:-1]
    squared = trimmed.reshape((-1, int(math.sqrt(trimmed.shape[0])+0.1)) + trimmed.shape[1:])
    stitched = np.vstack([np.hstack(row) for row in squared])
    return stitched


sea_monster_txt = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
lines = [x for x in sea_monster_txt.split('\n') if x]
sea_monster = np.array([
    [int(x) for x in (line.replace('#', '1').replace(' ', '0'))]
    for line in lines
])
"""
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0]
 [1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 1]
 [0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 0]]
"""


def count_monsters(image, monster=sea_monster):
    return (ndimage.correlate(image, monster, mode='constant') == sea_monster.sum()).sum()


image = build_image(endstate, data)
orients = list(tile_orientations(image))
monster_counts = [count_monsters(x) for x in orients]
monster_image = orients[np.argmax(monster_counts)]
roughness = monster_image.sum() - count_monsters(monster_image) * sea_monster.sum()
part_2 = roughness
