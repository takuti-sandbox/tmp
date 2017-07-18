def func():
    return '111'


class Foo():

    def __str__(self):
        return func()
