import sys

# Read input

readFile = True
splitLines = True
splitWords = True
convertToNumbers = False

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

if splitLines:
  input = input.splitlines()

if splitWords:
  input = [row.split() for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]


# Calculate result

vents = [([int(n) for n in start.split(',')], [int(n) for n in end.split(',')]) for start, _, end in input]

width = max([max(start[0], end[0]) for start, end in vents]) + 1
height = max([max(start[1], end[1]) for start, end in vents]) + 1

# print(vents)
print(width, height)

def calc(isSecondPart):
  counts = []
  for i in range(height):
    counts.append(([0] * width))

  for start, end in vents:
    x1 = min(start[0], end[0])
    x2 = max(start[0], end[0])
    y1 = min(start[1], end[1])
    y2 = max(start[1], end[1])
    if x1 == x2:
      for y in range(y1, y2 + 1):
        counts[y][x1] += 1
    elif y1 == y2:
      for x in range(x1, x2 + 1):
        counts[y1][x] += 1
    elif isSecondPart:
      xs = list(range(x1, x2 + 1))
      ys = list(range(y1, y2 + 1))
      if (start[0] < end[0]) != (start[1] < end[1]):
        ys.reverse()
      for i in range(len(xs)):
        counts[ys[i]][xs[i]] += 1      

  sum = 0
  for row in counts:
    for col in row:
      if col >= 2:
        sum += 1

  #print()
  #for row in counts:
  #  print(row)

  result = sum
  print("Result: {}".format(result))

calc(False)
calc(True)