INPUT = [8,7,1,3,6,9,4,5,2] # Today's input

# Class that defines a single cup (It's a linked list)
class Cup:
  # Set my value
  def __init__(self, number):
    self.num = number
  
  # Getters and setters for the link to the next Cup
  def setNext(self, next):
    self.nextCup = next

  def getNext(self):
    return self.nextCup

# Stores state & contains functions for the Cup game
class CupState:
  def __init__(self, inputArr):
    # Map values to Cups
    cupDict = {}

    # Loop through our input, construct cups, and set the links in the linked list
    prevCup = None
    for num in inputArr:
      cup = Cup(num)
      cupDict[num] = cup

      if(prevCup):
        prevCup.setNext(cup)
      else:
        self.currentCup = cup

      prevCup = cup
    # Surprise! Its a circular list. Last links back to the first
    prevCup.setNext(self.currentCup)

    self.cupDict = cupDict

  # Removes the next N cups from the circle, starting at the current cup
  def __removeNCups__(self, n):
    removedCups = []
    cupIter = self.currentCup
    # Loop through the next N cups, adding each cup to the removedCups array
    for i in range(0, n):
      nextCup = cupIter.getNext()
      removedCups.append(nextCup)
      cupIter = nextCup

    # Update the link from the currentCup to the next cup after the removed ones
    link = removedCups[n-1].getNext()
    self.currentCup.setNext(link)
    removedCups[n-1].setNext(None)

    return removedCups

  # Add the cups in cupList to the end of cup, linking up both sides
  def __addCups__(self, cup, cupList):
    link = cup.getNext()

    cup.setNext(cupList[0])
    cupList[len(cupList)-1].setNext(link)

  # Returns true if num is one of the value present in cup list
  def __cupNumInCupList__(self, num, cupList):
    for cup in cupList:
      if(cup.num == num):
        return True
      
    return False
  
  def simulateRound(self):
    # Remove our cups
    removedCups = self.__removeNCups__(3)

    # Find our next number
    nextNumber = self.currentCup.num - 1
    # Our next number must be greater than 0, and not have been removed from the loop
    while(nextNumber <= 0 or self.__cupNumInCupList__(nextNumber, removedCups)):
      # Subtract 1 to try the next
      nextNumber -= 1
      # If we are below our valid numbers, loop back to the top and try from there
      if(nextNumber <= 0):
        nextNumber = max(self.cupDict.keys())

    # Readd the removed cups at the found number
    self.__addCups__(self.cupDict[nextNumber], removedCups)
    # Select the next cup
    self.currentCup = self.currentCup.getNext()

  # Runs simulateRound n times
  def simulateNRounds(self, n):
    for i in range(0, n):
      self.simulateRound()

  # Starts at cup 1, concatenates all the cup labels from there 
  def getPart1Answer(self):
    oneCup = self.cupDict[1]
    combinedNumbers = ""
    currentCup = oneCup.getNext()
    while(currentCup.num != oneCup.num):
      combinedNumbers += str(currentCup.num)
      currentCup = currentCup.getNext()

    return combinedNumbers

  # Starts at cup 1, gets the product of the next two cup labels
  def getPart2Answer(self):
    oneCup = self.cupDict[1]
    cup1 = oneCup.getNext()
    cup2 = cup1.getNext()
    return cup1.num * cup2.num

# Helps generate all the extra numbers for part 2
def generatePart2Array(inputArray, totalCups):
  newArray = inputArray.copy()
  counter = max(inputArray) + 1

  while(len(newArray) < totalCups):
    newArray.append(counter)
    counter+=1

  return newArray

def main():
  cupState = CupState(INPUT)
  cupState2 = CupState(generatePart2Array(INPUT, 1000000))

  print("--Part 1--")
  cupState.simulateNRounds(100)
  print(cupState.getPart1Answer())

  print("--Part 2--")
  cupState2.simulateNRounds(10000000)
  print(cupState2.getPart2Answer())

main()