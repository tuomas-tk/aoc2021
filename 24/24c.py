import sys
from typing import List, Tuple
from collections import defaultdict
import math
from functools import lru_cache
from copy import copy, deepcopy
from math import floor

@lru_cache(maxsize=None)
def calcStep(prevZ, input, c1, c2):
  z = prevZ
  x = 0 if ((prevZ % 26) + c1 == input) else 1
  if c1 < 0:
    z = floor(z / 26) # tämä kadottaa edellisen inputin pois
  z = z * (25 * x + 1) + (input + c2) * x
  return z

stepConstants = [
  (14, 12),
  (13, 6),
  (12, 4),
  (14, 5),
  (13, 0),
  (-7, 4),
  (-13, 15),
  (10, 14),
  (-7, 6),  # 9
  (11, 14),
  (-9, 8),
  (-2, 5),
  (-9, 14),
  (-14, 4),
]

def calcResult(input):
  z = 0
  for i, (c1, c2) in enumerate(stepConstants):
    z = calcStep(z, input[i], c1, c2)
  return z

i = [1,2,3,4,5,6,7,8,9]

# def recursive():
#@lru_cache(maxsize=None)
def findLargestAcceptable(prevZ, inputs, step):
  if step <= 3:
    print(inputs)
    print(calcStep.cache_info())
    #print(findLargestAcceptable.cache_info())
  if step == 14:
    return None
  c1, c2 = stepConstants[step]
  for input in i:
    if c1 < 0 and step >= 1 and prevZ % 26 + c1 != input:
      #print("skipped {} {} {}".format(c1, step, inputs))
      continue
    nextZ = calcStep(prevZ, input, c1, c2)
    if nextZ == 0:
      return inputs * 10 + input
    res = findLargestAcceptable(nextZ, inputs * 10 + input, step + 1)
    if res != None:
      return res
  return None

print(findLargestAcceptable(0, 0, 0))

def run():
  target = [0]
  for step in [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
    print()
    print("--- STEP {} --- {}".format(step, len(target)))
    newTargets = set()
    for prevZ in range(0, 1000000):
      c1, c2 = stepConstants[step]
      for input in i:
        if calcStep(prevZ, input, c1, c2) in target:
          newTargets.add(prevZ)
          #print(prevZ, input)
    target = list(newTargets)

# print(run())

"""
for i1 in i:
  for i2 in i:
    for i3 in i:
      for i4 in i:
        for i5 in i:
          for i6 in i:
            for i7 in i:
              for i8 in i:
                for i9 in i:
                  for i10 in i:
                    for i11 in i:
                      for i12 in i:
                        for i13 in i:
                          for i14 in i:
                            input = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14]
                            if calcResult(input) == 0:
                              print("FOUND RESULT {}".format(input))
                    print(i7, i8, i9, i10)

for input in range(11111111111111, 99999999999999):
  if input % 10000 == 0:
    print(input, (input - 11111111111111) / (99999999999999 - 11111111111111) * 100)
  input = [int(i) for i in str(input)]
  if calcResult(input) == 0:
    print("FOUND RESULT {}".format(input))
"""