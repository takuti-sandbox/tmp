import math
from concurrent import futures


def is_prime(n):
    """
    >>> is_prime(41)
    True
    >>> is_prime(42)
    False
    """
    if n == 1:
        return False
    elif n == 2:
        return True

    for i in range(2, (int(math.sqrt(n)) + 1) + 1):
        if n % i == 0:
            return False

    return True


values = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419,
]


def task_single():
    for value in values:
        print(value, is_prime(value))


def task_multithread():
    with futures.ThreadPoolExecutor() as executor:
        future_to_value = {executor.submit(is_prime, value): value for value in values}
        for future in futures.as_completed(future_to_value):
            print(future_to_value[future], future.result())


def task_multiprocess():
    with futures.ProcessPoolExecutor() as executor:
        future_to_value = {executor.submit(is_prime, value): value for value in values}
        for future in futures.as_completed(future_to_value):
            print(future_to_value[future], future.result())


if __name__ == '__main__':
    import time
    import sys

    if len(sys.argv) < 2:
        exit()

    start = time.time()

    if sys.argv[1] == 'single':
        task_single()
    elif sys.argv[1] == 'multithread':
        task_multithread()
    elif sys.argv[1] == 'multiprocess':
        task_multiprocess()

    end = time.time()

    print('{}: elapsed time = {}'.format(sys.argv[1], end - start))
