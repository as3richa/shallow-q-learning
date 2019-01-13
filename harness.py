import world
import state

st = state.State(world.generate(), 0, 0, 0, 0)

while not st.done:
  print(st.render())

  command = input('f/cw/ccw> ')

  if command == 'f':
    st, reward = st.forward()
  elif command == 'cw':
    st, reward = st.clockwise()
  elif command == 'ccw':
    st, reward = st.counterclockwise()

  print('+ %d' % reward)
