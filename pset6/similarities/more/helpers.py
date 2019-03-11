from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    matrix = []
    # initial matrix value inialization
    for i in range(len(a) + 1):
        tmp = []
        for j in range(len(b) + 1):
            if i == 0 and j == 0:
                tmp.append((0, None))
            elif i == 0:
                tmp.append((j, Operation.INSERTED))
            elif j == 0:
                tmp.append((i, Operation.DELETED))
            else:
                tmp.append((-1, None))
        matrix.append(tmp)

    # every path cost calculation
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            tmp = []
            minValue = -1
            op = 999
            # case when symbols in string are equals
            if a[i - 1:i] == b[j - 1:j]:
                matrix[i][j] = (matrix[i - 1][j - 1][0], Operation.SUBSTITUTED)
            # get minimum cost of nerby previous operations
            else:
                tmp.append(matrix[i][j - 1][0])
                tmp.append(matrix[i - 1][j - 1][0])
                tmp.append(matrix[i - 1][j][0])
                minValue = min(tmp)
                if minValue == tmp[0]:
                    op = Operation.INSERTED
                elif minValue == tmp[1]:
                    op = Operation.SUBSTITUTED
                else:
                    op = Operation.DELETED
                matrix[i][j] = (minValue + 1, op)
    return matrix
