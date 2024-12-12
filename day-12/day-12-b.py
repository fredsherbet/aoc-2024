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
    region = set()
    while q:
        (r, c) = q.popleft()
        if map[r][c] == id:
            region.add((r, c))
            q.extend([(y, x) for y,x in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
                      if y >= 0 and y < len(map) and x >= 0 and x < len(map[0])])
            map[r][c] = '.'

    east_fences = set()
    north_fences = set()
    for y, x in region:
        if (y-1, x) not in region:
            # Looking North
            east_fences.add((y, x, 'n'))
        if (y+1, x) not in region:
            # Looking South
            east_fences.add((y+1, x, 's'))
        if (y, x-1) not in region:
            # Looking East
            north_fences.add((y, x, 'e'))
        if (y, x+1) not in region:
            # Looking West
            north_fences.add((y, x+1, 'w'))

    # Need to squash the fence set; we'll keep one fence from each edge
    print(f"North before: {sorted(north_fences)}")
    all = north_fences.copy()
    for r,c,d in sorted(all):
        if (r+1, c, d) in all:
            print(f"north_fences.remove(({r}, {c}))")
            north_fences.remove((r, c, d))
    print(f"North after: {sorted(north_fences)}")
    print(f"East before: {sorted(east_fences)}")
    all = east_fences.copy()
    for r,c,d in sorted(all):
        if (r, c+1, d) in sorted(all):
            print(f"east_fences.remove(({r}, {c}))")
            east_fences.remove((r, c, d))
    print(f"East after: {sorted(east_fences)}")

    # Fencing needed is product of area and perimeta, because modern economics
    print(f"Region of {id} has cost {len(region)}*({len(north_fences)}+{len(east_fences)}) = {len(region) * (len(north_fences) + len(east_fences))}")
    return len(region) * (len(north_fences) + len(east_fences))


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



