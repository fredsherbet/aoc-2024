

class Map():
    def __init__(self):
        self.m = []
        self.height = -1
        self.width = -1
        self.robot = None
        self.boxes = set()

    def append(self, row):
        self.width = len(row)
        self.height += 1
        self.m.append(row)
        c = row.find('@')
        if c >= 0:
            self.robot = (self.height, c)
        for (c, ch) in enumerate(row):
            if ch == 'O':
                self.boxes.add((self.height, c))

    def move_robot(self, d):
        v = {'^': (-1, 0),
             'v': (1, 0),
             '>': (0, 1),
             '<': (0, -1)}[d]
        ny, nx = self.step(self.robot, v)
        if self.in_bounds(ny, nx) and (ny, nx) not in self.boxes:
            self.robot = (ny, nx)
            return

        # Moving boxes!
        oy, ox = ny, nx
        while self.in_bounds(oy, ox):
            oy, ox = self.step((oy, ox), v)
            if self.in_bounds(oy, ox) and (oy, ox) not in self.boxes:
                self.robot = (ny, nx)
                self.boxes.remove(self.robot)
                self.boxes.add((oy, ox))
                return

        # Cannot move boxes; nothing moves
        return

    def step(self, p, v):
        return ([c+d for c,d in zip(p, v)])

    def in_bounds(self, y, x):
        return y > 0 and y < self.height-1 and x > 0 and x < self.width-1

    def gps(self, b):
        y, x = b
        return (y*100 * x)

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.robot == (y, x):
                    print('@', end="")
                elif (y, x) in self.boxes:
                    print('O', end="")
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

for i in instructions:
    map.move_robot(i)

map.print()
print(sum(map.gps(b) for b in map.boxes))



