# Collect visited cells in a set, so that we dedup as we go. Walk through
# the path of the guard, until they leave the map
from collections import deque

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
        self.candidates = set()

        # Each time we turn the guard, we'll rotate this list, and add places
        # the guard visits to the set at the front of the list.
        # Say, the guard is moving up:
        #   * the front set is the places visited while moving up;
        #   * second moving right;
        #   * third is moving down;
        #   * fourth is moving left.
        #
        # To see if we could create a loop, when the guard visits a place in the
        # second set, then an obstruction in front of the guard would create a loop.
        self.visited_in_direction = deque([set(), set(), set(), set()])

        r = 0
        for row in rows:
            self.width = len(row)
            for c in range(self.width):
                if row[c] == '#':
                    self.obstructions.add((r, c))
                elif row[c] == '^':
                    self.guard_position = (r, c)
                    self.guard_velocity = (-1,0)
                    self.visited_in_direction[0].add(self.guard_position)
            r += 1
        self.height = r

        print(f"Grid dimensions: {self.height}x{self.width}")

    @property
    def guard_is_on_map(self):
        x = self.guard_position[0]
        y = self.guard_position[1]
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def walk_guard_forward_until_collision(self):
        while self.guard_is_on_map:
            #print(f"Guard position: {self.guard_position}; velocity {self.guard_velocity}")
            if self.position_in_front_of_guard in self.obstructions:
                return
            self.step_guard_forward()
            self.visited_in_direction[0].add(self.guard_position)
            if self.guard_position in self.visited_in_direction[1]:
                print(f"Found candidate: {self.position_in_front_of_guard} while moving {self.guard_velocity}")
                self.candidates.add(self.position_in_front_of_guard)

    def step_guard_forward(self):
        self.guard_position = self.position_in_front_of_guard
        assert self.guard_position not in self.obstructions

    @property
    def position_in_front_of_guard(self):
        return tuple(c + v for c, v in zip(self.guard_position, self.guard_velocity))

    def turn_guard_right(self):
        self.guard_velocity = self.right_turn_velocity_map[self.guard_velocity]
        self.visited_in_direction.rotate(-1)
        self.visited_in_direction[0].add(self.guard_position)


if __name__ == '__main__':
    with open('input') as input:
        grid = Grid(l.strip() for l in input.readlines())

    while grid.guard_is_on_map:
        grid.walk_guard_forward_until_collision()
        grid.turn_guard_right()

    print(len(grid.candidates))
