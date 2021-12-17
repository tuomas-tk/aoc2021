import sys
import re
from typing import List, Tuple
import itertools
from collections import defaultdict

# Read input

readFile = True
splitLines = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

def parseRow(row) -> Tuple[Tuple[int, int], Tuple[int, int]]:
  m = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", row)
  return (
    (int(m[1]), int(m[2])),
    (int(m[3]), int(m[4]))
  )

input = [parseRow(row) for row in input]

# Calculate result

def calculate(target):
  tx, ty = target
  tx0, tx1 = tx
  ty0, ty1 = ty
  # This works only if the target area is to the positive x direction
  assert tx[0] >= 0 and tx[1] >= 0
  # and if it is fully below the starting point
  assert ty[0] < 0 and ty[1] < 0
  # Order of the coordinates should be increasing
  assert tx0 < tx1 and ty0 < ty1

  # First we look at the x-direction, and go through different initial velocities (vx0)
  # that might lead us to some x-coordinate inside the target area.
  
  # These dictionaries contain sets of all found vx0 values, grouped by the t value,
  # which is the number of time steps required to reach the target area.
  # The maps are in format { t -> set(vx0) }
  tToVx0Map = defaultdict(set)
  # Because of the drag, we finally end up falling vertically downwards for infinity
  # inside the target area. This map contains list of vx0 values that lead to this situation,
  # and the t value is the first one which lands us on the target area, meaning that all t values
  # larger than that are completely valid.
  inftToVx0Map = defaultdict(set)

  results: Tuple[int, int, int] = [] # [(h, x, y)]
  
  for vx0 in range(0, tx1 + 1):
    # lower limit: not moving in x-direction
    # upper limit: moving to the far edge of target area on the first step

    possibleT = []

    for t in range(1, vx0):
      # lower limit: at the target area after the first step
      # upper limit: t = vx0 - 1, which means that drag has ALMOST decreased the x velocity to zero.
      #              Warning: the simulation in y direction must still continue, because
      #              we could be falling vertically down

      x = -t * (t - 1) / 2 + vx0 * t

      #print("vx0: {}   t: {}   x: {}".format(vx0, t, x))
      if x > tx1:  # we have exceeded the target area, no need to simulate further
        break
      elif x >= tx0 and x <= tx1:
        possibleT.append(t)
    
    # Handling the case vx(t)=0 which happens when t >= vx0 separately
    x = -vx0 * (vx0 - 1) / 2 + vx0 * vx0
    if x >= tx0 and x <= tx1:
      inftToVx0Map[min(possibleT)].add(vx0)
    else:
      for t in possibleT:
        tToVx0Map[t].add(vx0)

  #print(tToVx0Map)
  #print(inftToVx0Map)

  # Let's ASSUME that we are shooting up or sideways (vy0 >= 0).
  # Then the probe rises to the height
  #   h = vy0 + (vy0 - 1) + (vy0 - 2) + (vy0 - 3) + ... + 1
  # which is an arithmetic sum
  #   h = S = (vy0 + 1) / 2 * vy0

  # After that it starts to fall again, so that at time
  #   t1 = 2 * vy0 + 1
  # it is again at height y=0.

  # The Mysterious Underwater Christmas Land doesn't have drag in vertical direction,
  # which means that according to the law of conservation of energy the velocity at time t1 is
  #   v(t1) = -vy0
  # and from there on the y-coordinate behaves according to the arithmetic sum:
  #   y(t1 + 0) = 0
  #   y(t1 + 1) = -(vy0 + 1)
  #   y(t1 + 2) = -((vy0 + 1) + (vy0 + 2))
  #   y(t1 + 3) = -((vy0 + 1) + (vy0 + 2) + (vy0 + 3))
  #            ...
  #   y(t1 + t) = -((vy0 + 1) + (vy0 + 2) + ... + (vy0 + t))
  #             = -(((vy0 + 1) + (vy0 + t)) / 2 * t)
  #             = -(vy0 + (t + 1) / 2) * t

  # BUT when we are shooting directly downwards at velocity vy0 < 0 the y-coordinate evolves as
  #   y(0) = 0
  #   y(1) = vy0
  #   y(2) = vy0 + (vy0 - 1)
  #   y(3) = vy0 + (vy0 - 1) + (vy0 - 2)
  #       ...
  #   y(t) = vy0 + (vy0 - 1) + ... + (vy0 - (t - 1))
  #        = (vy0 + (vy0 - t + 1)) / 2 * t
  #        = (vy0 + (-t + 1) / 2) * t

  for vy0 in range(ty0, abs(ty0) + 1):
    # lower limit: smallest possible velocity to shoot still upwards (this was just an assumption)
    # upper limit: when dropping below y=0 again after the first time step the probe hits the bottom edge of the target area

    if vy0 >= 0: # shooting up
      # h = maximum value of y
      h = (vy0 + 1) / 2 * vy0
      # time when again at y=0
      t1 = 2 * vy0 + 1
      calcY = lambda dt: -(vy0 + (dt + 1) / 2) * dt
    else: # shooting down
      h = 0
      t1 = 0
      calcY = lambda dt: (vy0 + (-dt + 1) / 2) * dt

    # Iterate through time infinitely forward, break is inside
    # t = t1 + dt
    for dt in itertools.count(1):
      y = calcY(dt)
      #print("  vy0: {}   h: {}   t1: {}   t: {}   y: {}".format(sign * vy0, h, t1, t1 + dt, y))
      if y < ty0: # have went below the target area
        break
      elif y >= ty0 and y <= ty1: # inside target area
        t = t1 + dt
        # print("target at t = " + str(t))
        # Go through the possible times when the x-coordinate is correct to match the x and y coords together
        # Distinct t values where the probe passes the target area
        if t in tToVx0Map:
          vx0s = tToVx0Map[t]
          #print("found distinct results in x-direction at time {}:   {}".format(t, vx0s))
          for vx0 in vx0s:
            results.append((h, vx0, vy0))
        # Values that go from t to infinity (because falling vertically inside target area)
        for xt, vx0s in inftToVx0Map.items():
          if xt <= t:
            #print("found infinity results in x-direction at time {}:   {}".format(t, vx0s))
            for vx0 in vx0s:
              results.append((h, vx0, vy0))

  return results
  

for row in input:
  print("Input: {}".format(row))

  results = calculate(row)

  # print("\n".join([str(r) for r in results]))

  # 1
  result = int(max([h for h, _, _ in results]))
  print("Result 1: {}".format(result))

  # 2
  result = len(set([(x, y) for _, x, y in results]))
  print("Result 2: {}".format(result))