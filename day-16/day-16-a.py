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
        self.m.append(row)
        for (c, ch) in enumerate(row):
            if ch == '#':
                self.wall.add((self.height, c))
            elif ch == 'S':
                self.start = (self.height, c)
            elif ch == 'E':
                self.end = (self.height, c)
        self.height += 1

map = Map()

with open('input') as input:
    for l in input:
        l = l.strip()
        map.append(l)

q = deque()
visited = []
q.append((map.start, 'E', 0, 0))
best_score = 999999999999

while q:
    pos, dir, v_ix, score = q.pop()
    visited = visited[:v_ix]
    if pos in visited:
        continue
    if score >= best_score:
        continue
    if pos == map.end:
        best_score = score
        print(f'Found new best score {score}')
        continue
    #print(f"Visiting {pos} {dir}, @{score}")
    visited.append(pos)
    if map.m[pos[0]][pos[1]+1] != '#':
        q.append(((pos[0], pos[1]+1), 'E', v_ix+1, score + ( 1 if dir == 'E' else 1001)))
    if map.m[pos[0]][pos[1]-1] != '#':
        q.append(((pos[0], pos[1]-1), 'W', v_ix+1, score + ( 1 if dir == 'W' else 1001)))
    if map.m[pos[0]+1][pos[1]] != '#':
        q.append(((pos[0]+1, pos[1]), 'S', v_ix+1, score + ( 1 if dir == 'S' else 1001)))
    if map.m[pos[0]-1][pos[1]] != '#':
        q.append(((pos[0]-1, pos[1]), 'N', v_ix+1, score + ( 1 if dir == 'N' else 1001)))

print(best_score)

