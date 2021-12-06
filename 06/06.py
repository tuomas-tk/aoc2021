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

if splitLines:
  input = input.splitlines()

if splitWords:
  input = [row.split(',') for row in input]

if convertToNumbers:
  if splitWords:
    input = [[int(value.strip()) for value in row] for row in input]
  else:
    input = [int(value.strip()) for value in input]

input = input[0]

# Calculate result


print(input)

# 1

fish = [i for i in input]

for day in range(80):
  for i in range(len(fish)):
    if fish[i] == 0:
      fish[i] = 6
      fish.append(8)
    else:
      fish[i] -= 1

result = len(fish)
print("Result: {}".format(result))


# 2

counts = [0] * 9
for x in input:
  counts[x] += 1

for day in range(256):
  zeros = counts[0]
  for c in range(8):
    counts[c] = counts[c + 1]
  counts[6] += zeros
  counts[8] = zeros

result = sum(counts)
print("Result: {}".format(result))