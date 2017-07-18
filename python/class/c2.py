import c1
from c1 import Foo


def func():
    return '222'


def func2():
    return '222'


class Bar(Foo):

    def __str__(self):
        return func()


print('Foo: %s' % Foo())
print('Bar: %s' % Bar())

c1.func = func2
print('Foo: %s' % Foo())
