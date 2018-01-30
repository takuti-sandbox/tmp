class ClazzA(object):

    def __init__(self, a=10, b=20, **kwargs):
        ClazzB(**kwargs)


class ClazzB(object):

    def __init__(self, c=0, d=0):
        print(c, d)


if __name__ == '__main__':
    ClazzA(a=1, c=100, d=200)  # => 100, 200
