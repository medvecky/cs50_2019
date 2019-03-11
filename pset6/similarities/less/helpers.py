from nltk.tokenize import sent_tokenize


# function split text by \n delimiter
def splitByLines(text):
    result = []
    for line in text.split('\n'):
        if line != "":
            result.append(line)
    return result


# function to split text by substrings with certain length
def splitBySubstrings(text, substringLength):
    result = []
    for position in range(len(text) - substringLength + 1):
        result.append(text[position:position + substringLength])
    return result


def lines(a, b):
    """Return lines in both a and b"""

    # generate lines list from a
    linesA = splitByLines(a)
    # generate lines list from b
    linesB = splitByLines(b)

    # convert lists to set and get sets intersection
    return list(set(linesA).intersection(set(linesB)))


def sentences(a, b):
    """Return sentences in both a and b"""

    # generate lists of senetences by nltk tokenize function
    linesA = sent_tokenize(a, language='english')
    linesB = sent_tokenize(b, language='english')

    # convert lists to set and get sets intersection
    return list(set(linesA).intersection(set(linesB)))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    linesA = splitBySubstrings(a, n)
    linesB = splitBySubstrings(b, n)
    return list(set(linesA).intersection(set(linesB)))
