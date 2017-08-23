from queue import Queue

from fastcat import FastCat


def get_child_categories(category, max_depth=1):
    f = FastCat()

    q = Queue()
    q.put((category, 0))

    res = list()

    while not q.empty():
        cat, depth = q.get()
        if depth == max_depth:
            break

        child_categories = f.narrower(cat)
        for c in child_categories:
            q.put((c, depth + 1))

        res += child_categories

    return res


if __name__ == '__main__':
    print(get_child_categories('関数型プログラミング', max_depth=2))
