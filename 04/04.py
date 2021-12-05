# 1
BOARD_SIZE = 5

input = open('in', 'r').read().strip().split('\n\n')

numbers = [int(s) for s in input[0].split(',')]
boards = [[[int(n) for n in row.split()] for row in b.splitlines()] for b in open('in', 'r').read().strip().split('\n\n')[1:]]
marked = []

def countMaxResult(board, marked):
  c = [0] * BOARD_SIZE
  r = [0] * BOARD_SIZE
  s = 0
  for ci in range(BOARD_SIZE):
    for ri in range(BOARD_SIZE):
      if (board[ri][ci] in marked):
        c[ci] += 1
        r[ri] += 1
      else:
        s += board[ri][ci]
  return max(max(c), max(r)), s


print(numbers)
print(boards)
print()

for i in range(len(numbers)):
  boardResults = [sum for maxRes, sum in [countMaxResult(board, numbers[0:(i+1)]) for board in boards] if maxRes == BOARD_SIZE]
  if (len(boardResults) > 0):
    result = boardResults[0] * numbers[i]
    break

print("Result: {}".format(result))


# 2

print()

hasWon = [False] * len(boards)
for i in range(len(numbers)):
  boardResults = [(maxRes, sum) for maxRes, sum in [countMaxResult(board, numbers[0: (i + 1)]) for board in boards]]
  for bi in range(len(boards)):
    maxRes, sum = boardResults[bi]
    if maxRes == BOARD_SIZE:
      if not hasWon[bi]:
        hasWon[bi] = True
        if all(hasWon):
          result = sum * numbers[i]
          break

print("Result: {}".format(result))