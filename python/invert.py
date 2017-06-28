class Foo(object):

    def __init__(self, x):
        self.x = x

    def __invert__(self):
        return -self.x


if __name__ == '__main__':
    f = Foo(100)
    print(~f)
