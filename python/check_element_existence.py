import bisect
import time


def search_bisect(a, x):
    i = bisect.bisect_left(a, x)
    return i != len(a) and a[i] == x


def search_set(s, x):
    return x in s


if __name__ == '__main__':
    a = list(range(10000000))
    x = 10  # search target

    start = time.time()
    for i in range(10000):
        search_bisect(a, x)
    print('bisect:\t%f' % (time.time() - start))

    s = set(a)
    start = time.time()
    for i in range(10000):
        search_set(s, x)
    print('set:\t%f' % (time.time() - start))
