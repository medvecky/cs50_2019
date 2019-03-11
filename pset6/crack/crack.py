#!/usr/bin/env python3

import crypt
import sys

# password generator


def possiblePasswodsGenerator(hashString, salt):
    # possible characters for passwords
    letters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for first in letters[1:]:
        for second in letters:
            for third in letters:
                for fourth in letters:
                    for fifth in letters:
                        candidate = f"{first}{second}{third}{fourth}{fifth}".strip()
                        if candidate.isalpha():
                            if crypt.crypt(candidate, salt) == hashString:
                                print(candidate)
                                exit(0)


#  validate args
if len(sys.argv) != 2:
    print("Usage: ./crack hash")
    exit(1)

# get hash
hashString = sys.argv[1]

# get salt
salt = hashString[0:2]

# generate and check password

possiblePasswodsGenerator(hashString, salt)