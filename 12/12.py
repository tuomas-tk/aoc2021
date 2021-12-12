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

input = input.splitlines()

if splitWords:
  input = [row.split('-') for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

if not splitLines:
  input = input[0]


# Calculate result

neighbours = dict()
for a, b in input:
  neighbours[a] = neighbours.get(a, []) + [b]
  neighbours[b] = neighbours.get(b, []) + [a]

# 1

def findPaths(curr, visited):
  if curr == "end":
    return [visited + [curr]]
  elif curr.islower() and curr in visited:
    return []
  else:
    return [
      path
        for next in neighbours[curr]
          for path in findPaths(next, visited + [curr])
    ]


paths = findPaths('start', [])
result = len(paths)
print("Result: {}".format(result))


# 2

def findPaths2(curr, visited, hasVisitedSmallTwice):
  if curr == "end":
    return [visited + [curr]]
  elif curr.islower() and curr in visited:
    if hasVisitedSmallTwice or curr == "start" or curr == "end":
      return []
    else:
      hasVisitedSmallTwice = True
      # no return here

  return [
    path
      for next in neighbours[curr]
        for path in findPaths2(next, visited + [curr], hasVisitedSmallTwice)
  ]

paths = findPaths2('start', [], False)
result = len(paths)
print("Result: {}".format(result))