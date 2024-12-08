from itertools import combinations
from collections import defaultdict

antinodes = set()
nodes = defaultdict(set)


# Load the grid
with open('input') as input:
    grid = [r.strip() for r in input.readlines()]
height = len(grid)
width = len(grid[0])

# Read in the node locations
for y in range(height):
    row = grid[y]
    for x in range(width):
        cell = row[x]
        if cell != '.':
            nodes[cell].add((x, y))

# Calculate the antinode locations
for freq, locs in nodes.items():
    for n1, n2 in combinations(locs, 2):
        # 2 antinode locations for each pair,
        #   * projecting from a-b-antinode (b + n(b-a))
        #   * projecting from b-a-antinode (a + n(a-b))
        for (ax, ay), (bx, by) in [(n1, n2), (n2, n1)]:
            n = 0
            while True:
                x, y = bx + n*(bx - ax), by + n*(by - ay)
                if x < 0 or x >= width or y < 0 or y >= height:
                    # Left the map
                    break
                antinodes.add((x, y))
                n += 1

print(len(antinodes))



