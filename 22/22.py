import sys
import re

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

input = [
  re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", row).groups()
  for row in input
]

input = [
  (state == "on", (int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)))
  for state, x1, x2, y1, y2, z1, z2 in input
]

# Calculate result

# 1

# contains cells that are on
onCubes = set()

for state, (x1, x2, y1, y2, z1, z2) in input:
  if (x1 < -50 or x2 > 50):
    continue
  for x in range(x1, x2 + 1):
    for y in range(y1, y2 + 1):
      for z in range(z1, z2 + 1):
        if state:
          onCubes.add((x, y, z))
        else:
          onCubes.discard((x, y, z))

result = len(onCubes)
print("Result: {}".format(result))

# 2

def flatten(t):
  return [item for sublist in t for item in sublist]

def removeSecondFromFirst(cuboid1, cuboid2):
  """Returns a list of cuboids that cover all parts of cuboid1 expect those that are also covered by cuboid2"""
  x1a, x2a, y1a, y2a, z1a, z2a = cuboid1
  x1b, x2b, y1b, y2b, z1b, z2b = cuboid2
  # Intersection
  x1i, x2i = max(x1a, x1b), min(x2a, x2b)
  y1i, y2i = max(y1a, y1b), min(y2a, y2b)
  z1i, z2i = max(z1a, z1b), min(z2a, z2b)
  # Nothing removed if the cuboids do not overlap
  if x1i > x2i or y1i > y2i or z1i > z2i:
    return [cuboid1]
  remaining = []
  # X-direction
  if x1a < x1i:
    remaining.append((
      x1a, x1i - 1,
      y1a, y2a,
      z1a, z2a,
    ))
  if x2a > x2i:
    remaining.append((
      x2i + 1, x2a,
      y1a, y2a,
      z1a, z2a,
    ))
  # Y-direction
  if y1a < y1i:
    remaining.append((
      x1i, x2i,
      y1a, y1i - 1,
      z1a, z2a,
    ))
  if y2a > y2i:
    remaining.append((
      x1i, x2i,
      y2i + 1, y2a,
      z1a, z2a,
    ))
  # Z-direction
  if z1a < z1i:
    remaining.append((
      x1i, x2i,
      y1i, y2i,
      z1a, z1i - 1,
    ))
  if z2a > z2i:
    remaining.append((
      x1i, x2i,
      y1i, y2i,
      z2i + 1, z2a,
    ))
  return remaining


onCuboids = list()

for i, (state1, cuboid1) in enumerate(input):
  if state1:  # Need to turn on some cubes
    previouslyOff = [cuboid1]
    # Remove those cubes from the new section that already have been turned on
    # to avoid turning them on multiple times
    for cuboid2 in onCuboids:
      previouslyOff = flatten([removeSecondFromFirst(c, cuboid2) for c in previouslyOff])
    onCuboids.extend(previouslyOff)
  else:  # Need to turn off some cubes
    onCuboids = flatten([removeSecondFromFirst(c, cuboid1) for c in onCuboids])


def size(cuboid):
  x1, x2, y1, y2, z1, z2 = cuboid
  return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

result = sum(size(c) for c in onCuboids)
print("Result: {}".format(result))


# TESTS

assert removeSecondFromFirst(
  (0, 4, 0, 4, 0, 4),
  (1, 7, 2, 5, 1, 2),
) == [
  (0, 0, 0, 4, 0, 4), # -x
  (1, 4, 0, 1, 0, 4), # -y
  (1, 4, 2, 4, 0, 0), # -z
  (1, 4, 2, 4, 3, 4), # +z
]

assert removeSecondFromFirst(
  (0, 4, 0, 4, 0, 4),
  (1, 7, 2, 5, 60, 70), # outside of z area
) == [
  (0, 4, 0, 4, 0, 4), # whole first cuboid
]