from collections import deque

class Map:
    def __init__(self):
        self.width = 7
        self.height = 7
        self.blocks = set()
        self.steps = None

    def add_block(self, y, x):
        self.blocks.add((y, x))

    def shortest_route(self, fy, fx, ty, tx):
        self.do_bfs((fy, fx))
        return self.steps[ty][tx]


    def do_bfs(self, start):
        y, x = start
        self.steps = []
        for r in range(self.height):
            self.steps.append([])
            for c in range(self.width):
                self.steps[-1].append(999999999)

        q = deque()
        q.append((y, x, 0))
        while q:
            y, x, score = q.popleft()
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                # Cannot step outside the map
                continue
            if (y, x) in self.blocks:
                # Cannot step here
                continue
            if self.steps[y][x] <= score:
                # Already found a better route to here
                continue

            self.steps[y][x] = score

            for y, x in [(y, x+1),
                         (y, x-1),
                         (y+1, x),
                         (y-1, x)]:
                q.append((y, x, score + 1))

    def print(self):
        for row in self.steps:
            for s in row:
                print(f"{s if s <99999 else '##':2} ", end="")
            print()
        print()


map = Map()
with open('input') as input:
    count = 0
    for l in input:
        x, y = l.strip().split(',')
        map.add_block(int(y), int(x))
        count += 1
        if count >= 12:
            break

shortest_route = map.shortest_route(0,0, 6,6)
map.print()
print(shortest_route)

