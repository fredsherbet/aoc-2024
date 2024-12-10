
with open('input') as input:
    diskmap = [int(n) for n in input.read().strip()]

assert len(diskmap)%2 == 1, "Expected odd number in diskmap"

checksum = 0
block_pos = 0
left_file_pos = 0
left_file_id = 0
right_file_pos = len(diskmap)-1
right_file_size = diskmap[right_file_pos]
right_file_id = right_file_pos // 2

while left_file_pos < right_file_pos:
    # Read in next file
    for _ in range(diskmap[left_file_pos]):
        checksum += block_pos * left_file_id
        block_pos += 1

    left_file_pos += 1
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
