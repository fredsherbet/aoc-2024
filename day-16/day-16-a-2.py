from collections import deque

class Map:
    def __init__(self):
        self.m = []
        self.height = 0
        self.width = -1
        self.wall = set()
        self.start = None
        self.end = None

    def append(self, row):
        self.width = len(row)
        self.m.append([])
        for (c, ch) in enumerate(row):
            if ch == '#':
                self.wall.add((self.height, c))
                self.m[-1].append('#')
            elif ch == 'S':
                self.start = (self.height, c)
                self.m[-1].append(999999999)
            elif ch == 'E':
                self.end = (self.height, c)
                self.m[-1].append(9999999999)
            else:
                self.m[-1].append(9999999999)
        self.height += 1

    def at(self, pos):
        y,x = pos
        return self.m[y][x]

    def set(self, pos, val):
        y,x = pos
        self.m[y][x] = val

map = Map()

with open('input') as input:
    for l in input:
        l = l.strip()
        map.append(l)

# Do a BF walk through the maze, marking the cheapest way to get to each cell

q = deque()
q.append((map.start, 'E', 0))

while q:
    pos, dir, score = q.popleft()
    if map.at(pos) == '#':
        continue
    if map.at(pos) <= score:
        # Already found a better route to here
        continue
    map.set(pos, score)

    for y, x, d in [(pos[0], pos[1]+1, 'E'),
                    (pos[0], pos[1]-1, 'W'),
                    (pos[0]+1, pos[1], 'S'),
                    (pos[0]-1, pos[1], 'N')]:
        q.append(((y, x), d, score + (1 if dir == d else 1001)))

print(map.at(map.end))

