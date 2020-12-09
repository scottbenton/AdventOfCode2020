FILE_NAME="./Day8/input.txt"

# Instruction class to hold the operation and the argument
class Instruction: 
  def __init__(self, operation, argument):
    self.operation = operation
    self.argument = argument
  
  def getOperation(self):
    return self.operation
  def getArgument(self):
    return self.argument
  
  def __repr__(self):
    return self.operation + ": " + str(self.argument)

def parseFile():
  instructions = []

  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    lines = data.split('\n')

    # Parse each line into an instruction
    for line in lines:
      if(line):
        splitLines = line.split(" ")
        instructions.append(Instruction(splitLines[0], int(splitLines[1])))
  
  return instructions

def runInstructionSet(instructions):
  currentLine = 0 # The line we are currently checking
  globalCounter = 0 # The global counter that "acc" adds to
  
  visitedLines = set() # A set of all lines we have visited

  # If the current line is valid and we haven't visited it yet, run the loop
  while(instructions[currentLine] and not currentLine in visitedLines):
    # Add this line to our visited lines
    visitedLines.add(currentLine)

    # Destructure the operation and argument from the class
    op = instructions[currentLine].getOperation()
    arg = instructions[currentLine].getArgument()

    # Accumulator operations need to add one to the counter, and move to the next instruction
    if(op == "acc"):
      globalCounter += arg
      currentLine += 1
    # No Operation operations move to the next line
    elif(op == "nop"):
      currentLine += 1
    # Jump operations move exactly arg lines forwards or backwards
    elif(op == "jmp"):
      currentLine += arg
    # Just in case
    else:
      print("INVALID OPERATION:", op)
      currentLine += 1
  
  return globalCounter
    
# Add default values so we don't need a wrapper function
def findWorkingInstructionSet(instructions, currentLine=0, counter=0, visitedLines = set(), haveSwitched=False):
  # If we've been here, or we are out of range, this configuration is invalid
  if(currentLine in visitedLines or currentLine > len(instructions) or currentLine < 0):
    return -1
  # Hey we've reached the end! This is valid!
  elif(currentLine == len(instructions)):
    return counter
  # We aren't at the end of this line yet, lets work this out
  else:
    # Destructure the Instruction class
    op = instructions[currentLine].getOperation()
    arg = instructions[currentLine].getArgument()

    # Calculate the next values
    nextLine = currentLine + 1
    nextCounter = counter
    visitedLines.add(currentLine)

    if(op == "acc"):
      nextCounter += arg
    elif(op == "jmp"):
      nextLine += arg - 1

    # Our first shot at this - we may get a second depending
    firstTryOutput = findWorkingInstructionSet(instructions, nextLine, nextCounter, visitedLines, haveSwitched)

    # If the first try failed, we haven't switched anything yet, and the current operation is swappable
    if(firstTryOutput < 0 and not haveSwitched and (op == "jmp" or op == "nop")):
      # Swap the operations and try again
      if(op == "nop"):
        return findWorkingInstructionSet(instructions, currentLine + arg, counter, visitedLines, True)
      elif(op == "jmp"):
        return findWorkingInstructionSet(instructions, currentLine + 1, counter, visitedLines, True)
    else:
      # If our first try was valid, bubble it to the top
      return firstTryOutput

def main():
  instructions = parseFile()

  print("--Part 1--")
  accumulatedValue = runInstructionSet(instructions)
  print("Accumulator Value:", accumulatedValue)

  print("--Part 2--")
  fixedValue = findWorkingInstructionSet(instructions)
  print("Accumulator Value:", fixedValue)
main()
