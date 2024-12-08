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
    for (ax, ay), (bx, by) in combinations(locs, 2):
        # 2 antinode locations for each pair,
        #   * projecting from a-b-antinode (b + (b-a))
        #   * projecting from b-a-antinode (a + (a-b))
        x, y = 2*bx - ax, 2*by - ay
        if x >= 0 and x < width and y >= 0 and y < height:
            antinodes.add((x, y))
        x, y = 2*ax - bx, 2*ay - by
        if x >= 0 and x < width and y >= 0 and y < height:
            antinodes.add((x, y))

print(len(antinodes))



