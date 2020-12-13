import functools
import itertools
import operator

with open(datafile) as fh:
    datatext = fh.read()

arrival_text, buses_text = datatext.split()

# Part 1

arrival_time = int(arrival_text)
buses = [int(x) for x in buses_text.split(',') if x.isdigit()]

def waiting_time(bus, start_time):
    return bus - (start_time % bus)

def next_bus(arrival_time, buses):
    busit = iter(buses)
    nextbus = next(busit)
    minwait = waiting_time(nextbus, arrival_time)
    for bus in busit:
        wait = waiting_time(bus, arrival_time)
        if wait < minwait:
            minwait = wait
            nextbus = bus
    return nextbus * minwait
    
part_1 = next_bus(arrival_time, buses)

# Part 2

def parse_bustext(txt):
    return [(i, int(bus)) for (i, bus) in enumerate(txt.split(',')) if bus.isdigit()]

def align_schedule(sched):
    buses = []
    start = 1
    for (offset, bus) in sched:
        s1 = itertools.count(start, functools.reduce(operator.mul, buses, 1))
        s2 = (x for x in s1 if not (x + offset) % bus)
        start = next(s2)
        buses.append(bus)
    return start

part_2 = align_schedule(parse_bustext(buses_text))

