def diff(lst1: list, lst2: list):
    return [value for value in lst1 if not value in lst2]


def intersection(lst1: list, *args):
    lst1 = lst1
    for lst2 in args:
        lst1 = [value for value in lst1 if value in lst2]
    return lst1


def intersection_list_organs(lst: list):
    out = lst.pop(0)
    for sub in lst:
        out = intersection(out, sub)
    return out
