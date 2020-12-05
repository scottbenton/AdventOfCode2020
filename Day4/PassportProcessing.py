import re

# List of valid eye colors, used for part 2
VALID_EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
# Path to file
FILE_NAME = "./input.txt"

# Helper passport class
class Passport:
  # Constructor, initializes all to None
  def __init__(self):
    self.birthYear = None
    self.issueYear = None
    self.expirationYear = None
    self.height = None
    self.hairColor = None
    self.eyeColor = None
    self.passportID = None
    self.countryID = None
  
  # Check validity - if anything other than countyID is not defined, its invalid
  def isValid(self):
    if self.birthYear and self.issueYear and self.expirationYear and self.height and self.hairColor and self.eyeColor and self.passportID:
      return True
    return False

  def setBirthYear(self, birthYear):
    intBY = int(birthYear)
    # P2 - Is our birth year in this range?
    if (1920 <= intBY <= 2002):
      self.birthYear = intBY
  
  def setIssueYear(self, issueYear):
    intIY = int(issueYear)
    # P2 - Is our issue year in this range?
    if (2010 <= intIY <= 2020):
      self.issueYear = intIY
  
  def setExpirationYear(self, expYear):
    intExpYear = int(expYear)
    # P2 - Is our expiration year in this range?
    if (2020 <= intExpYear <= 2030):
      self.expirationYear = intExpYear

  def setHeight(self, height):
    units = ""
    h = 0
    try:
      # Try to extract the units
      units = height[len(height) -2:]
      h = int(height[:len(height) - 2])
    except ValueError:
      # If the units aren't correct, continue on
      pass

    # Valid range for CM
    if (units == "cm" and 150 <= h <= 193):
      self.height = height
    # Valid range for IN
    elif (units == "in" and 59 <= h <= 76):
      self.height = height

  def setHairColor(self, hairColor):
    # Check and make sure the hex part is valid 
    hexValid = False
    try:
      int(hairColor[1:], 16)
      hexValid = True
    except ValueError:
      pass
    # Make sure we have a pound sign in position 1, and seven total characters
    if (hairColor[0] == "#" and hexValid and len(hairColor) == 7):
      self.hairColor = hairColor

  def setEyeColor(self, eyeColor):
    index = -1
    # If our index isn't in the array, it isn't valid
    try:
      index = VALID_EYE_COLORS.index(eyeColor)
    except ValueError:
      index = -1
    
    if (index >= 0):
      self.eyeColor = eyeColor
    
  def setPassportID(self, passportID):
    passportValid = False
    try:
      int(passportID)
      passportValid = True
    except ValueError:
      pass
    # The ID must be numeric, and it must be 9 total characters
    if (passportValid and len(passportID) == 9):
      self.passportID = passportID

  def setCountryID(self, countryID):
    # No validation needed
    self.countryID = countryID
  
  def readFromPair(self, key, value):
    # Map file keys to setter functions
    setters ={
      "byr": self.setBirthYear,
      "iyr": self.setIssueYear,
      "eyr": self.setExpirationYear,
      "hgt": self.setHeight,
      "hcl": self.setHairColor,
      "ecl": self.setEyeColor,
      "pid": self.setPassportID,
      "cid": self.setCountryID
    }
    # Call the proper setter
    return setters.get(key)(value)

  def __repr__(self):
    # For debugging purposes
    return "Birth Year: " + str(self.birthYear) + ", Issue Year: " + str(self.issueYear) + ", Expiration Year: " + str(self.expirationYear) + ", Height: " + str(self.height) + ", Hair Color: " + str(self.hairColor) + ", Eye Color: " + str(self.eyeColor) + ", Passport ID" + str(self.passportID) + ", Country ID: " + str(self.countryID)

def parseFile():
  # Create a list of passports
  passports = []

  with open(FILE_NAME, 'r') as file:
    # Read the data & split across newlines and spaces
    data = file.read()
    splitData = re.split(' |\n', data)

    # Since the data is split across mutliple strings, we need to keep a passport until we are finished reading
    currentPassport = Passport()
    for pair in splitData:
      # If there is another key/value pair in this passport
      if (len(pair) > 0):
        # Read it into our Passport object
        splitPair = pair.split(":")
        currentPassport.readFromPair(splitPair[0], splitPair[1])
      # Otherwise, add our currentPassport to the list, and move on to the next one
      else:
        passports.append(currentPassport)
        currentPassport = Passport()
  
  return passports

def main():
  # Get our list of passports
  passports = parseFile()

  # Check validity of all the passports
  count = 0
  for passport in passports:
    if (passport.isValid()):
      count += 1
      
  print(count)

main()