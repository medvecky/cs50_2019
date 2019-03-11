#!/usr/bin/env python3
from cs50 import get_float

# function to get change owed


def getValidChangeOwed():
    changeOwed = get_float("Change owed: ")
    while changeOwed < 0:
        changeOwed = get_float("Change owed: ")
    return changeOwed


# total coins counter for result
coinsCounter = 0
changeOwed = getValidChangeOwed()
intValueOfCoins = int(changeOwed * 100)

# temporary result number of 25
tmp = intValueOfCoins // 25
coinsCounter += tmp

# left to issue after issuing 25
intValueOfCoins %= 25

# temporary result number of 10
tmp = intValueOfCoins // 10
coinsCounter += tmp

# left to issue after issuing 10
intValueOfCoins %= 10

# temporary result number of 5
tmp = intValueOfCoins // 5
coinsCounter += tmp

# left to issue after issuing 5
intValueOfCoins %= 5

coinsCounter += intValueOfCoins
print(coinsCounter)