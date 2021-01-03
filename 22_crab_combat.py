from collections import deque


class RecursiveCombatGame:
    
    def __init__(self, d1, d2, boredom_limit=1_000_000):
        self.d1 = deque(d1)
        self.d2 = deque(d2)
        self.boredom_limit = boredom_limit
        self.visited = set()
        
    def cyclecheck(self):
        key = (tuple(self.d1), tuple(self.d2))
        if key in self.visited:
            return True
        self.visited.add(key)
    
    def trick(self):
        if self.cyclecheck():
            return 'p1'
        d1, d2 = self.d1, self.d2
        c1, c2 = d1.popleft(), d2.popleft()
        if c1 <= len(d1) and c2 <= len(d2):
            self.subgame = RecursiveCombatGame(list(d1)[:c1], list(d2)[:c2])
            winner = self.subgame.play()
        else:
            if c1 > c2:
                winner = 'p1'
            elif c2 > c1:
                winner = 'p2'
            else:
                raise ValueError("can't happen")
        if winner == 'p1':
            d1.append(c1)
            d1.append(c2)
        else:
            d2.append(c2)
            d2.append(c1)
        if not (d1 and d2):
            return winner
    
    def play(self):
        for _ in range(self.boredom_limit):
            winner = self.trick()
            if winner:
                return winner
        else:
            raise BoredomError


def BoredomError(Exception):
    pass
    
    
