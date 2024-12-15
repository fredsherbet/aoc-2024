

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
        if c >= 0
            self.robot = (self.height, c)
        for (c, ch) in enumerate(row):
            if ch == 'O':
                self.boxes.add(self.height, c)

    def move_robot(self, d):
        v = {'^': (-1, 0),
             'v': (1, 0),
             '>': (0, 1),
             '<': (0, -1)}[d]
        #TODO

    def gps(self, b):
        y, x = b
        #TODO


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

print(sum(map.gps(b) for b in map.boxes))



