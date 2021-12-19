import sys
import re
from collections import defaultdict

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = re.split(r'--- scanner \d+ ---\n', input)
input = [scanner.strip().splitlines() for scanner in input[1:]]
input = [[[int(value) for value in line.split(',')] for line in scanner] for scanner in input]

# Calculate result

def flatten(t):
  return [item for sublist in t for item in sublist]

def allRelativeDistances(beacons):
  l = []
  for ia, ba in enumerate(beacons):
    for ib, bb in enumerate(beacons):
      if ib >= ia:
        continue
      l.append((
        (
          bb[0] - ba[0],
          bb[1] - ba[1],
          bb[2] - ba[2]
        ),
        (ia, ib)
      ))
  return l

memoAllRelativeDistancesOfScanner = dict([
  (i, allRelativeDistances(scanner))
  for i, scanner in enumerate(input)
])

def countSame(dist1, dist2):
  l = []
  dist1.sort(key=lambda d: d[0])
  dist2.sort(key=lambda d: d[0])
  l1 = len(dist1)
  l2 = len(dist2)
  i = 0
  j = 0
  while i < l1 and j < l2:
    d1 = dist1[i]
    d2 = dist2[j]
    if d1[0] == d2[0]:
      l.append((d1, d2))
      i += 1
      j += 1
    elif d1[0] < d2[0]:
      if i + 1 < l1:
        i += 1
      else:
        j += 1
    else:
      if j + 1 < l2:
        j += 1
      else:
        i += 1
  return l


COORD_PERMUTATIONS = [
  [0, 1, 2],
  [1, 2, 0],
  [2, 0, 1],
  [0, 2, 1],
  [2, 1, 0],
  [1, 0, 2],
]

SIGN_PERMUTATIONS = [
  [+1, +1, +1],
  [+1, +1, -1],
  [+1, -1, +1],
  [-1, +1, +1],
  [-1, -1, -1],
  [-1, -1, +1], 
  [-1, +1, -1],
  [+1, -1, -1],
]

def transformCoords(coordPerm, signPerm, coords):
  return (
    signPerm[0] * coords[coordPerm[0]],
    signPerm[1] * coords[coordPerm[1]],
    signPerm[2] * coords[coordPerm[2]]
  )

def transformRelativeDistances(coordPerm, signPerm, relDists):
  return [
    (
      transformCoords(coordPerm, signPerm, coords),
      idxs
    )
    for coords, idxs in relDists
  ]



def findMatchingPairs(scannerIndex1, scannerIndex2):
  relDists1 = memoAllRelativeDistancesOfScanner[scannerIndex1]
  relDists2 = memoAllRelativeDistancesOfScanner[scannerIndex2]
  l = []
  for coordPerm in COORD_PERMUTATIONS:
    for signPerm in SIGN_PERMUTATIONS:
      transformed2 = transformRelativeDistances(coordPerm, signPerm, relDists2)
      same = countSame(relDists1, transformed2)
      if len(same) >= 12:
        foundPairs = set(flatten([[(a1, b2), (a1, b2)] for (_, (a1, a2)), (_, (b1, b2)) in same]))
        l.append((coordPerm, signPerm, foundPairs))
  return l


def findNeighbours(si1, skip):
  s1 = input[si1]

  results = []
  for si2, s2 in enumerate(input):
    if si2 == si1 or si2 in skip:
      continue
    # print("Trying to find match from scanner {} to scanner {}...".format(si1, si2))
    matches = findMatchingPairs(si1, si2)

    for match in matches:
      coordPerm, signPerm, foundPairs = match
      print("Found possibly matching scanner #{} with coordPerm {}, signPerm {}".format(si2, coordPerm, signPerm))
      deltas = set()
      for pair in foundPairs:
        canon = s1[pair[0]]
        transformed = transformCoords(coordPerm, signPerm, s2[pair[1]])
        delta = (
          transformed[0] + canon[0],
          transformed[1] + canon[1],
          transformed[2] + canon[2],
        )
        deltas.add(delta)
      if len(deltas) != 1:
        print(" > but the delta values (count: {}) were not consistent for all pairs of the match.".format(len(deltas)))
        continue
      delta = deltas.pop()
      results.append((si2, coordPerm, signPerm, delta))
      print(" > VERIFIED MATCH from scanner #{} to #{} with coordPerm {}, signPerm {} and delta {}".format(si1, si2, coordPerm, signPerm, delta))

  return results


def combineMap(currI, visited): # returns set of beacon coordinates and a set of scanner coordinates
  
  canonBeacons = set([(x,y,z) for x,y,z in input[currI]])
  canonScanners = set([(0, 0, 0)])

  nexts = findNeighbours(currI, visited)
  visited |= {n[0] for n in nexts}
  
  for ni, coordPerm, signPerm, delta in nexts:
    beacons, scanners = combineMap(ni, visited)

    beacons = [transformCoords(coordPerm, signPerm, coords) for coords in beacons]
    beacons = [(
      delta[0] - coords[0],
      delta[1] - coords[1],
      delta[2] - coords[2],
    ) for coords in beacons]
    canonBeacons |= set(beacons)
    
    scanners = [transformCoords(coordPerm, signPerm, coords) for coords in scanners]
    scanners = [(
      delta[0] - coords[0],
      delta[1] - coords[1],
      delta[2] - coords[2],
    ) for coords in scanners]
    canonScanners |= set(scanners)
  return canonBeacons, canonScanners

canonBeacons, canonScanners = combineMap(0, {0})


# 1

result = len(canonBeacons)
print("Result: {}".format(result))

# 2

maxDist = 0
for x1,y1,z1 in canonScanners:
  for x2,y2,z2 in canonScanners:
    d = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
    if d > maxDist:
      maxDist = d

result = maxDist
print("Result: {}".format(result))



## ---- UNIT TESTS ----

assert (transformRelativeDistances(
  [0, 2, 1],
  [-1, -1, +1],
  [
    ((1, 2, 3), (42, 69)),
    ((4, 5, 6), (40, 70))
  ]
)) == [
  ((-1, -3, 2), (42, 69)),
  ((-4, -6, 5), (40, 70))
]