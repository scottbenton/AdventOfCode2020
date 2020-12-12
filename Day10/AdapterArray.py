FILE_NAME="./Day10/input.txt"

def parseFile():
  # Start with only the outlet, 0
  adapters = [0]

  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines
    data = file.read()
    lines = data.split('\n')

    # Parse each line into our adapter array
    for line in lines:
      if(line): 
        adapters.append(int(line))

  # Sort our adapters before returning them
  adapters.sort()
  return adapters;

def findDifferencesInArray(arr):
  # Dictionary that will store the count of each possible difference
  differences = {}

  # Go through the list, add one for each difference to our dictionary
  count = 1
  while(count < len(arr)):
    difference = arr[count] - arr[count-1]

    if(difference in differences):
      differences[difference]+=1
    else:
      differences[difference] = 1
  
    count += 1
  
  return differences

# Wrapper for find differences that multiplies 1 & 3 counts together for part 1
def solvePart1(arr):
  differences = findDifferencesInArray(arr)
  return differences[1] * differences[3]

# Recursive function, takes an array, and finds all combinations where the items differ by < 3
def findAllCombinations(arr, currIndex=0):
  # Base case - if we are at the end of the array, return 1
  if(currIndex >= len(arr) - 1):
    return 1

  # Keep a count of all possible combos
  count = 0
  # Combo for not skipping next value
  count += findAllCombinations(arr, currIndex + 1)
  # If we can skip the next value, find all combinations where we do that
  if(currIndex < len(arr) - 2 and arr[currIndex + 2] - arr[currIndex] <= 3):
    count += findAllCombinations(arr, currIndex + 2)
  # If we can skip two values, find all of those combinations
  if(currIndex < len(arr) - 3 and arr[currIndex + 3] - arr[currIndex] <= 3):
    count += findAllCombinations(arr, currIndex + 3)
  return count


# This function breaks up our large array into smaller arrays.
# If we figure out the combinations in each smaller array, we can combine to find the overall combinations
def solvePart2(arr):
  startIdx = 0 # Where we are starting our sublist from
  length = 1 # The length of our sublist
  currentIdx = 1 # The current index within our list

  combinationCounts = [] # The counts for our combinations

  # Loop while our smaller array has space left
  while(startIdx + 2 <= len(arr)): 
    # Loop while we aren't at the end of the array, and while there isn't a gap of 3
    while(currentIdx < len(arr) - 1 and arr[currentIdx] - arr[currentIdx - 1] < 3): 
      length += 1 # increment the length of the smaller array
      currentIdx += 1 # Move to check the next index

    # When we reach here, we've found a smaller array that is separated on either end by a gap of 3
    # This means it is separated from the rest of the array - anything we do here doesn't affect the combinations of the rest of the array
    combinationCounts.append(findAllCombinations(arr[startIdx:startIdx + length])) # Find all combos for this smaller array
    length = 1 # Reset our small array to initial values
    startIdx = currentIdx
    currentIdx += 1

  # Find the product of all the values in our combinationCounts to get the overall combination number
  reducedValue = 1
  for combinationCount in combinationCounts:
    reducedValue *= combinationCount

  return reducedValue  

  
def main():
  adapters = parseFile()
  
  # Add the phone to the list of adapters
  adapters.append(adapters[len(adapters) - 1] + 3)
  
  print("--Part 1--")
  part1Sol = solvePart1(adapters)
  print(part1Sol)

  print("--Part 2--")
  part2Sol = solvePart2(adapters)
  print(part2Sol)

main()