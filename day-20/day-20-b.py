from collections import Counter,deque
import sys

class Map:
    def __init__(self):
        self.map = []
        self.steps = 0
        self.start = None
        self.end = None
        self.p = None

    def find_shortcuts(self):
        #print(f"Find shortcuts landing at {self.p}")
        # We can shortcut to self.p from anywhere that's on the route we've
        # been so far, and is within a radius of 20 steps
        for l,d in self.within(20):
            if self.at(l) not in ['#', '.']:
                saving = self.at(self.p) - self.at(l) - d
                if saving > 0:
                    yield saving

    def within(self, steps):
        seen = set()
        q = deque()
        q.extend((l, 1) for l in self.next_to(self.p))
        while q:
            l, d = q.popleft()
            if d > steps:
                continue
            if l in seen:
                continue
            seen.add(l)
            yield (l, d)
            q.extend((l, d+1) for l in self.next_to(l))


    def print(self, overrides):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if (y,x) in overrides and self.at((y,x)) != '#':
                    print(f"{self.map[y][x]:2},{overrides[(y,x)]:2} |", end="")
                else:
                    print(f"{self.map[y][x]:2}    |", end="")
            print()

    def next_to(self, p):
        y, x = p
        if y > 1: yield (y-1,x)
        if y < len(self.map)-2: yield (y+1,x)
        if x > 1: yield (y,x-1)
        if x < len(self.map[0])-2: yield (y,x+1)

    def at(self, p):
        return self.map[p[0]][p[1]]

    def set(self, p, val):
        self.map[p[0]][p[1]] = val

    def at_end(self):
        return self.p == self.end

    def step(self):
        for l in self.next_to(self.p):
            if self.at(l) == '.':
                self.steps += 1
                self.set(l, self.steps)
                self.p = l
                return

    def append(self, row):
        self.map.append(row)
        if 'S' in l:
            self.start = (len(self.map)-1, l.find('S'))
            self.set(self.start, 0)
            self.p = self.start
        if 'E' in l:
            self.end = (len(self.map)-1, l.find('E'))
            self.set(self.end, '.')


map = Map()

with open('input') as input:
    for l in input:
        l = l.strip()
        map.append(list(l))

print(f"Race from {map.start} to {map.end}")
shortcuts = []
while not map.at_end():
    #print(f"Step {map.steps} from {p}")
    shortcuts.extend(map.find_shortcuts())
    map.step()

# And also shortcuts straight to the end
shortcuts.extend(map.find_shortcuts())

for l, count in sorted(Counter(shortcuts).items(), key=lambda x: x[0]):
    print(f"{count} can save {l}")
print(sum(1 for s in shortcuts if s >= 100))

