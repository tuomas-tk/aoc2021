import sys

# Read input

readFile = True
splitLines = True
splitWords = False
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

counts = [0]*len(input[0])

for word in input:
  for i in range(len(word)):
    if word[i] == '1':
      counts[i] += 1

for i in range(len(counts)):
  counts[i] = counts[i] * 1.0 / len(input)

sum = 0
sum2 = 0
for i in range(len(counts)):
  if counts[i] >= 0.5:
    sum += pow(2, len(counts) - i - 1)
  else:
    sum2 += pow(2, len(counts) - i - 1)

result = sum * sum2
print("Result: {}".format(result))

# 2

oxygen = [v for v in input]
co2 = [v for v in input]

def countt(arr, i):
  counts = 0
  for word in arr:
    if word[i] == '1':
      counts += 1
  return counts * 1.0 / len(arr)

for i in range(len(input[0])):
  oRatio = countt(oxygen, i)
  cRatio = countt(co2, i)

  if (len(oxygen) > 1):
    oxygen = [v for v in oxygen if ((v[i] == '1') == (oRatio >= 0.5))]
  if (len(co2) > 1):
    co2 = [v for v in co2 if ((v[i] == '1') == (cRatio < 0.5))]

oInt = 0
for i in range(len(oxygen[0])):
  if (oxygen[0][i] == '1'):
    oInt += pow(2, len(oxygen[0]) - i - 1)

co2Int = 0
for i in range(len(co2[0])):
  if (co2[0][i] == '1'):
    co2Int += pow(2, len(co2[0]) - i - 1)

result = oInt * co2Int
print("Result: {}".format(result))