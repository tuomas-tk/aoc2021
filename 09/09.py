import sys

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

input = [list(row) for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

if not splitLines:
  input = input[0]


# Calculate result

# 1

totalRisk = 0

for y in range(len(input)):
  for x in range(len(input[y])):
    curr = input[y][x]
    neighbours = [(x + dirX, y + dirY) for dirX, dirY in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
    neighbours = [(x, y) for x, y in neighbours if y >= 0 and y < len(input) and x >= 0 and x < len(input[y])]
    if all([curr < input[y][x] for x, y in neighbours]):
      totalRisk += curr + 1


result = totalRisk
print("Result: {}".format(result))


# 2

lowPoints = []

for y in range(len(input)):
  for x in range(len(input[y])):
    curr = input[y][x]
    neighbours = [(x + dirX, y + dirY) for dirX, dirY in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
    neighbours = [(x, y) for x, y in neighbours if y >= 0 and y < len(input) and x >= 0 and x < len(input[y])]
    if all([curr < input[y][x] for x, y in neighbours]):
      lowPoints.append((x, y))

def findBasin(currX, currY, found, input):
  neighbours = [(currX + dirX, currY + dirY) for dirX, dirY in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
  neighbours = [(x, y) for x, y in neighbours if y >= 0 and y < len(input) and x >= 0 and x < len(input[y])]
  neighbours = [(x, y) for x, y in neighbours if input[y][x] >= input[currY][currX] and input[y][x] < 9 and (x, y) not in found]
  for x, y in neighbours:
    found.add((x, y))
    findBasin(x, y, found, input)
  return found

basins = [len(findBasin(lowX, lowY, {(lowX, lowY)}, input)) for lowX, lowY in lowPoints]
basins.sort(reverse=True)

result = basins[0] * basins[1] * basins[2]
print("Result: {}".format(result))