# Day 22: Crab Combat

## Problem Description

From [Advent of Code](https://adventofcode.com/)

### Part 1

It only takes a few hours of sailing the ocean on a raft for boredom to sink in. Fortunately, you brought a small deck of space cards! You'd like to play a game of Combat, and there's even an opponent available: a small crab that climbed aboard your raft before you left.

Fortunately, it doesn't take long to teach the crab the rules.

Before the game starts, split the cards so each player has their own deck (your puzzle input). Then, the game consists of a series of rounds: both players draw their top card, and the player with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. If this causes a player to have all of the cards, they win, and the game ends.

Once the game ends, you can calculate the winning player's score. The bottom card in their deck is worth the value of the card multiplied by 1, the second-from-the-bottom card is worth the value of the card multiplied by 2, and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.

Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score?

### Part 2

You lost to the small crab! Fortunately, crabs aren't very good at recursion. To defend your honor as a Raft Captain, you challenge the small crab to a game of Recursive Combat.

Recursive Combat still starts by splitting the cards into two decks (you offer to play with the same starting decks as before - it's only fair). Then, the game consists of a series of rounds with a few changes:

- Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
- Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
- If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
- Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.

As in regular Combat, the winner of the round (even if they won the round by winning a sub-game) takes the two cards dealt at the beginning of the round and places them on the bottom of their own deck (again so that the winner's card is above the other card). Note that the winner's card might be the lower-valued of the two cards if they won the round due to winning a sub-game. If collecting cards by winning the round causes a player to have all of the cards, they win, and the game ends.

Here is an example of a small game that would loop forever without the infinite game prevention rule:

```
Player 1:
43
19

Player 2:
2
29
14
```

During a round of Recursive Combat, if both players have at least as many cards in their own decks as the number on the card they just dealt, the winner of the round is determined by recursing into a sub-game of Recursive Combat. (For example, if player 1 draws the 3 card, and player 2 draws the 7 card, this would occur if player 1 has at least 3 cards left and player 2 has at least 7 cards left, not counting the 3 and 7 cards that were drawn.)

To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next cards in their deck (the quantity of cards copied is equal to the number on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it is on hold and completely unaffected; no cards are removed from players' decks to form the sub-game. (For example, if player 1 drew the 3 card, their deck in the sub-game would be copies of the next three cards in their deck.)

After the game, the winning player's score is calculated from the cards they have in their original deck using the same rules as regular Combat.

Defend your honor as Raft Captain by playing the small crab in a game of Recursive Combat using the same two decks as before. What is the winning player's score?

## Solution

Today's problem wasn't too difficult to set up the logic for. Going through Problem 1, I wanted to make sure that the infrastructure I set up in the `Player` class was generic enough to be useful for part 2, so adding the functions to save the initial state, get the score, and draw/add cards made it easy to reuse for both parts.

Part one was super easy, as all I needed to do was draw both cards and give both cards to the dealer of the higher one. A trivial implementation with the `Player` class

Part two's main differences come from the historical data that needs to be parsed and from the recursive nature of the problem. I expected the comparing of arrays for historical checks to be more complex, as in most languages I would have needed to hash out some kind of value for quicker comparisons, but my solution for part 2 still executes timely despite the easy implementation. With the base case handled, I just needed to compare the output of recursive calls to determine who to assign the cards to, which also wasn't difficult.

## What I learned

Python seems to be very well optimized under the hood, especially for the ease of use it offers. Comparison of arrays in other languages, especially ones done without looping through each value in the array tends to either take a while or require more legwork, so for array comparisons to just work and work fast was a pleasant surprise!
