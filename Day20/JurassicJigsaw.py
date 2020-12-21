import math
FILE_NAME = "./Day20/input.txt"
SEA_MONSTER = [
  "                  # ",
  "#    ##    ##    ###",
  " #  #  #  #  #  #   "
] # Sea monster shape

# Class for storing the sea monster
class SeaMonster:
  def __init__(self):
    self.length = len(SEA_MONSTER[0])
    self.height = len(SEA_MONSTER)
    seaMonsterIndexes = []
    # Find each instance of # and store its x index in a 2d array
    for line in SEA_MONSTER:
      seaMonsterIndexes.append(self.__findAllIndexes__(line))
    self.indexes = seaMonsterIndexes

  def __findAllIndexes__(self, str):
    return [i for i, ltr in enumerate(str) if ltr == "#"]

  def getDimensions(self):
    return self.length, self.height
  
  def getIndexes(self):
    return self.indexes

# Class for each tile
class Tile:
  # Init & getters for the id of the tile and the image present
  def __init__(self, id, image):
    self.id = id
    self.img = image

  def getImage(self):
    return self.img

  def getId(self):
    return self.id

  # Getters for each side of the image
  def getTopSide(self):
    return self.img[0]

  def getRightSide(self):
    return [row[len(self.img) - 1] for row in self.img]

  def getBottomSide(self):
    return self.img[len(self.img) - 1]

  def getLeftSide(self):
    return [row[0] for row in self.img]

  # Flips the image along the vertical axis
  def flipVertical(self):
    self.img = self.img[::-1]

  # Rotates the image 90 deg clockwise
  def rotate(self):
    self.img = list(zip(*self.img[::-1]))

# Reads in the file, returns all our information
def parseFile():
  tiles = {}
  
  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    lines = data.split('\n')

    tileKey = 0
    tileLines = []
    for line in lines:
      # We're starting a new tile
      if("Tile" in line):
        tileKey = int(line.strip("Tile :"))
      elif(line):
        tileLines.append(line)
      # We are ending a tile
      else:
        tiles[tileKey]= Tile(tileKey, tileLines.copy())
        tileKey=0
        tileLines.clear()
        
  return tiles

# Returns true if the given tile fits in x, y in the array, false otherwise
def checkTileFit(image, tile, x, y):
  # If we are at the first spot, it will fit
  if(x == 0 and y == 0):
    return True
  
  # Since we always add to the bottom or right, these are the only two sides we may need to check
  checkTop = True
  checkLeft = True

  # Only check top
  if(x == 0): 
    checkLeft = False
  # Only check left
  if(y == 0):
    checkTop = False
    
  # Check the sides. If either doesn't work, return false
  if(checkTop):
    if(image[y-1][x].getBottomSide() != tile.getTopSide()):
      return False
  if(checkLeft):
    if(image[y][x-1].getRightSide() != tile.getLeftSide()):
      return False
  return True
  
# Backtracking algorithm to find an image where the borders match
def findWorkingImage(tiles, unusedTileKeys, dimensions, currentImage, x=0, y=0):
  if(len(unusedTileKeys) == 0):
    return currentImage
  else:
    for tileKey in unusedTileKeys:
      tile = tiles[tileKey]
      for i in range(0, 2):
        # Try all flips
        tile.flipVertical()
        for j in range(0, 4):
          # This tile fits here
          if(checkTileFit(currentImage, tile, x, y)):
            nextImage = copy2DArray(currentImage)
            nextImage[y][x] = tile
            nextTileKeys = unusedTileKeys.copy()
            nextTileKeys.remove(tileKey)
            nextX = int((x + 1) % dimensions)
            nextY = y + 1 if nextX == 0 else y
            result = findWorkingImage(tiles, nextTileKeys, dimensions, nextImage, nextX, nextY)
            if(result != -1):
              return result
          # If it doesn't fit, rotate it
          tile.rotate()
  return -1

# Makes a copy of a 2D array
def copy2DArray(array):
  newArray = []
  for list in array:
    subArray = []
    for item in list:
      subArray.append(item)
    newArray.append(subArray)
  return newArray

# Constructs an empty 2D array with the default value set
def construct2DArray(defaultValue, dimensions):
  return [[defaultValue for i in range(dimensions)] for j in range(dimensions)]

# DEBUG - prints out the 2D Tile image array
def printTiles(img):
  for list in img:
    for tile in list:
      if(tile):
        print(tile.getId(), end="\t")
      else:
        print("-", end="\t")
    print()

# DEBUG - prints out a 2D array
def print2DArray(arr):
  for y in arr:
    for x in y:
      print(x, end="")
    print()
  
# Solves part 1 once we have our image
def getProductOfCorners(image):
  max = len(image) -1;
  return image[0][0].getId() * image[0][max].getId() * image[max][0].getId() * image[max][max].getId()

# Removes the borders and combines the remainder
def combineImage(imageArray):
  image = []
  innerDimension = len(imageArray[0][0].getImage())
  outerDimension = len(imageArray)
  dimension = outerDimension * innerDimension

  for y in range(dimension):
    yArr = []
    outerY = math.floor(y / innerDimension)
    innerY = y % innerDimension
    for x in range(dimension):
      outerX = math.floor(x / innerDimension)
      innerX = x % innerDimension

      shouldAdd = True

      if(innerX == 0 or innerX == innerDimension - 1):
        shouldAdd = False
      elif(innerY == 0 or innerY == innerDimension - 1):
        shouldAdd = False

      if(shouldAdd):
        outerImage = imageArray[outerY][outerX].getImage()
        yArr.append(outerImage[innerY][innerX])

    if(len(yArr) > 0):
      image.append(yArr)

  return image

# Finds all instances of sea monsters in the image, returns the number of # that aren't a part of the sea monster
def findSeaMonster(image, monster):
  monsterCount = 0
  imageCopy = copy2DArray(image)

  width, height = monster.getDimensions()
  indexes = monster.getIndexes()
  iterationCount = 0
  while(iterationCount < 8):
    for y in range(0, len(imageCopy) - height):
      for x in range(0, len(imageCopy[0]) - width):
        invalid = False
        for checkY in range(len(indexes)):
          for checkX in indexes[checkY]:
            if(not (imageCopy[y + checkY][x + checkX] == '#' or imageCopy[y + checkY][x + checkX] == 'O')):
              invalid = True
              break
          if(invalid):
            break;
        if(not invalid):
          monsterCount+=1
          for checkY in range(len(indexes)):
            for checkX in indexes[checkY]:
              if(imageCopy[y + checkY][x + checkX] != 'O'):
                imageCopy[y+checkY][x+checkX] = 'O'


    # Rotate image
    if(iterationCount% 2 == 0):
      imageCopy = imageCopy[::-1]
    imageCopy = list(zip(*imageCopy[::-1]))
    iterationCount += 1

  unaffiliatedCount = 0
  for y in range(len(imageCopy)):
    for x in range(len(imageCopy[0])):
      if(imageCopy[y][x] == '#'):
        unaffiliatedCount += 1

  return unaffiliatedCount

def main():
  tiles = parseFile()
  
  keyList = [];
  for tileKey in tiles:
    keyList.append(tileKey)

  emptyImage = construct2DArray(None, int(math.sqrt(len(tiles))))

  print("--Part 1--")
  image = findWorkingImage(tiles, keyList, math.sqrt(len(tiles)), emptyImage)
  printTiles(image)
  corners = getProductOfCorners(image)
  print("Product of corner ids =", corners)

  print("--Part 2--")
  combinedImage = combineImage(image)
  # print2DArray(combinedImage)
  monsterCount = findSeaMonster(combinedImage, SeaMonster())
  print("Count of untouched #'s =", monsterCount)
main()