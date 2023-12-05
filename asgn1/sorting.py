import sys
import time


def selectionSort(lst):
    for i in range(len(lst)):
        smallestIdx = findMin(lst, i)
        lst[i], lst[smallestIdx] = lst[smallestIdx], lst[i]
    return lst


def findMin(lst, startIdx):
    smallest = lst[startIdx]
    smallestIdx = startIdx
    for i in range(startIdx, len(lst)):
        if smallest > lst[i]:
            smallest = lst[i]
            smallestIdx = i
    return smallestIdx


def mergeSort(lst):
    if len(lst) == 1:
        return lst

    mid = len(lst) // 2
    subLst1 = mergeSort(lst[0:mid])
    subLst2 = mergeSort(lst[mid:len(lst)])

    x = 0
    y = 0
    newLst = []

    while x < len(subLst1) and y < len(subLst2):
        if subLst1[x] < subLst2[y]:
            newLst.append(subLst1[x])
            x += 1
        else:
            newLst.append(subLst2[y])
            y += 1

    while x < len(subLst1):
        newLst.append(subLst1[x])
        x += 1

    while y < len(subLst2):
        newLst.append(subLst2[y])
        y += 1

    return newLst


def countingSort(lst):
    countMap = {}
    newLst = []
    for num in lst:
        countMap[num] = 1 + countMap.get(num, 0)

    for i in range(min(lst), max(lst) + 1):
        count = countMap.get(i, 0)
        if count != 0:
            newLst += [i] * count
    return newLst


def getRuntime(startTime):
    return time.time() - startTime


# fileName = sys.argv[1]
# fp = open(fileName, "r")
# arg = fp.read().split(",")
# lst = [int(x) for x in arg]
#
# startTime = time.time()
# result = selectionSort(lst)
# print(f"Selection Sort ({getRuntime(startTime)} ms): {str(result).replace('[', '').replace(']', '')}")
#
# lst = [int(x) for x in arg]  # Make unsorted list again
# startTime = time.time()
# result = mergeSort(lst)
# print(f"Merge Sort     ({getRuntime(startTime)} ms): {str(result).replace('[', '').replace(']', '')}")
#
# startTime = time.time()
# result = countingSort(lst)
# print(f"Counting Sort  ({getRuntime(startTime)} ms): {str(result).replace('[', '').replace(']', '')}")