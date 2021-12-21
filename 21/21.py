import sys
from typing import Tuple
from functools import lru_cache
from collections import deque, defaultdict
from itertools import count

# Read input

readFile = True
splitLines = False
splitWords = True
convertToNumbers = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = [int(row.split(": ")[1]) for row in input.splitlines()]


# Calculate result

# 1

dice = count(1)

class Player:
  score = 0
  pos = 0
  def __init__(self, pos):
    self.pos = pos - 1
  def move(self, d):
    self.pos = (self.pos + d) % 10
    self.score += self.pos + 1

players = deque(Player(pos) for pos in input)

while all(p.score < 1000 for p in players):
  d = next(dice) + next(dice) + next(dice)
  p = players.popleft()
  p.move(d)
  players.append(p)

result = min(p.score for p in players) * (next(dice) - 1)
print("Result: {}".format(result))


# 2

DICE = [1, 2, 3]
LIMIT = 21

# precalculate the amounts of different possible sums of three Dirac dice
diceSumCounts = defaultdict(int)
for d1 in DICE:
  for d2 in DICE:
    for d3 in DICE:
      s = d1 + d2 + d3
      diceSumCounts[s] += 1

@lru_cache(maxsize=None)
def findWinnerCount(score1, score2, pos1, pos2) -> Tuple[int, int]:
  if score2 >= LIMIT:
    return (0, 1)

  winCount1 = 0
  winCount2 = 0
  for d, c in diceSumCounts.items():
    newPos1 = (pos1 + d) % 10
    newScore1 = score1 + newPos1 + 1
    win1, win2 = findWinnerCount(score2, newScore1, pos2, newPos1)
    winCount1 += win2 * c
    winCount2 += win1 * c
  return winCount1, winCount2

win1, win2 = findWinnerCount(0, 0, input[0] - 1, input[1] - 1)

result = max(win1, win2)
print("Result: {}".format(result))