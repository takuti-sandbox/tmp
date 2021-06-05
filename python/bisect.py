def debug_print(arr, lo, mid, hi):
    l1 = map(lambda v: '%3d' % v, arr)
    l2 = ['   '] * len(arr)
    l2[lo] = '  ^'
    l2[mid] = '  ^'
    l2[hi] = '  ^'
    l3 = ['   '] * len(arr)
    l3[lo] = '  L'
    l3[mid] = '  M'
    l3[hi] = '  H'
    l4 = ['   '] * len(arr)
    if lo == hi:
        l4[lo] = '  L'
    if mid == hi:
        l4[mid] = '  M'
    l5 = ['   '] * len(arr)
    if lo == mid:
        l5[lo] = '  L'
    print(' '.join(l1))
    print(' '.join(l2))
    print(' '.join(l3))
    print(' '.join(l4))
    print(' '.join(l5))


def search(arr, val):
    """
    >>> search([2, 4, 8, 16, 32], 1)
    0
    >>> search([2, 4, 8, 16, 32], 4)
    1
    >>> search([2, 4, 8, 16, 32], 3)
    1
    >>> search([2, 4, 8, 16, 32], 10)
    3
    >>> search([2, 4, 8, 16, 32], 64)
    5
    """
    if val < arr[0]:
        return 0

    for i in range(1, len(arr)):
        if arr[i-1] < val and val <= arr[i]:
            return i

    return len(arr)


def bisect(arr, val, debug=False):
    """Bisection algorithm

    Return an index of an ascending-ordered array `arr` where `val` can be
    inserted. A returned index `i` indicates a potential insertion point, and
    `arr[i:]` must come after `val` once inserted.

    >>> bisect([2, 4, 8, 16, 32], 1)
    0
    >>> bisect([2, 4, 8, 16, 32], 4)
    1
    >>> bisect([2, 4, 8, 16, 32], 3)
    1
    >>> bisect([2, 4, 8, 16, 32], 10)
    3
    >>> bisect([2, 4, 8, 16, 32], 64)
    5
    """
    if len(arr) == 0:
        return 0
    if val < arr[0]:
        return 0
    if arr[-1] < val:
        return len(arr)

    lo, hi = 0, len(arr) - 1

    while lo < hi:
        if val == arr[lo]:
            return lo
        elif val == arr[hi]:
            return hi

        mid = (lo + hi) // 2

        if debug:
            debug_print(arr, lo, mid, hi)

        if val == arr[mid]:
            return mid
        elif val < arr[mid]:
            hi = mid
        else:
            lo = mid + 1

    if debug:
        debug_print(arr, lo, mid, hi)
    return lo


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    bisect([2, 4, 8, 16, 32], 10, debug=True)
    # import random
    # bisect(sorted(random.sample(range(100), 10)), 50, debug=True)
