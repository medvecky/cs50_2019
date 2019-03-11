#!/usr/bin/env python3
from cs50 import get_int

# function to get valid Height value for mario game


def get_valid_integer():
    height = get_int("Height: ")
    while height < 0 or height > 23:
        height = get_int("Height: ")
    return height

# function for printing blocks


def printBlocks(numberOfBlocks):
    for i in range(numberOfBlocks):
        print("#", end="")


#  get valid height value
height = get_valid_integer()

# two inner loops for pyramid drawing
for row in range(height):
    # counter for blocks in left side
    numberOfBlocks = 0
    for column in range(height):
        # condition to form right pyramid
        if column < height - 1 - row:
            print(" ", end="")
        else:
            print("#", end="")
            numberOfBlocks += 1
    # hole in pyramid center
    print("  ", end="")
    # create right side of pyramid
    printBlocks(numberOfBlocks)
    print()