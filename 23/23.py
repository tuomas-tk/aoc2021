import sys
from typing import List, Tuple
from functools import lru_cache

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = [row[3:10].split("#") for row in input.splitlines()[2:6]]

# Calculate result

def replaceIndex(tuple, index, value):
  return tuple[:index] + (value,) + tuple[index+1:]

LocState = Tuple[
  int, int, int, int, int, int, int, int, int, int,
  int, int, int, int, int, int, int, int, int, int,
  int, int, int, int, int, int
] # 26

State = Tuple[int, LocState]


def wantsToMove(name, location, locState):
  if type(location) == Hallway:
    return True
  elif type(location) == Sideroom:
    return not location.isFilledWith(name, locState)
    
def findAllowedSteps(prevLocations: List['Node'], name: int, locState: LocState) -> List[Tuple['Node', int]]:
  steps = []
  for n in prevLocations[-1].neighbours:
    if n in prevLocations:
      continue
    if locState[n.i] != -1:
      continue
    canStop, canPass = n.isAllowedToStopOrPass(name, prevLocations, locState)
    if canStop:
      steps.append((n, 1))
    if canPass:
      nextSteps = findAllowedSteps(prevLocations + [n], name, locState)
      steps.extend((node, cost + 1) for node, cost in nextSteps)
  return steps

class Node:
  neighbours: List['Node']
  i: int
  def __init__(self, i):
    self.neighbours = []
    self.i = i
  # def isAvailable(self, amphipods):
    #return all(a.location != self for a in amphipods)
  def isAllowedToStopOrPass(self, name: int, comingFrom: List['Node'], locState: LocState) -> Tuple[bool, bool]:
    raise Exception("Not implemented")

class Sideroom(Node):
  targetOccupant = None
  deeperNeighbour: 'Sideroom' = None
  def __init__(self, i, targetOccupant):
    super().__init__(i)
    self.targetOccupant = targetOccupant
  def isAllowedToStopOrPass(self, name: int, comingFrom: List[Node], locState: LocState) -> Tuple[bool, bool]:
    isOk = self.targetOccupant == name or type(comingFrom[-1]) == Sideroom
    canStop = isOk and (self.deeperNeighbour == None or self.deeperNeighbour.isFilledWith(name, locState))
    canPass = isOk
    return canStop, canPass
  def isFilledWith(self, name: int, locState: LocState) -> bool:
    correctName = name == self.targetOccupant
    correctOccupant = locState[self.i] == name
    deeperOk = self.deeperNeighbour == None or self.deeperNeighbour.isFilledWith(name, locState)
    return correctName and correctOccupant and deeperOk
  def __repr__(self):
    return "<Sideroom{} {} ({} neighbours)>".format(self.i, self.targetOccupant, len(self.neighbours))

class Hallway(Node):
  canBeStopped: bool
  def __init__(self, i, canBeStopped):
    super().__init__(i)
    self.canBeStopped = canBeStopped
  def isAllowedToStopOrPass(self, name: int, comingFrom: List[Node], locState: LocState) -> Tuple[bool, bool]:
    if type(comingFrom[0]) == Hallway: # started the move already from hallway -> can't stop in hallway
      return False, True
    else:
      return self.canBeStopped, True
  def __repr__(self):
    return "<Hallway{} {} ({} neighbours)>".format(self.i, "stoppable" if self.canBeStopped else "non-stop", len(self.neighbours))
  
# 1

# Create the burrow with the following indexing:

# 0   1   2   3   4   5   6   7   8   9   10
#        11      15      19      23
#        12      16      20      24
#        13      17      21      25
#        14      18      22      26

nodes: List[Node] = []
for i in range(0, 11):
  nodes.append(Hallway(i, i not in [2, 4, 6, 8]))
for i in range(0, 10):
  nodes[i].neighbours.append(nodes[i + 1])
for i in range(1, 11):
  nodes[i].neighbours.append(nodes[i - 1])

for hallwayIndex, target in [(2, 1), (4, 10), (6, 100), (8, 1000)]:
  siderooms = []
  for si in range(0, 4):
    sideroom = Sideroom(len(nodes), target)
    siderooms.append(sideroom)
    nodes.append(sideroom)
  
  nodes[hallwayIndex].neighbours.append(siderooms[0])
  siderooms[0].neighbours.append(nodes[hallwayIndex])

  for si in range(0, 3):
    siderooms[si].neighbours.append(siderooms[si + 1])
    siderooms[si].deeperNeighbour = siderooms[si + 1]
  for si in range(1, 4):
    siderooms[si].neighbours.append(siderooms[si - 1])

print("BURROW")
print()
print(nodes)
print()
print()

# Create the amphipods

UNIT_COSTS = {
  "A": 1,
  "B": 10,
  "C": 100,
  "D": 1000,
}

# amphipods: List[Amphipod] = []
locState: LocState = (
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1,
)

for i, row in enumerate(input):
  for j, name in enumerate(row):
    nodeIndex = 11 + i + (j * 4)
    locState = replaceIndex(locState, nodeIndex, UNIT_COSTS[name])

print("LOCSTATE")
print()
print(locState)
print()
print()

@lru_cache(maxsize=None)
def simulateStep(locState: LocState) -> List[State]:
  # prevCost, locState = state
  nextStates = []
  for locIndex, movingAmphipod in enumerate(locState):
    #print(locIndex, movingAmphipod)
    if movingAmphipod == -1:
      continue
    #print(movingAmphipod)
    if wantsToMove(movingAmphipod, nodes[locIndex], locState):
      steps = findAllowedSteps([nodes[locIndex]], movingAmphipod, locState)
      for targetNode, weight in steps:
        #print("    >> {}".format(targetNode))
        newLocState = replaceIndex(
          replaceIndex(locState, targetNode.i, movingAmphipod),
          locIndex,
          -1
        )
        nextStates.append((
          movingAmphipod * weight,
          newLocState
        ))
      #print(steps)
    #print()
  return nextStates

FINISHED: LocState = (
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  1, 1, 1, 1,
  10, 10, 10, 10,
  100, 100, 100, 100,
  1000, 1000, 1000, 1000,
)

def isFinished(state: LocState) -> bool:
  return state == FINISHED

COST_TO_NAME = {
  1: 'A',
  10: 'B',
  100: 'C',
  1000: 'D',
}

def printState(locState):
  print()
  s = ""
  for i in range(0, 11):
    a = COST_TO_NAME.get(locState[i])
    if a:
      s += a
    else:
      s += "."
  print(s)
  for row in range(0, 4):
    s = " "
    for i in range(11 + row, 11 + 4*4, 4):
      a = COST_TO_NAME.get(locState[i])
      if a:
        s += " " + a
      else:
        s += " ."
    print(s)
  print()

"""
states = [(0, amphipods)]
results = []
while not len(results):
  newStates = []
  print(len(states))
  states.sort(key=lambda s: s[0])
  #printState(states[0][1])
  print(states[0][0], states[-1][0])
  for prevState in states:
    printState(prevState[1])
    #print(prevState[0])
    if isFinished(prevState):
      print("FOUND A RESULT: {}".format(prevState))
      results.append(prevState[0])
      break
    else:
      newState = simulateStep(prevState)
      newStates.extend(newState)
  states = newStates

print(results)
print(min(results))
"""

count = 0
minResult = 9999999999

def recursive(i, prevCost: int, state: State) -> int:
  global count
  global minResult
  #print()
  #print(i, prevCost)
  #printState(state)
  if i < 2:
    print(i)
  if prevCost >= minResult:
    return 88888888888
  if isFinished(state):
    print("RESULT FOUND {}".format(state))
    #printState(state[1])
    if prevCost < minResult:
      minResult = prevCost
    return prevCost
  nextStates = simulateStep(state)
  if len(nextStates) == 0:
    # print("DEAD END")
    count = count + 1
    if count % 10000 == 0:
      print(count)
      print(minResult)
      printState(state)
    return 999999999999
  #for cost, s in nextStates:
  #  recursive(i + 1, prevCost + cost, s)
  return min(recursive(i + 1, prevCost + c, s) for c, s in nextStates)

result = recursive(0, 0, locState)
print("Result: {}".format(result))
print("MinResult: {}".format(minResult))

#print()
#print()
#nextS = simulateStep((0, locState))
#print(len(nextS))
#for s in nextS:
#  printState(s[1])
#printState(nextS[1])
#print(nextS)
#print()
#print(nextS[1][0].location)
#print()
#print(nextS[1][0].getAllowedSteps(nextS[1]))
#printState(amphipods)
