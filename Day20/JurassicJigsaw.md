# Day 20: Jurassic Jigsaw

## Problem Description

From [Advent of Code](https://adventofcode.com/)

### Part 1

The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the distance! Since you have some spare time, you might as well see if there was anything interesting in the image the Mythical Information Bureau satellite captured.

After decoding the satellite messages, you discover that the data actually contains many small images created by the satellite's camera array. The camera array consists of many cameras; rather than produce a single square image, they produce many smaller square image tiles that need to be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile with a random unique ID number. The tiles (your puzzle input) arrived in a random order.

Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to a random orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.

To show how the tiles should be reassembled, each tile's image data includes a border that should line up exactly with its adjacent tiles. All tiles have this border, and the border lines up exactly when the tiles are both oriented correctly. Tiles at the edge of the image also have this border, but the outermost edges won't line up with any other tiles.

Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?

### Part 2

Now, you're ready to check the image for sea monsters.

The borders of each tile are not part of the actual image; start by removing them.

Now, you're ready to search for sea monsters! Because your image is monochrome, a sea monster will look like this:

```
                  #
#    ##    ##    ###
 #  #  #  #  #  #
```

When looking for this pattern in the image, the spaces can be anything; only the # need to match. Also, you might need to rotate or flip your image before it's oriented correctly to find sea monsters. In the above image, after flipping and rotating it to the appropriate orientation, there are two sea monsters (marked with O):

Determine how rough the waters are in the sea monsters' habitat by counting the number of # that are not part of a sea monster. In the above example, the habitat's water roughness is 273.

How many # are not part of a sea monster?

## Solution

Today's example relied a lot on manipulations and searches of 2D arrays. In order to help with that, I created a Tile class that handled manipulations such as flipping, rotating, and getting the borders of the tile.

From there I used a backtracking algorithm to place each tile on the board wherever it fits. Once I had my image constructed, I removed the borders, and searched through each variation of flipped and rotated images to find all sea monster instances. I replaced each character in the sea monster with another as I went so I could count untouched characters later.

After all the sea monsters had been placed, I counted the remaining `#` to get the solution to part 2.

## What I learned

I learned a lot about array manipulation in python using features such as using [::-1] to invert arrays.
