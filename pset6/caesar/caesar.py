#!/usr/bin/env python3

import sys
from cs50 import get_string

# check command line args

if len(sys.argv) != 2:
    print("Usage: ./caesar k")
    exit(1)

# get numeric key value
k = int(sys.argv[1])

# get plain text
plainText = get_string("plain text: ")
plainTextAsList = list(plainText)

# text encryption
for i in range(len(plainTextAsList)):
    # for upper case
    if plainTextAsList[i].isalpha() and plainTextAsList[i].isupper():
        plainTextAsList[i] = chr((((ord(plainTextAsList[i]) - 65) + k) % 26) + 65)
    # for lower case
    elif plainTextAsList[i].isalpha() and plainTextAsList[i].islower():
        plainTextAsList[i] = chr((((ord(plainTextAsList[i]) - 97) + k) % 26) + 97)
plainText = ""
plainText = ''.join(plainTextAsList)
print("ciphertext: {}".format(plainText))