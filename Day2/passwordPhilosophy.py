# File containing our password list
FILENAME = "./input.txt"

def readFile(filepath):
  with open(filepath, 'r') as file:
    return file.readlines();
  return None;

def parseFile(fileLines):
  validPasswordsPolicy1 = 0
  validPasswordsPolicy2 = 0

  for line in fileLines:
    section = line.strip().split(" ")
    
    numbers = section[0].split("-")
    num1 = int(numbers[0])
    num2 = int(numbers[1])

    letter = section[1].replace(":", "")
    if (isValidPasswordPolicy1(section[2], letter, num1, num2)):
      validPasswordsPolicy1 += 1
    if (isValidPasswordPolicy2(section[2], letter, num1 - 1, num2 - 1)):
      validPasswordsPolicy2+= 1
  
  return [validPasswordsPolicy1, validPasswordsPolicy2]

def isValidPasswordPolicy1(password, letter, minNum, maxNum):
  count = password.count(letter)
  if (minNum <= count and count <= maxNum):
    return True
  else:
    return False

def isValidPasswordPolicy2(password, letter, pos1, pos2):
  passLen = len(password)
  pos1HasLetter = pos1 < passLen and password[pos1] == letter
  pos2HasLetter = pos2 < passLen and password[pos2] == letter

  if ((pos1HasLetter or pos2HasLetter) and not (pos1HasLetter and pos2HasLetter)):
    return True
  else:
    return False

def main():
  fileLines = readFile(FILENAME)
  validPasswords = parseFile(fileLines)
  print("Total valid passwords policy 1:", validPasswords[0])
  print("Total valid passwords policy 2:", validPasswords[1])

main()