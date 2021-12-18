import sys
import math
from functools import reduce
import copy

# Read input

readFile = True
splitLines = True


if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()


# Calculate result

class Node:
  parent: 'Node'
  depth: int

  def __init__(self, parent: 'Node'):
    self.parent = parent
    self.depth = parent.depth + 1 if parent else 0

  def updateDepth(self):
    if not self.parent:
      self.depth = 0
    else:
      self.depth = self.parent.depth + 1


class Pair(Node):
  left: Node
  right: Node

  def __init__(self, parent: Node, left: Node, right: Node):
    super().__init__(parent)
    self.left = left
    self.right = right
    if left:
      left.parent = self
    if right:
      right.parent = self

  def addNode(self, node: Node):
    if not self.left:
      self.left = node
      node.parent = self
    elif not self.right:
      self.right = node
      node.parent = self
    else:
      raise Exception("This node is already full")

  def updateDepth(self):
    super().updateDepth()
    if self.left:
      self.left.updateDepth()
    if self.right:
      self.right.updateDepth()

  def __repr__(self):
    return "[{},{}]".format(self.left, self.right)


class Regular(Node):
  value: int

  def __init__(self, parent: Node, value: int):
    super().__init__(parent)
    self.value = value

  def __repr__(self):
    return "{}".format(self.value)


def createTree(input):
  tree = None
  prev = None
  for i, char in enumerate(input):
    if char == "[" and i == 0:  # first character
      root = Pair(None, None, None)
      tree = root
      prev = root
    elif char == "[":  # start of a pair
      newPair = Pair(prev, None, None)
      prev.addNode(newPair)
      prev = newPair
    elif char in "0123456789":  # number
      if type(prev) == Pair:
        newRegular = Regular(prev, int(char))
        prev.addNode(newRegular)
        prev = newRegular
      elif type(prev) == Regular:
        prev.value = prev.value * 10 + int(char)
      else:
        raise Exception(
          "Encountered number in string while the previous node was not a Pair or a Regular (it was {})".format(type(prev)))
    elif char == ",":
      prev = prev.parent
    elif char == "]":
      prev = prev.parent
    else:
      raise Exception(
        "Encountered unknown character {} in string at index {}".format(char, i))
  return tree


def findPairToExplode(curr: Node) -> Pair:
  """Find the leftmost pair which has depth 4. By the rules this is guaranteed to be a pair of two regulars."""
  if type(curr) == Pair and curr.depth == 4:
    return curr
  if type(curr) == Pair:
    l = findPairToExplode(curr.left)
    if l:
      return l
    r = findPairToExplode(curr.right)
    if r:
      return r
  return None


def findNextRegularToRight(curr: Node) -> Regular:
  # reached root node without finding anything
  if not curr.parent:
    return None
  # if curr is right child of parent
  elif curr.parent.right == curr:
    return findNextRegularToRight(curr.parent)
  # if found the nearest parent from where we can move to right
  elif curr.parent.left == curr:
    c = curr.parent.right
    while type(c) == Pair:
      c = c.left
    return c
  else:
    return None


def findNextRegularToLeft(curr: Node) -> Regular:
  # reached root node without finding anything
  if not curr.parent:
    return None
  # if curr is left child of parent
  elif curr.parent.left == curr:
    return findNextRegularToLeft(curr.parent)
  # if found the nearest parent from where we can move to left
  elif curr.parent.right == curr:
    c = curr.parent.left
    while type(c) == Pair:
      c = c.right
    return c
  else:
    return None


def replaceInParent(curr: Node, replaceWith: Node) -> None:
  """Replace the current node with another one. Takes care of the parent-child relations."""
  replaceWith.parent = curr.parent
  if curr == curr.parent.left:
    curr.parent.left = replaceWith
  elif curr == curr.parent.right:
    curr.parent.right = replaceWith
  else:
    raise Exception(
      "Node {} was neither child of its parent {}".format(curr, curr.parent))


def findRegularToSplit(curr: Node) -> Regular:
  """Find the leftmost regular number which is 10 or larger"""
  if type(curr) == Regular and curr.value >= 10:
    return curr
  if type(curr) == Pair:
    l = findRegularToSplit(curr.left)
    if l:
      return l
    r = findRegularToSplit(curr.right)
    if r:
      return r
  return None


def reduceTree(tree: Node) -> None:
  """Reduce the tree as much as possible. Mutates the original tree."""
  while True:
    explode = findPairToExplode(tree)
    if explode:
      l = findNextRegularToLeft(explode)
      r = findNextRegularToRight(explode)
      if l:
        l.value += explode.left.value
      if r:
        r.value += explode.right.value
      replaceInParent(explode, Regular(None, 0))
      explode.parent.updateDepth()
      continue

    split = findRegularToSplit(tree)
    if split:
      newPair = Pair(
        split.parent,
        Regular(None, math.floor(split.value / 2)),
        Regular(None, math.ceil(split.value / 2))
      )
      replaceInParent(split, newPair)
      split.parent.updateDepth()
      continue

    # If nothing was exploded or split, we break out of the loop
    break
  pass

def calcMagnitude(curr: Node) -> int:
  if type(curr) == Regular:
    return curr.value
  elif type(curr) == Pair:
    return 3 * calcMagnitude(curr.left) + 2 * calcMagnitude(curr.right)
  else:
    return 0
  

trees = [createTree(row) for row in input]

for tree in trees:
  reduceTree(tree)

# 1

def sumNumbers(tree1, tree2):
  t1c = copy.deepcopy(tree1)
  t2c = copy.deepcopy(tree2)
  s = Pair(None, t1c, t2c)
  s.updateDepth()
  reduceTree(s)
  return s

total = reduce(sumNumbers, trees)

result = calcMagnitude(total)
print("Result: {}".format(result))

# 2
largest = 0
for t1 in trees:
  for t2 in trees:
    if t1 == t2:
      continue
    m = calcMagnitude(sumNumbers(t1, t2))
    if m > largest:
      largest = m

result = largest
print("Result: {}".format(result))
