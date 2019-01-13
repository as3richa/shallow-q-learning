from random import randrange
from collections import deque

EMPTY, OBSTACLE, GOAL = range(3)

_DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))

class World:
  def __init__(self, size):
    self.size = size

    while True:
      self._grid = [[EMPTY for y in range(self.size)] for x in range(self.size)]

      gx, gy = self._random_point()
      self._grid[gx][gy] = GOAL

      for i in range(randrange(self.size**2 // 3)):
        ax, ay = self._random_point()

        if (ax, ay) == (gx, gy):
          continue

        self._grid[ax][ay] = OBSTACLE

      if self._solvable(gx, gy):
        break

    self.empty_cells = []

    for x in range(self.size):
      for y in range(self.size):
        if self._grid[x][y] == EMPTY:
          self.empty_cells.append((x, y))

  def __getitem__(self, x):
    return self._grid[x]

  def _random_point(self):
    return (randrange(self.size), randrange(self.size))

  def _solvable(self, gx, gy):
    reachable = [[False for y in range(self.size)] for x in range(self.size)]

    queue = deque()

    queue.append((gx, gy))

    while len(queue) > 0:
      x, y = queue.popleft()

      for delta in _DELTAS:
        xx = x + delta[0]
        yy = y + delta[1]

        in_bounds = (xx >= 0 and yy >= 0 and xx < self.size and yy < self.size)

        if in_bounds and self._grid[xx][yy] == EMPTY and not reachable[xx][yy]:
          reachable[xx][yy] = True
          queue.append((xx, yy))

    for x in range(self.size):
      for y in range(self.size):
        if self._grid[x][y] == EMPTY and not reachable[x][y]:
          return False

    return True
