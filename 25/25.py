import sys
from copy import deepcopy

# Read input

readFile = True
splitLines = True
splitWords = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

if splitWords:
  input = [list(row) for row in input]

# Calculate result

# 1

def getSafeCoord(x, l):
  if x < 0:
    return l + x
  elif x >= l:
    return x - l
  else:
    return x

def inputEqual(in1, in2):
  for i in range(len(in1)):
    if in1[i] != in2[i]:
      return False
  return True

def printInput(in1):
  for row in in1:
    print(row)

step = 1
while step < 3999999999:
  nextInput = deepcopy(input)
  for y in range(len(input)):
    for x in range(len(input[y])):
      dir = input[y][x]
      if dir == ">":
        dx, dy = 1, 0
        if input[getSafeCoord(y + dy, len(input))][getSafeCoord(x + dx, len(input[0]))] == ".":
          nextInput[getSafeCoord(y + dy, len(input))][getSafeCoord(x + dx, len(input[0]))] = dir
          nextInput[y][x] = "."
  nextInput2 = deepcopy(nextInput)
  for y in range(len(input)):
    for x in range(len(input[y])):
      dir = nextInput[y][x]
      if dir == "v":
        dx, dy = 0, 1
        if nextInput[getSafeCoord(y + dy, len(input))][getSafeCoord(x + dx, len(input[0]))] == ".":
          nextInput2[getSafeCoord(y + dy, len(input))][getSafeCoord(x + dx, len(input[0]))] = dir
          nextInput2[y][x] = "."
  print(step)
  if inputEqual(nextInput2, input):
    break
  input = nextInput2
  step += 1

result = step
print("Result: {}".format(result))