import sys
import string
from typing import List, Tuple

# Read input

readFile = True
splitLines = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

input = input.splitlines()

# Calculate result

class Packet:
  version: int
  id: int
  lastBitIndex: int

  def __init__(self, version , id):
    self.version = version
    self.id = id

  def versionSum(self) -> int:
    raise Exception("versionSum() was not implemented")

  def value(self) -> int:
    raise Exception("value() was not implemented")

class Literal(Packet):
  _value = None

  def __init__(self, version, id, bits):
    super().__init__(version, id)
    print(" - Parsing literal content: " + bits)
    valueBits = ""
    left = str(bits)
    last = False
    while not last:
      if left[0] == "0":
        last = True
      valueBits += left[1:5]
      left = left[5::]
    self._value = int(valueBits, 2)
    self.lastBitIndex = len(bits) - len(left)
    print("   > integer value: " + str(self._value) + ", lastBitIndex was " + str(self.lastBitIndex))

  def versionSum(self):
    return self.version

  def value(self):
    return self._value

  def __repr__(self):
    return "━━━━ Literal {} (version: {})".format(self._value, self.version)

class Operator(Packet):
  subpackets: List[Packet] = None
  lengthTypeId: str = None

  def __init__(self, version, id, bits):
    super().__init__(version, id)
    self.subpackets = []
    print(" - Parsing op content ______" + bits)
    self.lengthTypeId = bits[0]
    print("   > LengthTypeId: " + self.lengthTypeId)
    if self.lengthTypeId == "0":
      subpacketTotalLength = int(bits[1: 15 + 1], 2)
      print("   > totalLength: " + str(subpacketTotalLength) + "      (" + bits[1: 15 + 1] + ")")
      firstBit = 15 + 1
      while (firstBit < subpacketTotalLength + 15):
        print("   > START SUBPACKET " + bits[firstBit::])
        subpacket, lastBitIndex = parsePacket(bits[firstBit::])
        self.subpackets.append(subpacket)
        firstBit += lastBitIndex
      
    else:
      subpacketCount = int(bits[1: 11 + 1], 2)
      print("  > subpacket count: " + str(subpacketCount) + "      (" + bits[1: 11 + 1] + ")")
      firstBit = 11 + 1
      while (len(self.subpackets) < subpacketCount):
        print("   > START SUBPACKET  " + bits[firstBit::])
        subpacket, lastBitIndex = parsePacket(bits[firstBit::])
        self.subpackets.append(subpacket)
        firstBit += lastBitIndex
        
    self.lastBitIndex = firstBit

  def versionSum(self):
    return self.version + sum([s.versionSum() for s in self.subpackets])

  def value(self):
    if self.id == 0:
      return sum([s.value() for s in self.subpackets])
    elif self.id == 1:
      p = 1
      for s in self.subpackets:
        p = p * s.value()
      return p
    elif self.id == 2:
      return min([s.value() for s in self.subpackets])
    elif self.id == 3:
      return max([s.value() for s in self.subpackets])
    elif self.id == 5:
      assert(len(self.subpackets) == 2)
      return 1 if self.subpackets[0].value() > self.subpackets[1].value() else 0
    elif self.id == 6:
      assert(len(self.subpackets) == 2)
      return 1 if self.subpackets[0].value() < self.subpackets[1].value() else 0
    elif self.id == 7:
      assert(len(self.subpackets) == 2)
      return 1 if self.subpackets[0].value() == self.subpackets[1].value() else 0
  
  def __repr__(self):
    s = "━━┳━ Operator #{} (version: {}, lengthType: {})\n".format(self.id, self.version, self.lengthTypeId)
    for si, sub in enumerate(self.subpackets):
      s += "  ┃\n"
      for i, line in enumerate(sub.__repr__().split('\n')):
        if si == len(self.subpackets) - 1:
          if i == 0:
            s += "  ┗" + line + "\n"
          else:
            s += "   " + line + "\n"
        else:
          if i == 0:
            s += "  ┣" + line + "\n"
          else:
            s += "  ┃" + line + "\n"
    return s.strip()

def parsePacket(bits: str) -> Tuple[Packet, int]:
  version = int(bits[0:3], 2)
  id = int(bits[3:6], 2)
  print()
  print("Parsing packet:     " + bits)
  print(" > version " + str(version))
  print(" > id " + str(id))
  if id == 4:
    packet = Literal(version, id, bits[6::])
  else:
    packet = Operator(version, id, bits[6::])
  return packet, packet.lastBitIndex + 6

def convertFromHex(line):
  b = bin(int(line, 16))[2::]
  while len(b) < len(line) * 4:
    b = "0" + b
  return b

# 1

print(convertFromHex(input[0]))

packets = [parsePacket(convertFromHex(line))[0] for line in input]

for p in packets:
  print()
  print(p)
  print(p.versionSum())
  print()

result = sum([p.versionSum() for p in packets])
print("Result: {}".format(result))

# 2

result = packets[0].value()
print("Result: {}".format(result))