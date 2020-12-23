FILE_NAME = "./Day22/input.txt"

# Player class, stores the ID and the deck
class Player:
  # Initialize values
  def __init__(self, id):
    self.id = id
    self.deck = []
  
  # Adds a card to the deck
  def addCard(self, card):
    self.deck.append(card)
  
  # After all cards have been added, sets a save point
  def finishInit(self):
    self.initialDeck = self.deck.copy()

  # Deals a card, removing it from the array
  def dealCard(self):
    card = self.deck[0]
    self.deck = self.deck[1:]
    return card
  
  # Resets back to the state saved in finishInit
  def reset(self):
    self.deck = self.initialDeck

  # Makes a copy of the Player, with only the next N entries in the array carrying over
  def copy(self, n):
    copyPlayer = Player(self.id)
    copyPlayer.deck = self.deck[:n]
    return copyPlayer

  # Returns the length of the deck
  def length(self):
    return len(self.deck)
  
  # Calculates the score
  def score(self):
    score = 0
    for idx in range(len(self.deck)):
      score += (idx + 1) * self.deck[len(self.deck) - 1 - idx]
    return score
  
  # To string
  def __str__(self):
    return str(self.id) +": " + str(self.deck)

# Reads in the file, returns all our information
def parseFile():
  player1 = Player(1)
  player2 = Player(2)
  
  with open(FILE_NAME, 'r') as file:
    
    # Read the data & split across newlines
    data = file.read()
    lines = data.split("\n")
    
    # Reads cards into player 1 or player 2
    player1sTurn = True
    for line in lines:
      if(not line):
        player1sTurn = False
      elif('Player' not in line):
        if(player1sTurn):
          player1.addCard(int(line))
        else:
          player2.addCard(int(line))
              
  # Finish initialization to set our "save point" to reset back to
  player1.finishInit()
  player2.finishInit()

  return player1, player2

# Part 1
def crabCombat(player1, player2):
  # So long as cards exist in both hands, the game continues
  while player1.length() > 0 and player2.length() > 0:
    # Deal each card
    card1 = player1.dealCard()
    card2 = player2.dealCard()
    # To the winner go the spoils
    if(card1 > card2):
      player1.addCard(card1)
      player1.addCard(card2)
    else:
      player2.addCard(card2)
      player2.addCard(card1)
  
  # Return the winner
  return player1 if player1.length() != 0 else player2

def recursiveCombat(player1, player2):
  # We need to store a history of winners
  deck1History = []
  deck2History = []
  # Game continues while both players have cards
  while(player1.length() > 0 and player2.length() > 0):
    # If the current decks have both been seen before, we have a repeat
    if(player1.deck in deck1History and player2.deck in deck2History):
      # Which means that player 1 wins this round
      return player1
    
    # Add the current decks to the history
    deck1History.append(player1.deck.copy())
    deck2History.append(player2.deck.copy())

    # Deal the cards
    card1 = player1.dealCard()
    card2 = player2.dealCard()

    # If the number present is less than the deck length for each card...
    if(card1 <= player1.length() and card2 <= player2.length()):
      # Call this function recursively, letting each player keep the next (card) values from their deck
      winningPlayer = recursiveCombat(player1.copy(card1), player2.copy(card2))
      # Distribute cards based on winners
      if winningPlayer.id == player1.id:
        player1.addCard(card1)
        player1.addCard(card2)
      else:
        player2.addCard(card2)
        player2.addCard(card1)
    # Distribute to the higher card
    else: 
      if(card1 > card2):
        player1.addCard(card1)
        player1.addCard(card2)
      else:
        player2.addCard(card2)
        player2.addCard(card1)
  
  # Return the winning player
  return player1 if player1.length() != 0 else player2
  

def main():
  player1, player2 = parseFile()

  print("--Part 1--")
  part1Winner = crabCombat(player1, player2)
  print(part1Winner.score())

  player1.reset()
  player2.reset()
  
  print("--Part 2--")
  part2Winner = recursiveCombat(player1, player2)
  print(part2Winner.score())
main()