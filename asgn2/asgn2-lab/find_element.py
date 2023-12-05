import sys


def find_element(lst):
    res = binarySearch(lst)
    if res is None:
        res = mergeSearch(lst)
    return res


def binarySearch(lst):
    if len(lst) == 2:
        if lst[0] + 1 != lst[1]:
            return lst[0] + 1
        else:
            return None

    mid = len(lst) // 2

    if lst[mid] + 1 != lst[mid + 1]:
        return lst[mid] + 1

    left = lst[0:mid]
    right = lst[mid:len(lst)]

    if hasMissing(left) and not hasMissing(right):
        return binarySearch(left)
    elif not hasMissing(left) and hasMissing(right):
        return binarySearch(right)
    else:
        return None


def hasMissing(lst):
    return len(lst) - 1 != lst[-1] - lst[0]


def mergeSearch(lst):
    if len(lst) == 1:
        return None
    if len(lst) == 2:
        if lst[0] + 1 != lst[1]:
            return lst[0] + 1
        else:
            return None

    mid = len(lst) // 2

    if lst[mid] + 1 != lst[mid + 1]:
        return lst[mid] + 1

    left = lst[0:mid]
    right = lst[mid:len(lst)]

    left_res = mergeSearch(left)
    right_res = mergeSearch(right)

    if left_res is not None:
        return left_res
    if right_res is not None:
        return right_res
    return None


if __name__ == "__main__":
    fileName = sys.argv[1]
    fp = open(fileName, "r")
    string_lst = fp.read().replace("\n", "").split(",")
    lst = [int(num) for num in string_lst]

    print(find_element(lst))
