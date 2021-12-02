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

# 1

h = 0
d = 0

for c, n in input:
  n = int(n)
  if c == "forward":
    h += n
  if c == "down":
    d += n
  if c == "up":
    d -= n

print(h, d)


result = h*d
print("Result: {}".format(result))

# 2

h = 0
d = 0
a = 0

for c, n in input:
  n = int(n)
  if c == "forward":
    h += n
    d += a * n
  if c == "down":
    a += n
  if c == "up":
    a -= n

print(h, d)

result = h*d
print("Result: {}".format(result))