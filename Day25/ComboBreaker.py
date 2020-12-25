FILE_NAME = "./Day25/input.txt"
SUBJECT_NUMBER = 7

# Read in our two keys
def parseFile():
  cardPublicKey = 0
  doorPublicKey = 0
  with open(FILE_NAME, 'r') as file:
    data = file.read()
    keys = data.split("\n")
    cardPublicKey = int(keys[0])
    doorPublicKey = int(keys[1])
  
  return cardPublicKey, doorPublicKey

# Transform our value - used for finding the iteration and the encryption key
def transformValue(value, subjectNumber):
  return (value * subjectNumber) % 20201227

# Takes a public key and the subject number and returns the loop count
def findLoopIteration(publicKey, subjectNumber = SUBJECT_NUMBER):
  value = 1
  loopCount = 0
  while(value != publicKey):
    value = transformValue(value, subjectNumber)
    loopCount+=1
  return loopCount

# Follows the same process to find the encryption key
def findEncryptionKey(subjectNumber, loopCount):
  value = 1
  for i in range(loopCount):
    value = transformValue(value, subjectNumber)
  return value

def main():
  cardPublicKey, doorPublicKey = parseFile()

  cardLoopCount = findLoopIteration(cardPublicKey)
  
  print("--Part 1--")
  encryptionKey = findEncryptionKey(doorPublicKey, cardLoopCount)
  print("Encryption Key:", encryptionKey)

  print("--Part 2--")
  print("Happy Holidays! :)")
main()
