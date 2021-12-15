import sys
import math
from queue import PriorityQueue

# Read input

readFile = True
splitLines = True
splitWords = True
convertToNumbers = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

if splitWords:
  input = [list(row) for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

if not splitLines:
  input = input[0]


# Calculate result


def getNeighbours(coords, size):
  x0, y0 = coords
  return [
    (x, y)
    for x, y in [(x0 + x, y0 + y) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    if y >= 0 and y < size and x >= 0 and x < size
  ]

def calculate(risks):
  q = PriorityQueue()

  for y in range(len(risks)):
    for x in range(len(risks[y])):
      if x == 0 and y == 0:
        q.put((0, (x, y)))
      else:
        q.put((math.inf, (x, y)))

  visited = set()
  lowestRisk = [[math.inf for x in row] for row in risks]
  lowestRisk[0][0] = 0

  while not q.empty():
    _, curr = q.get()
    x, y = curr
    if curr in visited:
      continue
    visited.add(curr)

    for nx, ny in getNeighbours(curr, len(risks)):
      prevLowestRisk = lowestRisk[ny][nx]
      newLowestRisk = lowestRisk[y][x] + risks[ny][nx]
      if newLowestRisk < prevLowestRisk:
        lowestRisk[ny][nx] = newLowestRisk
        q.put((newLowestRisk, (nx, ny)))

  result = lowestRisk[-1][-1]
  print("Result: {}".format(result))

  #import matplotlib.pyplot as plt
  #plt.subplot(211)
  #plt.imshow(risks, cmap='plasma', interpolation='nearest')
  #plt.subplot(212)
  #plt.imshow(lowestRisk, cmap='plasma', interpolation='nearest')
  #plt.show()


# 1
risks = input
calculate(risks)

# 2

n1 = len(risks)
n5 = len(risks) * 5
    
risks2 = []
for y in range(n5):
  arr = []
  for x in range(n5):
    arr.append(((risks[y % n1][x % n1] + math.floor(y / n1) + math.floor(x / n1) - 1) % 9) + 1)
  risks2.append(arr)

calculate(risks2)