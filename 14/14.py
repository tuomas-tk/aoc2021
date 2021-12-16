import sys
from collections import defaultdict

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()


template, rules = input.split('\n\n')

rules = rules.splitlines()
rules = [row.split(' -> ') for row in rules]

# Calculate result

pairs = defaultdict(lambda: 0)

# add one special character to end to allow counting the last element too in the end
template = template + "Ö" 
for i in range(len(template) - 1):
  pairs[template[i] + template[i + 1]] += 1


rules = defaultdict(None, rules)


def runRules(oldPairs, rules):
  pairs = defaultdict(int)
  for pair, count in oldPairs.items():
    insert = rules.get(pair)
    if insert is None:
      pairs[pair] += count
    else:
      pairs[pair[0] + insert] += count
      pairs[insert + pair[1]] += count
  return pairs

def countElements(pairs):
  counts = defaultdict(int)
  total = 0
  for pair, count in pairs.items():
    counts[pair[0]] += count
    total += count
  return counts, total

# 1 & 2

for i in range(1, 40 + 1):
  pairs = runRules(pairs, rules)
  if i in [10, 40]:
    counts, total = countElements(pairs)
    result = max(counts.values()) - min(counts.values())
    print("Result at {}: {}".format(i, result))