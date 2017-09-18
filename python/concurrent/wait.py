import time
from concurrent import futures


def wait():
    time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    wait()
    wait()
    end = time.time()
    print('Single:        elapsed time = {}'.format(end - start))

    start = time.time()
    with futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(wait)
        f2 = executor.submit(wait)
        f1.result()
        f2.result()
    end = time.time()
    print('Multi-thread:  elapsed time = {}'.format(end - start))

    start = time.time()
    with futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(wait)
        f2 = executor.submit(wait)
        f1.result()
        f2.result()
    end = time.time()
    print('Multi-process: elapsed time = {}'.format(end - start))
