FILE_NAME="./Day14/input.txt" # File containing today's input
IGNORED_MASK_CHAR = 'X' # The character that gets ignored in the part 1 mask

class ProgramEntry:
  # Constructor, takes in mask, a string
  def __init__(self, mask):
    self.mask = mask
    self.memoryDictionary={}

  # Takes a memory address (int) and a value (int) and adds them to a dictionary
  def addItemToMemoryDictionary(self, address, value):
    self.memoryDictionary[address] = value

  # Given a string, a character, and an index, replaces the character at the index with the new character
  def __replaceIndex(self, string, character, index):
    return string[:index] + character + string[index + 1:]

  # Converts an integer to a binary string, padded with 0's up to length
  def __intToBinStr(self, integer, length):
    return str(bin(integer)).replace("0b", "").zfill(length)

  # Part 1 Solver
  def getMaskedMemoryAddresses(self):
    memoryAddresses = {} # Memory addresses / masked values found in this entry

    # Loop through each address
    for address in self.memoryDictionary:
      # Convert the value to a binary string
      value = self.__intToBinStr(self.memoryDictionary[address], 36)
      # In the mask, any time there is not an 'X', replace the character with the one in the mask
      for i in range(0, len(self.mask)):
        maskChar = self.mask[i]
        if(maskChar != IGNORED_MASK_CHAR):
          value = self.__replaceIndex(value, maskChar, i)
      # Add the masked value as an int to our addresses
      memoryAddresses[address] = int(value, 2)

    return memoryAddresses

  # Part 2 Solver
  def getDecodedMemoryAddresses(self):
    memoryAddresses = {} # Decoded Memory addresses / values found in this entry

    # Loop through each address
    for address in self.memoryDictionary:
      # Convert the address to binary
      binAddress = self.__intToBinStr(address, 36)
      # Loop through our mask
      for i in range(0, len(self.mask)):
        maskChar = self.mask[i]
        # If the current character isn't 0, replace the address's character with it
        if(maskChar != '0'):
          binAddress = self.__replaceIndex(binAddress, maskChar, i)

      # Get all possible addresses and add them to the decoded dictionary
      for decodedAddress in self.__getAllAddresses(binAddress):
        memoryAddresses[decodedAddress] = self.memoryDictionary[address]
    
    return memoryAddresses

  # Helper for part 2 - recursively finds all 'X's in the address and replaces them with '0' or '1' and returns all of them
  def __getAllAddresses(self, stringAddress, index = 0):
    # If we are at the end of the string, return it as an integer
    if(index >= len(stringAddress)):
      return [int(stringAddress, 2)];
    # Otherwise...
    else:
      # If we are at an X, compute where X=1 and X=0, and return both arrays
      if(stringAddress[index] == 'X'):
        replacedOne = self.__replaceIndex(stringAddress, '0', index)
        replacedTwo = self.__replaceIndex(stringAddress, '1', index)
        return self.__getAllAddresses(replacedOne, index + 1) + self.__getAllAddresses(replacedTwo, index + 1)
      # Continue the recursive function
      else:
        return self.__getAllAddresses(stringAddress, index + 1)
        
  # To String function. For debugging purposes
  def __str__(self):
    return self.mask + ": " + str(self.memoryDictionary)

def parseFile():
  # Create our array of entries
  entries = []

  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    lines = data.split('\n')

    # Parse each line into our program entry array
    entry = None
    for line in lines:
      if(line):
        splitLine = line.split(" = ")
      
        # We are at a new entry
        if(splitLine[0] == "mask"):
          # If the entry already exists (not the first run) add it to the array
          if(entry):
            entries.append(entry)
          # Create a new entry and set the mask in
          entry = ProgramEntry(splitLine[1])
        else:
          # Parse the memory and the value into integers
          memory = int(splitLine[0].replace("mem[", "").replace("]", ""))
          value = int(splitLine[1])
          entry.addItemToMemoryDictionary(memory, value)

    # Add our final entry
    entries.append(entry)
  return entries

def followMemoryInstructions(entries, isPart1):
  memory = {}
  for entry in entries:
    # merge memory with the values from the entry
    newMemory = {}

    # Call part 1 or part 2 functions for the entry
    if isPart1:
      newMemory = entry.getMaskedMemoryAddresses()
    else:
      newMemory = entry.getDecodedMemoryAddresses()
    
    # Merge our memory with the new memory entries. New memories will replace old ones
    memory = {**memory, **newMemory }
  
  # Count each value present and return it
  total = 0
  for key in memory:
    total += memory[key]
    
  return total

def main():
  programEntries = parseFile()

  print("--Part 1--")
  sumMaskedMemoryValues = followMemoryInstructions(programEntries, True)
  print("Sum = " + str(sumMaskedMemoryValues))

  print("--Part 2--")
  sumDecodedMemoryValues = followMemoryInstructions(programEntries, False)
  print("Sum = " + str(sumDecodedMemoryValues))
main()