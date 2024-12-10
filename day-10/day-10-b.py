

with open('input') as input:
    map = [[int(n) for n in r.strip()] for r in input.readlines()]

height = len(map)
width = len(map[0])

# Build a map of the peaks accessible from each cell, starting with 9s
peak_finder = []
for r in range(height):
    pr = []
    peak_finder.append(pr)
    for c in range(width):
        if map[r][c] == 9:
            pr.append(1)
        else:
            pr.append(0)

# Work our way down in height, building the peak_finder
for h in range(8, -1, -1):
    for r in range(height):
        for c in range(width):
            if map[r][c] != h:
                continue
            for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
                if nr < 0 or nc < 0 or nr >= height or nc >= width:
                    continue
                if map[nr][nc] == h+1:
                    peak_finder[r][c] += peak_finder[nr][nc]

# Add up the peaks at each trailhead
score = 0
for r in range(height):
    for c in range(width):
        if map[r][c] == 0:
            score += peak_finder[r][c]

print(score)

