import sys

# Read input

readFile = True
splitLines = True
splitWords = False
convertToNumbers = False

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

if splitWords:
  input = [row.split() for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

if not splitLines:
  input = input[0]


input = [[int(char) for char in list(row)] for row in input]

# Calculate result

flashes = 0

class Octopus:
  """Single octopus that keeps track of energy and neighbours"""
  neighbours = []
  stepWhenLastFlashed = -1

  def __init__(self, energy):
    self.energy = energy

  def setNeighbours(self, neighbours):
    self.neighbours = neighbours

  def increaseEnergy(self, step):
    global flashes
    self.energy += 1
    if self.energy > 9 and self.stepWhenLastFlashed is not step:
      self.stepWhenLastFlashed = step
      flashes += 1
      for n in self.neighbours:
        n.increaseEnergy(step)

  def backToZeroIfOver(self):
    if self.energy > 9:
      self.energy = 0
      return 1
    return 0
  
  def __str__(self):
    return str(self.energy)

  def __repr__(self):
    return str(self.energy)


def initOctopuses(input):
  octopuses = [[Octopus(energy) for energy in row] for row in input]
  for y in range(len(input)):
    for x in range(len(input[y])):
      neighbours = [(x + dirX, y + dirY) for dirX, dirY in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]]
      neighbours = [octopuses[y][x] for x, y in neighbours if y >= 0 and y < len(input) and x >= 0 and x < len(input[y])]
      octopuses[y][x].setNeighbours(neighbours)
  return octopuses

# 1

octopuses = initOctopuses(input)

for step in range(100):
  for row in octopuses:
    for o in row:
      o.increaseEnergy(step)
  for row in octopuses:
    for o in row:
      o.backToZeroIfOver()
  print()
  print("step " + str(step))
  for row in octopuses:
    print(row)

result = flashes
print("Result: {}".format(result))


# 2

step = 1
octopuses = initOctopuses(input)

while True:
  for row in octopuses:
    for o in row:
      o.increaseEnergy(step)
  flashes = sum([sum([o.backToZeroIfOver() for o in row]) for row in octopuses])
  if flashes == 100:
    break
  step += 1

result = step
print("Result: {}".format(result))