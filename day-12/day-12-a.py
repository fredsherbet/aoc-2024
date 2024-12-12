from collections import deque

# Union-find, to build up our set of regions
# As we go, we can keep track of the area and perimeta; they're additive. Push
# the sum to the parent of the region, so that we don't need to walk each region
# summing up at the end

# Simpler option! Walk each region we discover, destroying it, so that as we
# then continue scanning the map, we know when we find another region that it's
# new.

def walk_region(map, row, col):
    id = map[row][col]
    q = deque()
    q.append((row, col))
    area = 0
    perimeta = 0
    in_region = set()
    while q:
        (r, c) = q.popleft()
        if map[r][c] == id:
            in_region.add((r, c))
            neighbours = [(y, x) for y,x in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
                          if y >= 0 and y < len(map) and x >= 0 and x < len(map[0])]
            area += 1
            perimeta += sum(1 for y,x in neighbours if map[y][x] != id and (y, x) not in in_region)
            perimeta += 4 - len(neighbours)
            q.extend(neighbours)
            map[r][c] = '.'

    # Fencing needed is product of area and perimeta, because modern economics
    print(f"Region of {id} has cost {area}*{perimeta} = {area*perimeta}")
    return area * perimeta


with open('input') as input:
    map = [list(row.strip()) for row in input.readlines()]

h = len(map)
w = len(map[0])

fencing_needed = 0

for r in range(h):
    for c in range (w):
        if map[r][c] != '.':
            fencing_needed += walk_region(map, r, c)

print(fencing_needed)



