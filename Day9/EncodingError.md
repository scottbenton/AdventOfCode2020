# Day 8: Encoding Error

## Problem Description

From [Advent of Code](https://adventofcode.com/)

### Part 1

With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:

- 26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
- 49 would be a valid next number, as it is the sum of 24 and 25.
- 100 would not be valid; no two of the previous 25 numbers sum to 100.
- 50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.

Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:

- 26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
- 65 would not be valid, as no two of the available numbers sum to it.
- 64 and 66 would both be valid, as they are the result of 19+45 and 21+45 resp\*ectively.

Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):

```
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
```

In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

### Part 2

The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

Again consider the above example. In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?

## Solution

After reading the input file to an integer list, the first task was to find the encoding error within the lines. I did this by running nested loops through the past 25 items, and optimized it a little by not bothering to add items that were already greater than the number I was checking against. Once I found the number that didn't add up, I returned it.

Part two was a little more interesting. I didn't want to completely brute force this, so I found a way to continually move the start and end of an array through the list of items looking for the set that would add up to our target number. Here is an example of how this algorithm works.

Say our target number is `8`, and our list of set items is

```
[3, 4, 6, 10, 5, 1, 3, 4]
```

I start out our `total` variable as the sum of the first two items, `7`.
Our count variable is set to `2`, since we currently hold two items in our total.

```
Total = 7
Count = 2
```

Since `7 < 8`, we will add the next line to our total, and add one to our count.

```
Total = 13
Count = 3
```

Now, since `13 > 8`, we need to remove the first item we added from our total, and remove 1 from our count.

```
Total = 10
Count = 2
```

Since `10 > 8`, we remove the first item from our total, but since our count must be at least 2, we shift over to the next item in the list, 10.

```
Total = 16
Count = 2
```

Still `16 > 8`, so we repeat the last step

```
Total = 15
Count = 2
```

Still `15 > 8`, so we repeat again

```
Total = 7
Count = 2
```

Since `7 < 8`, we need to increase our count by one.

```
Total = 8
Count = 3
```

Our total matches, and our numbers are `[5, 1, 3]`. We can then add the min and max of the array to get our encryption weakness, `6`.

## What I learned

The second half of the problem gave me an interesting chance to create an algorithm that walks through an array, and grabs a continuous subset of variable length that meets a certain parameter. While I'm sure that there are ways to increase the efficiency of my solution, I think that it does a nice job of accounting for differences in array length, while minimizing the computations necessary to check each unique array.
