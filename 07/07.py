import sys

# Read input

readFile = True
splitLines = False
splitWords = True
convertToNumbers = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

if splitWords:
  input = [row.split(',') for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

if not splitLines:
  input = input[0]


# Calculate result

# 1

minFuel = 10000000000000000

for p in range(min(input), max(input) + 1):
  fuel = 0
  for c in input:
    fuel += abs(p - c)
  if fuel < minFuel:
    minFuel = fuel

result = minFuel
print("Result: {}".format(result))


# 2
minFuel = 10000000000000000

for p in range(min(input), max(input) + 1):
  fuel = 0
  for c in input:
    fuel += int((abs(p - c) + 1) * abs(p - c) / 2)
  if fuel < minFuel:
    minFuel = fuel

result = minFuel
print("Result: {}".format(result))
