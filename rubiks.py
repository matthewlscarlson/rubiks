import numpy as np
from operator import attrgetter

# Rubik's Cube
# Cubies: Individual cubes stored in 2D array ('R' = Red, 'G' = Green, 'B' = Blue)
# Weight: f = g + h value calculated via heuristic() and cost in solve()
# Move: Description of move performed (e.g. "Row 0 Left")
# Parent: Cube from which this cube is derived
class Rubiks:
  def __init__(self, cubies, weight, move, parent):
    self.cubies = cubies
    self.weight = weight
    self.move = move
    self.parent = parent

  # Print cubies as move performed to get there
  def __str__(self):
    return '\n'.join(['|'.join([str(cubies) for cubies in row]) for row in
      self.cubies]) + '\nMove: ' + (self.move)

# Move Rubik's Cube by "rolling" row left or right OR column up and down
# E.g. R G B rolled left would be G B R
# and
#      R                    G
#      G rolled up would be B
#      B                    R
def move(cubies, pos, dir):

  # Duplicate cubies so that other cubes won't be altered
  cubies = cubies.copy()

  if dir == 'Left':
    cubies[pos,:] = np.roll(cubies[pos,:], 2)
  elif dir == 'Right':
    cubies[pos,:] = np.roll(cubies[pos,:], -2)
  elif dir == 'Up':
    cubies[:,pos] = np.roll(cubies[:,pos], 2)
  elif dir == 'Down':
    cubies[:,pos] = np.roll(cubies[:,pos], -2)

  return cubies

# Calculate h value (number of cubies out of place, i.e. Hamming distance)
# cost g calculated in solve()
def heuristic(cubies, goal):
  h = 0
  # If cubie not in right place add 1 to h
  for i,j in np.ndindex(goal.shape):
    if (cubies[i, j] != goal[i, j]):
        h += 1
  return h;

# Helper function to *efficiently* find move in opened/closed set
def find(list, key):
  for item in list:
    if np.array_equal(item.cubies, key.cubies): return 1
  return 0

# A* search algorithm
def solve(rubiks, goal):
  # Possible moves
  dirs = ['Left', 'Right', 'Up', 'Down']
  # The A* search algorithm open priority queue
  open = []
  # Start state automatically placed in closed
  closed = [rubiks]

  node = rubiks

  cost = 0

  # Heuristic of zero means goal state reached
  while heuristic(node.cubies, goal) > 0:
    cost += 1

    # Generate all successors for node
    # I.e. For row/column zero, one, or two you can move up, down, left, right
    for dir in dirs:
      for pos in range(np.shape(node.cubies)[0]):
        cubies = move(node.cubies, pos, dir)
        adjacent = Rubiks(cubies, heuristic(cubies, goal) + cost, ('Column '
          if dir == 'Up' or dir == 'Down' else 'Row ') + str(pos) + ' ' + dir,
          node)

        # Skip if in open or closed with lower weight
        if find(open, adjacent) or find(closed, adjacent):
          continue

        # Else add to open
        open.append(adjacent)

    # Sort open by minimum weight
    # Node has least weight and is popped off from open set
    open.sort(key=lambda move: move.weight)
    node = open.pop(0)

    # If node's parent is in closed remove nodes following it, reset cost,
    # and check open for stragglers
    for i, c in enumerate(closed):
      if c == node.parent:
        closed = closed[:i + 1]
        cost = i + 1
        for o in open:
          if o.parent not in closed:
            open.pop(0)

    # Add node to closed set after examining it
    closed.append(node)

  # Print moves needed to get to goal state
  for c in closed:
    print(c)

def main():

  # We want to get this to goal
  start = np.array([['R', 'G', 'G'],
                    ['G', 'B', 'R'],
                    ['B', 'R', 'B']])


  # Here is what solved 2D Rubik's Cube looks like
  goal = np.array([['R', 'R', 'R'],
                   ['G', 'G', 'G'],
                   ['B', 'B', 'B']])

  # Default cube will have these attributes:
  # Cubies: start
  # Heuristic: See heuristic() above
  # No parent, it is the first one
  # No move either, just call it Begin
  rubiks = Rubiks(start, heuristic(start, goal), 'Begin', None)

  # Solve the cube!
  solve(rubiks, goal)

if __name__ == "__main__":
    main()
