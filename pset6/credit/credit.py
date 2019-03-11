#!/usr/bin/env python3
from cs50 import get_int

# transfer card number to array of number


def putCardNumberToArray(cardNumber):
    return [int(d) for d in str(cardNumber)]


# control sum verification procedure
def checkControlSum(cardNumberAsArray):
    controlSum = 0
    # first part of control sum
    for i in range(len(cardNumberAsArray)):
        tmp = cardNumberAsArray[i]
        if i % 2 == 0:
            controlSum += tmp
        else:
            tmp *= 2
            if tmp > 9:
                controlSum += tmp % 10
                controlSum += tmp // 10
            else:
                controlSum += tmp
    # last number check
    if controlSum % 10 == 0:
        return True
    return False

# check company identifiers and valid number of digits


def checkCompanyIdentifierAndFormat(cardNumberAsArray):
    # 34 37 for AMEX
    numberLenght = len(cardNumberAsArray)
    if (cardNumberAsArray[numberLenght - 1] == 3 and
        (cardNumberAsArray[numberLenght - 2] == 4 or
         cardNumberAsArray[numberLenght - 2] == 7)):
        if numberLenght == 15:
            print("AMEX")
        else:
            print("INVALID")
    # check for master card 51 52 53 54
    elif (((cardNumberAsArray[numberLenght - 1] == 5) and
            (cardNumberAsArray[numberLenght - 2] == 1 or
             cardNumberAsArray[numberLenght - 2] == 2 or
             cardNumberAsArray[numberLenght - 2] == 3 or
             cardNumberAsArray[numberLenght - 2] == 4 or
             cardNumberAsArray[numberLenght - 2] == 5))):
        if numberLenght == 16:
            print("MASTERCARD")
        else:
            print("INVALID")
    # check for visa
    elif cardNumberAsArray[numberLenght - 1] == 4:
        if numberLenght == 16 or numberLenght == 13:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")

# card verification main procedure


def checkCard(cardNumberAsArray):
    if checkControlSum(cardNumberAsArray) == True:
        checkCompanyIdentifierAndFormat(cardNumberAsArray)
    else:
        print("INVALID")

# get card number with rude validation


def getValidCardNumber():
    cardNumber = get_int("Number: ")
    while cardNumber <= 0:
        cardNumber = get_int("Number: ")
    return cardNumber


# array representation of card number
cardNumber = getValidCardNumber()
cardNumberAsArray = putCardNumberToArray(cardNumber)
cardNumberAsArray.reverse()
checkCard(cardNumberAsArray)