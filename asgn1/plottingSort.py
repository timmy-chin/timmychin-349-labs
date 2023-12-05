import random
import time

from sorting import *


def plot():
    fp = open("sortPlot.csv", "a")
    fp.write("Selection Sort,Merge Sort,Counting Sort\n")
    for size in range(1000, 50001, 1000):
        print(f"Sorting size of {size}")
        lst = generateList(size)

        startTime = time.time()
        mergeSort(lst)
        mergeTime = getRuntime(startTime)

        startTime = time.time()
        countingSort(lst)
        countingTime = getRuntime(startTime)

        startTime = time.time()
        selectionSort(lst)
        selectionRuntime = getRuntime(startTime)

        fp.write(f"{selectionRuntime},{mergeTime},{countingTime}\n")


def generateList(size):
    return [random.randint(-10000000, 10000000) for i in range(size)]



plot()
