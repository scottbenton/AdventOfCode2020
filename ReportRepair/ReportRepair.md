# Day 1: Report Repair

## Problem Description

From [Advent of Code](https://adventofcode.com/2020/day/1)

### Part 1

After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721, 979, 366, 299, 675, 1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 \* 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?

### Part 2

The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?

## Solution

The solution to this problem is fairly trivial since our list of numbers is small, only 200 lines or so.
For setup, I have a function that takes in a filename, opens it, and parses through the data.
I created two separate solutions for this problem, one that is specific to the number of entries passed, and one that is more generalized.

### Problem Specific

To implement this solution in cases where you would only ever need to find 2 or 3 entries that sum to 2020, I used nested for loops. `findTwoEntryWinner` and `findThreeEntryWinner` in the solution file. These solutions work by using nested for loops to check the sum of combinations of numbers against the winning number, in this case, 2020. Once it finds a winning number it prints the product of the winning combination.

These two work well for this solution, but I did want to find a solution that would work for any number of entries needed. So I came up with a recursive solution

### Recursive Solution

The recursive solution relies on a list to keep track of our different counters.
Each counter will start at 1 entry further along than our previous entry, and will end 1 counter before the next entry ends. For example, checking 4 entries with a list of length 24, our first combination checked will be `[0, 1, 2, 3]`, and our last combination checked will be `[20, 21, 22, 23]`. By running things in this way, we ensure that no two counters will ever be on the same number.

Our base case for this solution is when we run out of indexes to increment. Whenever that happens, we check to see if the sum of the entries from the current counters matches the winning number, and if it does, we print out the product of those same entries.

Our recursive function `recursiveNEntryWinner` has a nice starter function called `findNEntryWinner` that initializes the counterList and calls `recursiveNEntryWinner` with starting values

Running the program gives this output

```
--TWO ENTRY WINNER--
926464
--THREE ENTRY WINNER--
65656536
--RECURSIVE TWO ENTRY WINNER--
926464
--RECURSIVE THREE ENTRY WINNER--
65656536
```
