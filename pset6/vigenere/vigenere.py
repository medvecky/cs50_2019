#!/usr/bin/env python3

import sys
from cs50 import get_string

# validation of command line args


def comandLineArgsValidation():
    # check for number of arguments
    if len(sys.argv) != 2:
        print("Usage ./vigenere k")
        return False

    # check for arg contains only aplphabet symbols
    if sys.argv[1].isalpha() == False:
        return False
    return True

# text encryption


def encryptText(plainText, key):

    # convert params strins to lists
    plainTextAsList = list(plainText)
    keyAsList = list(key)
    keyIndex = 0
    k = 0
    # text encryption
    for i in range(len(plainTextAsList)):
        # calculating of actual key value
        if keyAsList[keyIndex].isupper() == True:
            k = ord(keyAsList[keyIndex]) - ord('A')
        else:
            k = ord(keyAsList[keyIndex]) - ord('a')
        # for upper case
        if plainTextAsList[i].isalpha():
            if plainTextAsList[i].isupper():
                plainTextAsList[i] = chr((((ord(plainTextAsList[i]) - ord('A')) + k) % 26) + ord('A'))
            # for lower case
            elif plainTextAsList[i].islower():
                plainTextAsList[i] = chr((((ord(plainTextAsList[i]) - ord('a')) + k) % 26) + ord('a'))
            keyIndex += 1
            if keyIndex == len(keyAsList):
                keyIndex = 0
    plainText = ""
    plainText = ''.join(plainTextAsList)

    return plainText


# check command line args
if comandLineArgsValidation() == False:
    exit(1)

# get plain text
plainText = get_string("plaintext: ")

# call encryption function
plainText = encryptText(plainText, sys.argv[1])

print("ciphertext: {}".format(plainText))