from collections import Counter

def find_shortcuts(map, p):
    y, x = p
    for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if in_direction(map, p, direction, 1) == '#':
            shortcut_to = in_direction(map, p, direction, 2)
            if shortcut_to == '#' or shortcut_to == '.':
                continue
            #print(f"Shortcut found from {p} to {shortcut_to}")
            yield map[y][x] - shortcut_to - 2

def in_direction(map, f, d, count):
    y = f[0]
    x = f[1]
    for _ in range(count):
        y += d[0]
        x += d[1]
    if 0 > y or y >= len(map) or 0 > x or x >= len(map[0]):
        return '#'
    return map[y][x]


def step(map, p, steps):
    y, x = p
    for r, c in [(y+1,x), (y-1,x), (y,x+1), (y,x-1)]:
        if map[r][c] == '.':
            map[r][c] = steps
            return (r, c)

map = []

with open('input') as input:
    row = 0
    for l in input:
        l = l.strip()
        map.append(list(l))
        if 'S' in l:
            start = (row, l.find('S'))
        if 'E' in l:
            end = (row, l.find('E'))
        row += 1

print(f"Race from {start} to {end}")
p = start
shortcuts = []
steps = 0
map[start[0]][start[1]] = 0
map[end[0]][end[1]] = '.'
while p != end:
    steps += 1
    #print(f"Step {steps} from {p}")
    shortcuts.extend(find_shortcuts(map, p))
    p = step(map, p, steps)

# And also shortcuts straight to the end
shortcuts.extend(find_shortcuts(map, p))

for l, count in sorted(Counter(shortcuts).items(), key=lambda x: x[0]):
    print(f"{l}: {count}")
print(sum(1 for s in shortcuts if s >= 100))

