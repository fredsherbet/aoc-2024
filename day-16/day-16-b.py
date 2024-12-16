from collections import deque

class Map:
    def __init__(self):
        self.from_start = []
        self.to_end = []
        self.height = 0
        self.start = None
        self.end = None

    def append(self, row):
        self.from_start.append([])
        self.to_end.append([])
        for (c, ch) in enumerate(row):
            if ch == '#':
                self.from_start[-1].append('#')
                self.to_end[-1].append('#')
                continue
            self.from_start[-1].append(99999999999)
            self.to_end[-1].append(99999999999)
            if ch == 'S':
                self.start = (self.height, c)
            elif ch == 'E':
                self.end = (self.height, c)
        self.height += 1
        self.width = len(row)

    def at(self, pos):
        y,x = pos
        return self.from_start[y][x]

    @property
    def all_coords(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (y, x)

    def on_route(self, y, x):
        if self.from_start[y][x] == '#': return False
        score = self.from_start[y][x] + self.to_end[y][x]
        target = self.at(self.end)
        return score == target or score + 1000 == target


    def print(self):
        for y in range(self.height):
            x = 0
            while x < self.width:
                if self.from_start[y][x] == "#":
                    print('#', end="")
                elif self.on_route(y, x):
                    print('O', end="")
                else:
                    print('.', end="")
                x += 1
            print()
        print()


map = Map()

with open('input') as input:
    for l in input:
        l = l.strip()
        map.append(l)

# Do a BF walk through the maze, marking the cheapest way to get to each cell
# Then, do the same backwards, for cheapest score from each cell to end
# Then, any cell that sums forward/backward equal to the cheapest path, is on
# a cheapest path.
def do_bfs(start, map, dirs):
    y, x = start
    q = deque()
    q.append((y, x, dirs, 0))
    while q:
        y, x, dirs, score = q.popleft()
        if y == 13 and x == 1:
            print(f"{y}, {x}, {dirs}, {score}")
        cell = map[y][x]
        if cell == '#' or cell <= score:
            continue

        map[y][x] = score

        for y, x, d in [(y, x+1, 'E'),
                        (y, x-1, 'W'),
                        (y+1, x, 'S'),
                        (y-1, x, 'N')]:
            q.append((y, x, d, score + (1 if d in dirs else 1001)))


# From start
do_bfs(map.start, map.from_start, 'E')

# To end
do_bfs(map.end, map.to_end, 'NEWS')

map.print()

print(f"{map.end}: {map.at(map.end)} + {map.to_end[map.end[0]][map.end[1]]}")
print(f"{map.start}: {map.at(map.start)} + {map.to_end[map.start[0]][map.start[1]]}")
print('Seats on route')
print(sum(1 for y,x in map.all_coords if map.on_route(y, x)))

