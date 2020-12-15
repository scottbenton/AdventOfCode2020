def findNthSpokenWord(starter, n):
  lastSeenIndexes = dict();

  for i in range(0, len(starter) - 1):
    lastSeenIndexes[starter[i]] = i;

  print(lastSeenIndexes)

  lastNumber = starter[len(starter) - 1]
  for i in range(len(starter), n):
    lastSeenAt = lastSeenIndexes[lastNumber] if lastNumber in lastSeenIndexes else -1
    currentValue = i - 1 - lastSeenAt if lastSeenAt >= 0 else 0
    lastSeenIndexes[lastNumber] = i - 1
    lastNumber = currentValue

  return lastNumber

def main():
  input = [14, 3, 1, 0, 9, 5]

  print('--Part 1--')
  number2020 = findNthSpokenWord(input, 2020)
  print(number2020)

  print("--Part 2--")
  number30000000 = findNthSpokenWord(input, 30000000)
  print(number30000000)

main()