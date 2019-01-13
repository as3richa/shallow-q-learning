from world import EMPTY, OBSTACLE, GOAL

_DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))

_SHIP_CHARACTERS = ('▲', '▶', '▼', '◀')

_WORLD_CHARACTERS = {
  EMPTY: ' ',
  OBSTACLE: '*',
  GOAL: '$'
}

class State:
  def __init__(self, world, x, y, direction):
    self.world = world
    self.x = x
    self.y = y
    self.direction = direction

    out_of_bounds = (x < 0 or y < 0 or x >= self.world.size or y >= self.world.size)
    self.crashed = (out_of_bounds or world[x][y] == OBSTACLE)
    self.goal_achieved = (not out_of_bounds and world[x][y] == GOAL)

    self.done = (self.crashed or self.goal_achieved)

  def clockwise(self):
    assert not self.done
    return State(self.world, self.x, self.y, (self.direction + 1) % 4)

  def counterclockwise(self):
    assert not self.done
    return State(self.world, self.x, self.y, (self.direction + 3) % 4)

  def forward(self):
    assert not self.done
    xx = self.x + _DELTAS[self.direction][0]
    yy = self.y + _DELTAS[self.direction][1]
    return State(self.world, xx, yy, self.direction)

  def render(self):
    string = '┌' + ('─' * self.world.size) + '┐\n'

    for y in range(self.world.size):
      string += '│'

      for x in range(self.world.size):
        if self.world[x][y] == EMPTY and (x, y) == (self.x, self.y):
          string += _SHIP_CHARACTERS[self.direction]
        else:
          string += _WORLD_CHARACTERS[self.world[x][y]]

      string += '│\n'

    string += '└' + ('─' * self.world.size) + '┘'

    return string
