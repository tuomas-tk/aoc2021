import sys

# Read input

readFile = True
splitLines = True
splitWords = False
convertToNumbers = True

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

# 1

prev = input[0]
s = 0

for v in input:
  if (v > prev):
    s += 1
  prev = v

result = s
print("Result: {}".format(result))


# 2

prev = sum(input[0:3])
s = 0

for i in range(len(input)):
  newS = sum(input[i : i + 3])
  if (newS > prev):
    s += 1
  prev = newS

result = s
print("Result: {}".format(result))


# 2, more efficient version

result = sum(1 for i in range(2, len(input)) if input[i] > input[i - 3])

print("Result: {}".format(result))