# Day 24: Lobby Layout

## Problem Description

From [Advent of Code](https://adventofcode.com/)

### Part 1

Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator. You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the check-in desk until they've finished installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not in the mood to wait, you offer to help figure out the pattern.

The tiles are all white on one side and black on the other. They start with the white side facing up. The lobby is large enough to fit whatever pattern might need to appear there.

A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input). Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference tile in the very center of the room. (Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is identified by a series of these directions with no delimiters; for example, `esenee` identifies the tile you land on if you start at the reference tile and then move one tile east, one tile southeast, one tile northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once. For example, a line like `esew` flips a tile immediately adjacent to the reference tile, and a line like `nwwswee` flips the reference tile itself.

In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white). After all of these instructions have been followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed, how many tiles are left with the black side up?

### Part 2

The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the following rules:

- Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
- Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

Here, tiles immediately adjacent means the six tiles directly touching the tile in question.

The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be flipped, then they are all flipped at the same time.

How many tiles will be black after 100 days?

## Solution

My solution to today's problem relied heavily on [this](https://www.redblobgames.com/grids/hexagons/) ingenious article about representing hexagonal grids using 3D arrays.
The basic premise here is that since a point in 3d space has 6 different movement directions (+/- x, +/- y, +- z), we can apply this to the hexagon, which also has 6 different directions.
The big difference is that with hexagonal space, instead of moving 1 in the x direction, you will always move +1 in one direction and -1 in another.
This is to account for the fact that we could make a loop without ever backtracking on a direction (for example, moving north-west -> south-west -> east puts us back at the starting point)

Once I knew how to handle a hexagonal grid as a 3D array, I created a dictionary of tiles so that I could keep track of which were white and which were black.
The dictionary indexed a tuple of the (x, y, z) values of the hexagon, and returned the tile color.
This way, I could keep track of which ones had flipped.
Part 1 was easy enough, as I just had to read the input and count the number of black tiles.

Part 2 required a little bit more thought.
The method I came up with examines each point in the dictionary, and determines if it needs to change its state.
From there, I checked all of the point's neighbors, and if any of them needed to be flipped to black, I would add them to the next state dictionary.
Its not an incredibly well optimized algorithm, but it runs in reasonable time and gives me the correct answer once I count all the black tiles.

## What I learned

I learned how to represent a hexagonal grid with a three dimensional array!
