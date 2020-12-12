with open(datafile) as fh:
    data = [y for y in (x.strip() for x in fh) if y]

# Part 1

class Navigate:
    
    def N(self, x, p, h):
        return p + x * 1j, h
    
    def S(self, x, p, h):
        return p + x * -1j, h
    
    def E(self, x, p, h):
        return p + x, h
    
    def W(self, x, p, h):
        return p + x * -1, h
    
    def L(self, x, p, h):
        return p, h * pow(1j, (x % 360) // 90)

    def R(self, x, p, h):
        return p, h * pow(-1j, (x % 360) // 90)
    
    def F(self, x, p, h):
        return p + x * h, h
    
    def __call__(self, cmd, p, h):
        fun, arg = cmd[0], cmd[1:]
        return getattr(self, fun)(int(arg), p, h)

    
navigate = Navigate()        
position, heading = 0, 1
for command in data:
    position, heading = navigate(command, position, heading)
part_1 = abs(position.real) + abs(position.imag)


# Part 2

class WaypointNavigate(Navigate):
    
    def N(self, x, p, h):
        return p, h + x * 1j
    
    def S(self, x, p, h):
        return p, h + x * -1j
    
    def E(self, x, p, h):
        return p, h + x
    
    def W(self, x, p, h):
        return p, h + x * -1
    

wpnavigate = WaypointNavigate()    
position, waypoint = 0, 10+1j
for command in data:
    position, waypoint = wpnavigate(command, position, waypoint)
part_2 = abs(position.real) + abs(position.imag)
