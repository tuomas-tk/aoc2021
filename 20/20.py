import sys
import numpy as np

# Read input

readFile = True

if readFile:
  input = open('in', 'r').read().strip()
else:
  input = sys.stdin.read().strip()

algorithm, image = input.split('\n\n')
algorithm = np.array([1 if x == '#' else 0 for x in algorithm])
image = np.array([[1 if x == '#' else 0 for x in row] for row in image.splitlines()])

# Calculate results

kernel = 2 ** np.arange(9)[::-1].reshape(3, 3)

def printImg(image):
  s = ""
  for row in image:
    s += "".join(['██' if pixel > 0 else '  ' for pixel in row]) + "\n"
  sys.stdout.write(s)

for loop in range(50):
  nextImg = np.pad(np.zeros_like(image, dtype=bool), 1)
  image = np.pad(image, 2, constant_values=image[0,0])
  for y in range(0, len(image) - 2):
    for x in range(0, len(image) - 2):
      part = image[y : y + 3, x : x + 3]      
      nextImg[y, x] = algorithm[(part * kernel).sum()]
  image = nextImg
  if loop + 1 in [2, 50]:
    result = image.sum()
    print("Result at {} iterations: {}".format(loop + 1, result))
  #print()
  #print(loop)
  #printImg(image)