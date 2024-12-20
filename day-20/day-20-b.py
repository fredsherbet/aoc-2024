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
        q = deque()
        cheats_allowed = 20
        q.extend((l, cheats_allowed-1) for l in self.next_to(self.p) if self.at(l) == '#')
        visited = {self.p: cheats_allowed}
        shortcuts_from = set()
        while q:
            l, available_steps = q.popleft()
            if available_steps < 0:
                continue
            if l in visited and visited[l] > available_steps:
                # Already explored better routes from here
                continue
            visited[l] = available_steps
            q.extend((c, available_steps-1) for c in self.next_to(l))
            if self.at(l) == '#':
                continue
            if self.at(l) == '.':
                # This is a place we've not stepped to; we'll find this
                # shortcut when we step here, and look back.
                continue
            shortcuts_from.add(l)

        #self.print({})
        #self.print(visited)
        #print()
        #sys.exit(0)
        for l in shortcuts_from:
            saving = self.at(self.p) - self.at(l) - (cheats_allowed-visited[l])
            if saving > 0:
                #print(f"Found Shortcut from {l}({self.at(l)}) to {self.p}({self.at(self.p)}) saves {saving}")
                yield saving

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

