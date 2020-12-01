FILENAME = "./expense-report.txt";
WINNING_NUMBER = 2020

def readFile(filepath):
  with open(filepath, 'r') as file:
    data = file.read()
    splitData = data.split("\n")

    numberList = []

    for data in splitData:
      if(len(data) > 0):
        numberList.append(int(data))
    
    return numberList

def findTwoEntryWinner(numberList):
  for i in range(0, len(numberList) - 1):
    numI = numberList[i]
    for j in range(i + 1, len(numberList)):
      numJ = numberList[j]
      if (numI + numJ == WINNING_NUMBER):
        print(numI * numJ)

def findThreeEntryWinner(numberList):
  for i in range(0, len(numberList) - 2):
    numI = numberList[i]
    for j in range(i + 1, len(numberList)-1):
      numJ = numberList[j]
      for k in range(j + 1, len(numberList)):
        numK = numberList[k]
        if (numI + numJ + numK == WINNING_NUMBER):
          print(numI * numJ * numK)

def main():
  numbers = readFile(FILENAME)
  
  print("--TWO ENTRY WINNER--")
  findTwoEntryWinner(numbers)
  print("--THREE ENTRY WINNER--")
  findThreeEntryWinner(numbers)



main()