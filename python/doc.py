"""This is it.

Hello.

Foo!!
"""


class Foo(object):
    """I am Foo."""

    def __str__(self):
        return self.__doc__


class Bar(object):
    """I am Bar."""

    def __str__(self):
        return __doc__


if __name__ == '__main__':
    print(__doc__)
    print(Foo())
    print(Bar())
