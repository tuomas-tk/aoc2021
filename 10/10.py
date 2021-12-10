import sys
import queue

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


# Calculate result

pairs = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>',
}

def findFirstIllegal(row):
  opened = queue.LifoQueue()
  for c in row:
    pair = pairs.get(c)
    if pair:
      opened.put(pair)
    else:
      last = opened.get()
      if last is not c: # incorrect closing brace
        return c, opened
  return None, opened


points1 = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
}

points2 = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4,
}

pointSum1 = 0
pointList2 = []

for row in input:
  illegal, unclosed = findFirstIllegal(row)
  if illegal != None:
    pointSum1 += points1.get(illegal)
  else:
    p = 0
    while not unclosed.empty():
      c = unclosed.get()
      p = p * 5 + points2.get(c)
    pointList2.append(p)

# 1
result = pointSum1
print("Result: {}".format(result))

# 2
pointList2.sort()
result = pointList2[int(len(pointList2) / 2)]
print("Result: {}".format(result))