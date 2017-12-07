def f():
    """
    >>> 1
    1
    >>> 1 # doctest: +SKIP
    2
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
