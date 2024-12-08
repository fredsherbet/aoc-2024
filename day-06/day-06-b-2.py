# Collect visited cells in a set, so that we dedup as we go. Walk through
# the path of the guard, until they leave the map

class Grid:
    def __init__(self, rows):

        # Map from old velocity to new velocity, when the guard turns right
        self.right_turn_velocity_map = {
                (-1, 0): ( 0, 1),
                ( 0, 1): ( 1, 0),
                ( 1, 0): ( 0,-1),
                ( 0,-1): (-1, 0),
            }

        self.obstructions = set()

        r = 0
        for row in rows:
            self.width = len(row)
            for c in range(self.width):
                if row[c] == '#':
                    self.obstructions.add((r, c))
                elif row[c] == '^':
                    self.guard_position = (r, c)
                    self.guard_velocity = (-1,0)
            r += 1
        self.height = r

        print(f"Grid dimensions: {self.height}x{self.width}")

        # Save state, to be able to restore it
        self.original_guard_position = self.guard_position
        self.original_guard_velocity = self.guard_velocity

    def reset(self):
        self.guard_position = self.original_guard_position
        self.guard_velocity = self.original_guard_velocity

    @property
    def guard_is_on_map(self):
        x = self.guard_position[0]
        y = self.guard_position[1]
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def walk_guard_forward_until_collision(self):
        visited = set([self.guard_position])
        while self.guard_is_on_map:
            #print(f"Guard position: {self.guard_position}; velocity {self.guard_velocity}")
            self.step_guard_forward()
            if self.guard_has_collided():
                self.step_guard_backward()
                #print(visited)
                return visited
            visited.add(self.guard_position)
        #print(visited)
        return visited

    def step_guard_forward(self):
        self.guard_position = tuple(c + v for c, v in zip(self.guard_position, self.guard_velocity))

    def step_guard_backward(self):
        self.guard_position = tuple(c - v for c, v in zip(self.guard_position, self.guard_velocity))

    def guard_has_collided(self):
        return self.guard_position in self.obstructions

    def turn_guard_right(self):
        self.guard_velocity = self.right_turn_velocity_map[self.guard_velocity]

    def creates_loop(self, r, c):
        self.reset()
        #print(len(self.obstructions))
        assert (r, c) not in self.obstructions
        self.obstructions.add((r, c))
        collided_at = set()
        while self.guard_is_on_map:
            self.walk_guard_forward_until_collision()
            guard_state = (self.guard_velocity, self.guard_position)
            if guard_state in collided_at:
                # Everything that's happened before will happen again
                #print(f"with extra obstruction at {(r, c)}, Looped at {guard_state}, with collisions {collided_at}")
                self.obstructions.remove((r, c))
                return True
            collided_at.add(guard_state)
            self.turn_guard_right()
        # Walked off the map. No loop found
        self.obstructions.remove((r, c))
        return False


if __name__ == '__main__':
    with open('input') as input:
        grid = Grid(l.strip() for l in input.readlines())

    visited = set()
    while grid.guard_is_on_map:
        visited |= grid.walk_guard_forward_until_collision()
        grid.turn_guard_right()

    #print(f"ALL VISITED: {sorted(visited)}")
    print(len(visited))

    # Every visited cell is a candidate for putting an obstruction. Which of them cause a loop?
    print(sum(1 for r, c in visited if grid.creates_loop(r, c)))
