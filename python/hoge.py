from abc import ABCMeta, abstractmethod


class Hoge:

    __metaclass__ = ABCMeta

    def __init__(self, a):
        print('hi~', a)

    @abstractmethod
    def hi(self, a):
        if a == 0:
            print('HOGE!!!')
            return


class Fuga(Hoge):

    def __init__(self):
        super().__init__('there')
        print('haoooo')

    def hi(self, a):
        super().hi(a)
        print('Fuga!!!')


if __name__ == '__main__':
    Fuga()
