# Day 23: Crab Cups

## Problem Description

From [Advent of Code](https://adventofcode.com/)

### Part 1

The small crab challenges you to a game! The crab is going to mix up some cups, and you have to predict where they'll end up.

The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were 32415, there would be five cups in the circle; going clockwise around the circle from the first cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.

Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.

Each move, the crab does the following actions:

- The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
- The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
- The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
- The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters; each number except 1 should appear exactly once.

Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?

### Part 2

Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab), you are quite surprised when the crab starts arranging many cups in a circle on your raft - one million (1000000) in total.

Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing fashion starting from the number after the highest number in your list and proceeding one by one until one million is reached. (For example, if your labeling were 54321, the cups would be numbered 5, 4, 3, 2, 1, and then start counting up from 6 until one million is reached.) In this way, every number from one through one million is used exactly once.

After discovering where you made the mistake in translating Crab Numbers, you realize the small crab isn't going to do merely 100 moves; the crab is going to do ten million (10000000) moves!

The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise of cup 1. You can have them if you predict what the labels on those cups will be when the crab is finished.

In the above example (389125467), this would be 934001 and then 159792; multiplying these together produces 149245887792.

Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels together?

## Solution

The solution to today's problem was less about solving the problem, and more about optimizing it. My solution to part 1 made use of python's lists, which worked when we had 8 cups, and were doing 100 iterations, but once that crab pulled out 1 million cups and started doing 10 million iterations, a more performant solution was required.

The way that I decided to optimize this relied on two different data structures, maps and linked lists. We can use a linked list of cups to store the circle of cups. The first cup in the circle will hold a reference to the second, and so on and so forth until the last cup is reached, which holds a reference back to the first cup. We can then add and remove cups to this data structure simply by updating the references at the connecting edges of the change. This is what the functions `addCups` and `removeNCups` do. We run into a problem with this solution though when we need to find the next index down from our current index. We could search through our linked list to find it, but that has a time complexity of `O(n)`. We can access this in `O(1)` if we keep a map that links a cup label to the cup object. This way, if we are looking for the cup labeled 5, we can call `cupMap[5]` rather than searching through our linked list to find 5.

From there, it was easy enough to run iterations over our input and calculate the answers part 1 and part 2 required.

## What I learned

I think this is the first time I've needed to use a linked list in class, so it was interesting to find a problem where it made sense to use it!
