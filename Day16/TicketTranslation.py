FILE_NAME="./Day16/input.txt"

class Field:
  def __init__(self, name, range1, range2):
    # Name of the rule
    self.name = name 
    # Min and max for first range
    range1Split = range1.split("-")
    self.range1Min = int(range1Split[0])
    self.range1Max = int(range1Split[1])
    # Min and max for second range
    range2Split = range2.split("-")
    self.range2Min = int(range2Split[0])
    self.range2Max = int(range2Split[1])
    # For part 2, the possible indexes that this field could be
    self.possibleIndexes = []

  # Given a number, is that number in either range?
  def isNumberInRange(self, number):
    inRange1 = self.range1Min <= number <= self.range1Max
    inRange2 = self.range2Min <= number <= self.range2Max
    return inRange1 or inRange2

  # Return the name
  def getName(self):
    return self.name
  
  # Given the length of list, set possible indexes to that length
  def setPossibleIndexes(self, listLen):
    self.possibleIndexes = list(range(listLen))

  # Remove an index from contention
  def removePossibleIndex(self, index):
    self.possibleIndexes.remove(index)
  
  # Returns the list of possible indexes
  def getPossibleIndexes(self):
    return self.possibleIndexes
  
  # To string
  def __str__(self):
    return self.name + ": (" + str(self.range1Min) + ", " + str(self.range1Max) + ") or (" + str(self.range2Min) + ", " + str(self.range2Max) + ")"  
  # Comparator
  def __lt__(self, other):
    return len(self.possibleIndexes) < len(other.possibleIndexes)

# Reads in the file, returns all our information
def parseFile():
  fieldRules = [] # An array of rules
  myTicket = [] # An array of numbers
  otherTickets = [] # An array of arrays of numbers
  
  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    lines = data.split('\n')

    stage = 1 # Which step are we on?
    for line in lines:
      if(line):
        # If we are in stage 1, we need to construct our Field
        if(stage == 1):
          splitNameFromRanges = line.split(": ")
          name = splitNameFromRanges[0]
          ranges = splitNameFromRanges[1].split(" or ")
          fieldRules.append(Field(name, ranges[0], ranges[1]))
          
        # If we are in stage two or three, parse the line into an array of numbers
        else:
          if(not "ticket" in line): 
            splitLine = [int(num) for num in line.split(",")]
            if(stage == 2):
              myTicket = splitLine
            else:
              otherTickets.append(splitLine)
      else:
        stage += 1

  return fieldRules, myTicket, otherTickets

# For each field, check if the given number is valid
def isNumberValid(fields, number):
  for field in fields:
    if(field.isNumberInRange(number)):
      return True
  return False    

# Part 1 solution
def checkTicketScanErrorRate(fields, ticketList):
  errorRate = 0 # Total error rate

  # Loop through each number in each ticket and check its validity
  for ticket in ticketList:
    for number in ticket:
      # If the number is invalid, add it to the error
      if(not isNumberValid(fields, number)):
        errorRate += number
  
  return errorRate

# Filter out tickets where a totally invalid number exists
def filterTickets(fields, ticketList):
  newList = []
  for ticket in ticketList:
    isTicketValid = True
    for number in ticket:
      if(not isNumberValid(fields, number)):
        isTicketValid = False
        break
    if(isTicketValid):
      newList.append(ticket)

  return newList

# Searches for a solution where each index is assigned to a rule by backtracking
def backtrackIndexes(rules, ruleIndex = 0, usedIndexes = []):
  # Base case 1 - if we have hit the end, we have found a solution. Return a dictionary
  if(ruleIndex == len(rules)):
    return {}
  
  # Get our choices - the possible indexes for the current rule that haven't been used yet
  indexChoices = [i for i in rules[ruleIndex].getPossibleIndexes() if i not in usedIndexes]

  # Loop through our choices and try each index as the current value
  for index in indexChoices:
    resp = backtrackIndexes(rules, ruleIndex + 1, usedIndexes + [index])
    # If the index succeeds, add this index to our solution and return it
    if(resp != False):
      resp[index] = rules[ruleIndex].getName()
      return resp
  # If none of the choices worked, one of the previous choices was bad, lets backtrack
  return False

# Finds the indexes for each given field
def findFieldIndexes(fields, ticketList):
  # Filter "bad" tickets out
  filteredTickets = filterTickets(fields, ticketList)
  # Get the length of tickets
  ticketLength = len(filteredTickets[0])

  for field in fields:
    # Default the list of possible indexes to all indexes
    field.setPossibleIndexes(ticketLength)
    # Loop through each index in each ticket
    for i in range(ticketLength):
      for ticket in filteredTickets:
        # If the current index doesn't work in our ticket for our rule...
        if(not field.isNumberInRange(ticket[i])):
          # Remove it from the list of possible indexes
          field.removePossibleIndex(i)
          break
  
  # Sort our fields - VERY IMPORTANT FOR OUR PERFORMANCE
  fields.sort()
  # Backtrack to find our solution
  return backtrackIndexes(fields)

# Part two finds the product of all departure fields in our ticket
def solvePart2(fields, ticketList, myTicket):
  # Find the indexes for the fields
  fieldIndexes = findFieldIndexes(fields, ticketList)

  # Find the product of each field that starts with "departure"
  product = 1
  for index in fieldIndexes:
    if("departure" in fieldIndexes[index]):
      product *= myTicket[index]

  return product

def main():
  fieldRules, myTicket, otherTickets = parseFile()

  print("--Part 1--")
  errorRate = checkTicketScanErrorRate(fieldRules, otherTickets)
  print(errorRate)

  print("--Part 2--")
  product = solvePart2(fieldRules, otherTickets, myTicket)
  print(product)

main()