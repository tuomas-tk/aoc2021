import sys

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

points, folds = input.split("\n\n")

points = points.splitlines()
points = [row.split(',') for row in points]
points = [[int(value.strip()) for value in row] for row in points]
points = set([(row[0], row[1]) for row in points])

folds = folds.splitlines()
folds = [(value.split('=')[0][-1], int(value.split('=')[1].strip())) for value in folds]

# Calculate result

def newCoord(coords: (int, int), fold: (str, int)) -> (int, int):
  if fold[0] == 'x':
    if coords[0] == fold[1]:
      return None
    elif coords[0] > fold[1]:
      return (
        fold[1] - (coords[0] - fold[1]),
        coords[1]
      )
    else:
      return coords
  if fold[0] == 'y':
    if coords[1] == fold[1]:
      return None
    elif coords[1] > fold[1]:
      return (
        coords[0],
        fold[1] - (coords[1] - fold[1])
      )
    else:
      return coords

def foldAlong(fold: (str, int), points: set) -> set:
  return {newCoord(point, fold) for point in points}

# 1

result = len(foldAlong(folds[0], points))
print("Result: {}".format(result))


# 2

for fold in folds:
  points = foldAlong(fold, points)

maxX = max([x for x, y in points])
maxY = max([y for x, y in points])

for y in range(maxY + 1):
  row = [
    ("#" if (x, y) in points else " ")
    for x in range(maxX + 1)
  ]
  print("".join(row))