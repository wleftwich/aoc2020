with open(datafile) as fh:
    empty_chart_text = fh.read()
    

def text2chart(txt):
    D = {}
    for i, row in enumerate(txt.split()):
        for  j, val in enumerate(row):
            D[complex(i, j)] = val
    return D

# Part 1

def changeseat(chart, seatkey):
    seat = chart[seatkey]
    if seat == '.':
        return seat
    occupied = 0
    for drxn in [-1, -1+1j, 1j, 1+1j, 1, 1-1j, -1j, -1-1j]:
        if chart.get(seatkey + drxn) == '#':
            occupied += 1
    if seat == 'L' and occupied == 0:
        return '#'
    if seat == '#' and occupied > 3:
        return 'L'
    return seat


def nextchart(chart):
    return {key: changeseat(chart, key) for key in chart}


def run_till_stabilized(chart):
    nc = nextchart(chart)
    while nc != chart:
        chart, nc = nc, nextchart(nc)
    return nc


def count_occupied(chart):
    return sum(v == '#' for v in chart.values())


empty_chart = text2chart(empty_chart_text)
stabilized = run_till_stabilized(empty_chart)
part_1 = count_occupied(stabilized)

# Part 2


def changeseat2(chart, seatkey):
    seat = chart[seatkey]
    if seat == '.':
        return seat
    occupied = 0
    for drxn in [-1, -1+1j, 1j, 1+1j, 1, 1-1j, -1j, -1-1j]:
        neighbor = '.'
        scale = 0
        while neighbor == '.':
            scale += 1
            neighbor = chart.get((scale * drxn) + seatkey)
        if neighbor == '#':
            occupied += 1
    if seat == 'L' and occupied == 0:
        return '#'
    if seat == '#' and occupied > 4:
        return 'L'
    return seat


def nextchart2(chart):
    return {key: changeseat2(chart, key) for key in chart}


def run_till_stabilized2(chart):
    nc = nextchart2(chart)
    while nc != chart:
        chart, nc = nc, nextchart2(nc)
    return nc


stabilized2 = run_till_stabilized2(empty_chart)
part_2 = count_occupied(stabilized2)
