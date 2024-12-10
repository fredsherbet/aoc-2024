import sys
from collections import deque
from bisect import insort

with open('input') as input:
    diskmap = [int(n) for n in input.read().strip()]

assert len(diskmap)%2 == 1, "Expected odd number in diskmap"

disk = []
def insert_file(id, size, pos):
    assert len(disk) > pos + size, f"Disk too small for file {id}, size {size}, at {pos}"
    for block in range(size):
        disk[pos + offset] = id

block_pos = 0
left_file_pos = 0
left_file_id = 0
right_file_pos = len(diskmap)-1

# Keep track of where we have space available
space_map = []
for _ in range(10):
    space_map.append([])

# File map is the files listed (in order of ID) with their position and size (Everything we need to calculate the checksum)
file_map = []

block_pos = 0
file_next = True
for size in diskmap:
    if file_next:
        file_map.append((block_pos, size))
    else:
        space_map[size].append(block_pos)
    block_pos += size
    file_next = not file_next

print("Space map:")
for size in range(10):
    print(f"{size}: {space_map[size]}")

# Work through the files, in reverse, either moving or leaving in place.
# We'll update the file_pos in the file map, then use that to calculate the checksum.
for id in range(len(file_map)-1, -1, -1):
    pos, size = file_map[id]
    leftmost_space_pos = float('inf')
    for space in range(size, 10):
        if space_map[space]:
            space_pos = space_map[space][0]
            if leftmost_space_pos > space_pos:
                leftmost_space_pos = space_pos
                leftmost_space = space
            if space_pos > pos:
                # No useful spaces of this size (they're all to the right)
                space_map[space] = []

    if leftmost_space_pos < pos:
        space_map[leftmost_space].pop(0)
        file_map[id] = (leftmost_space_pos, size)
        gap = leftmost_space - size
        if gap:
            insort(space_map[gap], leftmost_space_pos+size)

checksum = 0
for id in range(len(file_map)):
    pos, size = file_map[id]
    print(f"File {id} at {pos}, size {size}")
    for p in range(pos, pos+size):
        checksum += id*p

print(checksum)
sys.exit(0)




max_space_available = 9

# Working from the right, hunt for space available for the file
space_needed = diskmap[right_file_pos]
for space in range(space_needed, 10):
    if space_map[space]:
        print(f"Found a spot for {right_file_pos}")
        insert_file(right_file_pos//2, space_needed, space_map[space].popleft())
        break
else:
    # Did not find a space; add more files from left until we find a space
    pass







# Calculate checksum
checksum = 0









# Files can only be up to 9 digits long. Let's use an array for files we've
# found that are looking for space, indexed on the space they need.
# Then, when we find space, we can hunt for the longest candidate that fits.
files_looking_for_space = []
for _ in range(10):
    files_looking_for_space.append(deque())

while left_file_pos < right_file_pos:
    # Read in next file
    for _ in range(diskmap[left_file_pos]):
        checksum += block_pos * left_file_id
        block_pos += 1

    left_file_pos += 1
    space_available = diskmap[left_file_pos]
    left_file_pos += 1

    for space in range(space_available, 0, -1):
        if files_looking_for_space[space]:

            break
    else:
        # Don't (yet) have a file to put in
        while diskmap[right_file_pos] > space_available:
            files_looking_for_space[diskmap[right_file_pos]].append(right_file_pos//2)
            right_file_pos -= 2


    # Fill in next space
    for _ in range(diskmap[left_file_pos]):
        if right_file_size <= 0:
            right_file_id -= 1
            right_file_pos -= 2
            right_file_size = diskmap[right_file_pos]
        if left_file_pos >= right_file_pos:
            break
        checksum += block_pos * right_file_id
        right_file_size -= 1
        block_pos += 1
    left_file_pos += 1
    left_file_id += 1

print(f"""Exited loop with following state:
      left_file_pos: {left_file_pos}
      right_file_pos: {right_file_pos}
      left_file_id: {left_file_id}
      right_file_id: {right_file_id}
      right_file_size: {right_file_size}
      block_pos: {block_pos}""")

# Finish reading in the left file (which has been partially moved to the space before it)
if left_file_id == right_file_id:
    print(f"Finish adding in last file")
    for _ in range(right_file_size):
        checksum += block_pos * left_file_id
        block_pos += 1

print(checksum)
