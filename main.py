from random import random, randrange, sample

from world import World
from state import State

_SIZE = 50

_LEARNING_RATE_DECAY = 1e-7
_DISCOUNT_FACTOR = 0.95

_MOVE_VALUE = -1e-6
_CRASH_VALUE = -1.0
_GOAL_VALUE = 1.0

_N_EPISODES = 10**7
_REPORT_EVERY = 10**6

_CLOCKWISE, _COUNTERCLOCKWISE, _FORWARD = range(3)

def render_world(world):
  return State(world, -1, -1, 0).render()

def measure_performance(world, q_table):
  successes = 0
  crashes = 0
  infinite_loops = 0

  for empty_cell in world.empty_cells:
    for direction in range(4):
      state = State(world, empty_cell[0], empty_cell[1], direction)

      visited = [[[False for direction in range(4)] for y in range(world.size)] for x in range(world.size)]

      while not state.done:
        (x, y, direction) = (state.x, state.y, state.direction)

        if visited[x][y][direction]:
          break

        visited[x][y][direction] = True

        expected_values = q_table[x][y][direction]
        best_action = None

        for action in range(3):
          if best_action is None or expected_values[action] > expected_values[best_action]:
            best_action = action

        if best_action == _CLOCKWISE:
          state = state.clockwise()
        elif best_action == _COUNTERCLOCKWISE:
          state = state.counterclockwise()
        else:
          state = state.forward()

      if state.goal_achieved:
        successes += 1
      elif state.crashed:
        crashes += 1
      else:
        infinite_loops += 1

  return (successes, crashes, infinite_loops)

world = World(_SIZE)

print("Generated a (%d, %d) world:\n%s" % (world.size, world.size, render_world(world)))

q_table = []

for x in range(world.size):
  q_table.append([])
  for y in range(world.size):
    q_table[-1].append([])
    for direction in range(4):
      q_table[-1][-1].append([])
      for action in range(3):
        q_table[-1][-1][-1].append(2 * random() - 1)

for episode in range(1, _N_EPISODES + 1):
  learning_rate = (1 - _LEARNING_RATE_DECAY)**episode

  (x, y) = sample(world.empty_cells, 1)[0]
  direction = randrange(4)
  state = State(world, x, y, direction)

  action = randrange(3)

  if action == _CLOCKWISE:
    next = state.clockwise()
  elif action == _COUNTERCLOCKWISE:
    next = state.counterclockwise()
  else:
    next = state.forward()

  immediate_reward = _MOVE_VALUE
  if next.goal_achieved:
    immediate_reward += _GOAL_VALUE
  elif next.crashed:
    immediate_reward += _CRASH_VALUE

  if next.done:
    best_future_reward = 0
  else:
    best_future_reward = max(q_table[next.x][next.y][next.direction])

  q_table[x][y][direction][action] *= (1 - learning_rate)
  q_table[x][y][direction][action] += learning_rate * (immediate_reward + _DISCOUNT_FACTOR * best_future_reward)

  if episode % _REPORT_EVERY == 0:
    successes, crashes, infinite_loops = measure_performance(world, q_table)

    total = successes + crashes + infinite_loops
    success_rate = successes / total
    crash_rate = crashes / total
    infinite_loop_rate = infinite_loops / total

    print("After %d episodes of training: S %.2f, C %.2f, I %.2f" % (episode, success_rate * 100, crash_rate * 100, infinite_loop_rate * 100))
