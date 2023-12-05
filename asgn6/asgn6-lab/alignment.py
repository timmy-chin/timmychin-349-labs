import sys


def parse(fileName):
    fp = open(fileName, "r")
    x = fp.readline().replace("\n", "")
    y = fp.readline().replace("\n", "")
    score_matrix = createMatrix(fp, getKeys(fp))
    return x, y, score_matrix


def getKeys(fp):
    keyStr = fp.readline().replace("\n", "")
    keys = keyStr.split()
    keys.pop(0)  # get rid of "."
    return keys


def createMatrix(fp, keys):
    matrix = {}
    for line in fp:
        values = line.replace("\n", "").split()
        key_char = values.pop(0)
        valueMap = createMap(keys, values)
        matrix[key_char] = valueMap
    return matrix


def createMap(keys, values):
    valueMap = {}
    for key, value in zip(keys, values):
        valueMap[key] = int(value)
    return valueMap


def alignment(x, y, score):
    dp_table = [[0] * (len(y) + 1) for k in range(len(x) + 1)]  # plus 1 for base case
    backTracker = [[""] * (len(y) + 1) for k in range(len(x) + 1)]
    initBaseCase(x, y, score, dp_table)

    # fill out dp_table
    for i in range(1, len(x) + 1):  # plus 1 for base case
        for j in range(1, len(y) + 1):
            align = dp_table[i - 1][j - 1] + score[x[i - 1]][y[j - 1]]
            remove = dp_table[i - 1][j] + score["-"][y[j - 1]]
            insert = dp_table[i][j - 1] + score[x[i - 1]]["-"]

            optimalScore = max(align, remove, insert)

            if optimalScore == align:
                path = "diagonal"
            elif optimalScore == remove:
                path = "up"
            else:
                path = "left"

            dp_table[i][j] = optimalScore
            backTracker[i][j] = path

    final_score = dp_table[-1][-1]
    known, unknown = generateString(x, y, backTracker)
    return final_score, known, unknown


def initBaseCase(x, y, score, dp_table):
    i = 0
    while i < len(x):
        dp_table[i + 1][0] = dp_table[i][0] + score[x[i]]["-"]
        i += 1
    j = 0
    while j < len(y):
        dp_table[0][j + 1] = dp_table[0][j] + score["-"][y[j]]
        j += 1


def generateString(x, y, backTracker):
    i = len(x)
    j = len(y)
    known = ""
    unknown = ""
    while i > 0 and j > 0:
        if backTracker[i][j] == "diagonal":
            known = x[i - 1] + known
            unknown = y[j - 1] + unknown
            i -= 1
            j -= 1
        elif backTracker[i][j] == "up":
            known = x[i - 1] + known
            unknown = "-" + unknown
            i -= 1
        elif backTracker[i][j] == "left":
            known = "-" + known
            unknown = y[j - 1] + unknown
            j -= 1

    while i > 0:
        known = x[i - 1] + known
        unknown = "-" + unknown
        i -= 1

    while j > 0:
        known = "-" + known
        unknown = y[j - 1] + unknown
        j -= 1
    return known, unknown


def printResult(final_score, known, unknown):
    known = " ".join(list(known))
    unknown = " ".join(list(unknown))

    print(f"Alignment with score {final_score}:\n{known}\n{unknown}")


if __name__ == "__main__":
    fileName = sys.argv[1]
    x, y, score_matrix = parse(fileName)
    final_score, known, unknown = alignment(x, y, score_matrix)
    printResult(final_score, known, unknown)