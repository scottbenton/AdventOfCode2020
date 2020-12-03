# File containing the expense report
FILENAME = "./expense-report.txt"
# The winning number to reach
WINNING_NUMBER = 2020

# Helper function for parsing the file
def readFile(filepath):
  with open(filepath, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    splitData = data.split("\n")

    # Convert strings to numbers, drop any empty strings
    numberList = []
    for data in splitData:
      if(len(data) > 0):
        numberList.append(int(data))
    
    # Return the number list
    return numberList

# Part 1 Solution
def findTwoEntryWinner(numberList):
  for i in range(0, len(numberList) - 1):
    numI = numberList[i]
    for j in range(i + 1, len(numberList)):
      numJ = numberList[j]
      if (numI + numJ == WINNING_NUMBER):
        print(numI * numJ)

# Part 2 Solution
def findThreeEntryWinner(numberList):
  for i in range(0, len(numberList) - 2):
    numI = numberList[i]
    for j in range(i + 1, len(numberList)-1):
      numJ = numberList[j]
      for k in range(j + 1, len(numberList)):
        numK = numberList[k]
        if (numI + numJ + numK == WINNING_NUMBER):
          print(numI * numJ * numK)

# Recursive solution for N entries
def findNEntryWinner(numberList, n):
  counterList = [0] * n
  recursiveNEntryWinner(numberList, counterList, 0)

def recursiveNEntryWinner(numberList, counterList, index):
  # Base Case - if we are past the end of the counterList, check if we match the winning number
  if (index == len(counterList)):

    # Keep track of the total and the product for our current counter locations
    total = 0
    product = 1
    for counter in counterList:
      num = numberList[counter]
      total += num
      product *= num

    # If the total matches our winning number, print the product
    if (total == WINNING_NUMBER):      
      print(product)

  # If we aren't at the base case just yet
  else:
    # Figure out where our counter should start (0 for first index)
    counterStart = 0
    if (index > 0):
      # And 1 + the previous counter in the list for other indexes
      # For example if the first counter is currently at 2, we can start the second
      # counter at 3 so that we don't check the same numbers against each other
      # Since we don't care about permutations for addition and multiplication, 
      # we can use this method to only check unique combinations of numbers
      counterStart = counterList[index - 1] + 1

    # Figure out where the counter should end
    # Earlier numbers should end earlier so that we don't check the same numbers against each other
    counterEnd = len(numberList) - (len(counterList) - index + 1)

    # Check each number in the range we just created
    for i in range(counterStart, counterEnd):
      # Set our current counter
      counterList[index] = i
      # Call the recursive function for the next counter down
      recursiveNEntryWinner(numberList, counterList, index + 1)

def main():
  numbers = readFile(FILENAME)
  
  print("--TWO ENTRY WINNER--")
  findTwoEntryWinner(numbers)
  print("--THREE ENTRY WINNER--")
  findThreeEntryWinner(numbers)

  print("--RECURSIVE TWO ENTRY WINNER--")
  findNEntryWinner(numbers, 2)
  print("--RECURSIVE THREE ENTRY WINNER--")
  findNEntryWinner(numbers, 3)


main()