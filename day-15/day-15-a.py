

class Map():
    def __init__(self):
        self.m = []
        self.height = 0
        self.width = -1
        self.robot = None
        self.boxes = set()
        self.wall = set()

    def append(self, row):
        self.width = len(row)
        self.m.append(row)
        for (c, ch) in enumerate(row):
            if ch == 'O':
                self.boxes.add((self.height, c))
            elif ch == '#':
                self.wall.add((self.height, c))
            elif ch == '@':
                self.robot = (self.height, c)
        self.height += 1

    def move_robot(self, d):
        v = {'^': (-1, 0),
             'v': (1, 0),
             '>': (0, 1),
             '<': (0, -1)}[d]
        ny, nx = self.step(self.robot, v)
        if (ny, nx) in self.wall:
            return
        if (ny, nx) not in self.boxes:
            # Nothing in the way; robot moves
            self.robot = (ny, nx)
            return

        # Pushing into a box
        by, bx = ny, nx
        while True:
            by, bx = self.step((by, bx), v)
            if (by, bx) in self.wall:
                # Hit a wall; nothing can move
                return
            if (by, bx) not in self.boxes:
                # Found a space for the boxes to move into
                self.robot = (ny, nx)
                self.boxes.remove(self.robot)
                self.boxes.add((by, bx))
                return

    def step(self, p, v):
        return ([c+d for c,d in zip(p, v)])

    def gps(self, b):
        y, x = b
        return (y*100 + x)

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.robot == (y, x):
                    print('@', end="")
                elif (y, x) in self.boxes:
                    print('O', end="")
                elif (y, x) in self.wall:
                    print('#', end="")
                else:
                    print('.', end="")
            print()
        print()


map = Map()

with open('input') as input:
    # map
    for l in input:
        l = l.strip()
        if not l:
            # End of the map
            break
        map.append(l)

    instructions = "".join(l.strip() for l in input)

map.print()

for i in instructions:
    map.move_robot(i)

map.print()
print(sum(map.gps(b) for b in map.boxes))



