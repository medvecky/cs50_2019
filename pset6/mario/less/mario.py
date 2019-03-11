#!/usr/bin/env python3
from cs50 import get_int

# function to get valid Height value for mario game


def get_valid_integer():
    height = get_int("Height: ")
    while height < 0 or height > 23:
        height = get_int("Height: ")
    return height


#  get valid height value
height = get_valid_integer()

# two inner loops for pyramid drawing
for row in range(height):
    for column in range(height + 1):
        # condition to form right pyramid
        if column < height - 1 - row:
            print(" ", end="")
        else:
            print("#", end="")
    print()