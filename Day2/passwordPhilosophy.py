# File containing our password list
FILENAME = "./input.txt"

def readFile(filepath):
  with open(filepath, 'r') as file:
    return file.readlines()
  return None

def checkPasswordFile(fileLines, passwordCheckerFn):
  validPasswordCount = 0

  for line in fileLines:
    section = line.strip().split(" ")
    
    numbers = section[0].split("-")
    num1 = int(numbers[0])
    num2 = int(numbers[1])

    letter = section[1].replace(":", "")
    if (passwordCheckerFn(section[2], letter, num1, num2)):
      validPasswordCount += 1
  
  return validPasswordCount

def isValidPasswordPolicy1(password, letter, minNum, maxNum):
  count = password.count(letter)
  if (minNum <= count and count <= maxNum):
    return True
  else:
    return False

def isValidPasswordPolicy2(password, letter, pos1, pos2):
  passLen = len(password)
  pos1HasLetter = pos1-1 < passLen and password[pos1-1] == letter
  pos2HasLetter = pos2-1 < passLen and password[pos2-1] == letter

  if ((pos1HasLetter or pos2HasLetter) and not (pos1HasLetter and pos2HasLetter)):
    return True
  else:
    return False

def main():
  fileLines = readFile(FILENAME)
  print("Total valid passwords policy 1:", checkPasswordFile(fileLines, isValidPasswordPolicy1))
  print("Total valid passwords policy 2:", checkPasswordFile(fileLines, isValidPasswordPolicy2))

main()