

class Map():
    def __init__(self):
        self.m = []
        self.height = 0
        self.width = -1
        self.robot = None
        self.boxes = set()
        self.wall = set()

    def append(self, row):
        self.width = len(row)*2
        self.m.append(row)
        for (c, ch) in enumerate(row):
            if ch == 'O':
                self.boxes.add((self.height, c*2))
            elif ch == '#':
                self.wall.add((self.height, c*2))
                self.wall.add((self.height, c*2+1))
            elif ch == '@':
                self.robot = (self.height, c*2)
        self.height += 1

    def move_robot(self, d):
        v = {'^': (-1, 0),
             'v': (1, 0),
             '>': (0, 1),
             '<': (0, -1)}[d]
        ny, nx = self.step(self.robot, v)
        if (ny, nx) in self.wall:
            return
        if not self.get_box((ny, nx)):
            # Nothing in the way; robot moves
            self.robot = (ny, nx)
            return

        # Pushing into a box
        boxes_in_path = set(self.boxes_in_path((ny, nx), v))
        if any(self.box_cannot_move(b, v) for b in boxes_in_path):
            # The robot cannot move, because a wall is blocking at least
            # one of the boxes. Since the robot cannot move, none of the boxes
            # move
            return

        # No wall is blocking any of the boxes, so they all move
        for b in boxes_in_path:
            self.move_box(b, v)

    def get_box(self, coords):
        if coords in self.boxes:
            return coords
        if (coords[0], coords[1]-1) in self.boxes:
            return (coords[0], coords[1]-1)

    def boxes_in_path(self, coords, v):
        print(f"boxes_in_path({coords}, {v})")
        b = self.get_box(coords)
        yield self.get_box(b)
        seen = set()
        # When moving in y axis, we could encounter 0, 1 or 2 boxes.
        # When moving in x axis, we could only encounter 0 or 1 box.
        if v[0] != 0:
            # Moving in y axis
            for c in self.box_coords(b):
                next_b = self.get_box(self.step(c, v))
                if next_b:
                    for box in self.boxes_in_path(next_b, v):
                        if box in seen:
                            continue
                        seen.add(box)
                        yield box
        else:
            # Not moving in y axis; must be moving in x axis (else we aren't moving at all)
            assert v[1] == 1 or v[1] == -1
            # We get to the next box by moving 2 steps at a time
            while True:
                b = self.step(self.step(b, v), v)
                if b in self.boxes:
                    yield b
                elif b in self.wall:
                    break


    def box_coords(self, b):
        yield b
        yield (b[0], b[1]+1)

    def box_cannot_move(self, b, v):
        return any(c in self.wall for c in self.box_coords(b))

    def move_box(self, b, v):
        self.boxes.remove(b)
        self.boxes.add(self.step(b, v))

    def step(self, p, v):
        return tuple(c+d for c,d in zip(p, v))

    def gps(self, b):
        y, x = b
        return (y*100 + x)

    def print(self):
        for y in range(self.height):
            x = 0
            while x < self.width:
                if self.robot == (y, x):
                    print('@', end="")
                elif (y, x) in self.boxes:
                    print('[]', end="")
                    x += 1
                elif (y, x) in self.wall:
                    print('#', end="")
                else:
                    print('.', end="")
                x += 1
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



