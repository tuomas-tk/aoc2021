import sys
import numpy as np

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
  input = [(row.split('|')[0].split(), row.split('|')[1].split()) for row in input]



# Calculate result

# 1

counts = [0] * 10

for patterns, digits in input:
  for digit in digits:
    if len(digit) == 2:    # 1
      counts[1] += 1
    elif len(digit) == 4:  # 4
      counts[4] += 1
    elif len(digit) == 3:  # 7
      counts[7] += 1
    elif len(digit) == 7:  # 8
      counts[8] += 1


result = sum(counts)
print("Result: {}".format(result))


# 2
# Implemented using Bayesian interference. This is overkill but wanted to see if it works.

np.set_printoptions(precision=4)

MAP = {
      'a': 0,
      'b': 1,
      'c': 2,
      'd': 3,
      'e': 4,
      'f': 5,
      'g': 6,
    }

INV_MAP = {v: k for k, v in MAP.items()}

DIGIT_SEGMENTS = {
  'abcefg': 0,
  'cf': 1,
  'acdeg': 2,
  'acdfg': 3,
  'bcdf': 4,
  'abdfg': 5,
  'abdefg': 6,
  'acf': 7,
  'abcdefg': 8,
  'abcdfg': 9,
}

def norm(arr):
  arr /= sum(arr)

total = 0

for patterns, digits in input:

  # Priori: equal probability of all segments
  segments = np.full((7, 7), 1 / 7)  # first dimension: unknown segment names
                                     # second dimension: probability for the segment name to represent different real segments

  for pattern in patterns:
    if len(pattern) == 2:  # 1 for sure
      likelihood = np.zeros(7)
      likelihood[MAP['c']] = 1
      likelihood[MAP['f']] = 1

    elif len(pattern) == 4:  # 4 for sure
      likelihood = np.zeros(7)
      likelihood[MAP['b']] = 1
      likelihood[MAP['c']] = 1
      likelihood[MAP['d']] = 1
      likelihood[MAP['f']] = 1

    elif len(pattern) == 3:  # 7 for sure
      likelihood = np.zeros(7)
      likelihood[MAP['a']] = 1
      likelihood[MAP['c']] = 1
      likelihood[MAP['f']] = 1

    elif len(pattern) == 7:  # 8 for sure
      likelihood = np.ones(7)
      # this gains no information

    elif len(pattern) == 5:  # 2, 3, or 5
      likelihood = np.zeros(7)
      likelihood[MAP['a']] = 1
      likelihood[MAP['b']] = 1 / 3
      likelihood[MAP['c']] = 2 / 3
      likelihood[MAP['d']] = 1
      likelihood[MAP['e']] = 1 / 3
      likelihood[MAP['f']] = 2 / 3
      likelihood[MAP['g']] = 1

    elif len(pattern) == 6:  # 0, 6, or 9
      likelihood = np.zeros(7)
      likelihood[MAP['a']] = 1
      likelihood[MAP['b']] = 1
      likelihood[MAP['c']] = 2 / 3
      likelihood[MAP['d']] = 2 / 3
      likelihood[MAP['e']] = 2 / 3
      likelihood[MAP['f']] = 1
      likelihood[MAP['g']] = 1

    else:
      print("unknown pattern", pattern)
    
    for i in range(7):
      if i in [MAP[c] for c in pattern]: # apply likelihood to segments which exist in the pattern
        segments[i] *= likelihood
      else:
        segments[i] *= (likelihood * (-1) + 1) # negated likelihood for segment names that do not exist in the pattern

    # normalize the posteriori
    for row in segments:
      norm(row)

  # print(segments)

  number = 0
  for digit in digits:
    # convert segments of each digit to the real segments
    realDigit = []
    for segment in digit:
      probs = list(segments[MAP[segment]])
      mostProbable = INV_MAP[probs.index(max(probs))]
      realDigit.append(mostProbable)
    # find which digit has these segments and add to the whole number
    realDigit.sort()
    n = DIGIT_SEGMENTS["".join(realDigit)]
    number = number * 10 + n

  total += number


result = total
print("Result: {}".format(result))

