import re
from typing import final

FILE_NAME = './Day24/input.txt';

WHITE_TILE = "w"
BLACK_TILE = "b"


# Reads in the file, returns all our information
def parseFile():
  instructions = []
  
  with open(FILE_NAME, 'r') as file:
    
    # Read the data & split across newlines
    data = file.read()
    rawInstructions = data.split("\n")
    for ri in rawInstructions:
      if(ri):
        # Use a regular expression to split across the different directions
        split = re.split("(w)|(e)|(se)|(sw)|(nw)|(ne)", ri)
        # Filter out empty strings and NoneTypes
        filtered = [i for i in split if i]
        instructions.append(filtered)
    # for line in lines:
       
  return instructions

# Read in an instruction, read out a tuple (x, y, z) coordinate
# Based on the coordinate system defined here https://www.redblobgames.com/grids/hexagons/
def parseInstruction(instruction):
  x = 0 
  y = 0
  z= 0
  for direction in instruction:
    if(direction == "w"):
      x-=1
      y+=1
    elif(direction == "e"):
      x += 1
      y -= 1
    elif(direction == "ne"):
      x += 1
      z -= 1
    elif(direction == "sw"):
      x -= 1
      z += 1
    elif(direction == "nw"):
      z -= 1
      y += 1
    elif(direction == "se"):
      z += 1
      y -= 1
    else:
      print(direction, "is invalid")
  return (x, y, z)

# Calls parseInstructions on each instruction, and sets tile colors accordingly
def parseInstructions(instructions):
  tileMap = {}
  for instruction in instructions:
    vector = parseInstruction(instruction)
    # If we have seen this vector before and its value is currently black, it should be white next
    if(vector in tileMap and tileMap[vector] == BLACK_TILE):
      tileMap[vector] = WHITE_TILE
    # Otherwise, it should be black
    else:
      tileMap[vector] = BLACK_TILE
  return tileMap

# Count the number of black tiles surrounding this tile, use that information to determine the next color 
def getNextTileValue(tileMap, vec):
  # Parse out x, y, z from our tuple
  x, y, z = vec
  # Count black tiles
  blackTileCount = 0
  # Diffs for x, y, and z should all be different - one should be +1, one should be 0, one should be -1 at all times
  for xDiff in range(-1, 2):
    for yDiff in range(-1, 2):
      if(xDiff == yDiff):
        continue
      for zDiff in range(-1, 2):
        if(xDiff == zDiff or yDiff == zDiff):
          continue
        # If one of the vectors surrounding this one is black, add one to the tile count
        surroundingVec = (x + xDiff, y+yDiff, z+zDiff)
        if(surroundingVec in tileMap and tileMap[surroundingVec] == BLACK_TILE):
          blackTileCount+=1

  # Different rules based on current tile color
  if(vec in tileMap and tileMap[vec] == BLACK_TILE):
    return BLACK_TILE if blackTileCount == 1 or blackTileCount == 2 else WHITE_TILE
  return BLACK_TILE if blackTileCount == 2 else WHITE_TILE


def performArt(tileMap):
  # The next state of our tiles
  nextTileMap = {}

  # For each vector in our current map
  for vec in tileMap:
    # Update this vector's value
    nextTileMap[vec] = getNextTileValue(tileMap, vec)

    # check the surrounding vector's values if the current vector is white. Otherwise, don't bother 
    if(tileMap[vec] == BLACK_TILE):
      x, y, z = vec
      for xDiff in range(-1, 2):
        for yDiff in range(-1, 2):
          if(xDiff == yDiff):
            continue;
          for zDiff in range(-1, 2):
            if(xDiff == zDiff or yDiff == zDiff):
              continue;
            testVec = (x + xDiff, y + yDiff, z + zDiff)
            # But only update them if we aren't already checking it, and if its going to be black
            # Otherwise, we waste computations spinning off from white tiles
            if(not testVec in tileMap):
              value = getNextTileValue(tileMap, testVec)
              nextTileMap[testVec] = value
  return nextTileMap

# Calls perform art n times
def performArtNTimes(tileMap, n):
  currentTileMap = tileMap
  for i in range(0, n):
    currentTileMap = performArt(currentTileMap)
  return currentTileMap

# Counts the black tiles in the values portion of a dictionary
def countBlackTiles(tileMap):
  return list(tileMap.values()).count(BLACK_TILE);

def main():
  instructions = parseFile()

  print("--Part 1--")
  tileMap = parseInstructions(instructions)
  blackTileCount = countBlackTiles(tileMap)
  print(blackTileCount)

  print("--Part 2--")
  finalTileMap = performArtNTimes(tileMap, 100)
  print(countBlackTiles(finalTileMap))

main()