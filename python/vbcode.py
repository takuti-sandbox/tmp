def to_bits(bytestream):
    return ''.join(list(map(lambda byte: '{0:08b}'.format(byte), bytestream)))


def vb_encode_number(n):
    """
    >>> to_bits(vb_encode_number(824))
    '0000011010111000'
    >>> to_bits(vb_encode_number(5))
    '10000101'
    >>> to_bits(vb_encode_number(214577))
    '000011010000110010110001'
    """
    res = []
    while True:
        res = [n % 128] + res  # prepend(bytes, n mod 128)
        if n < 128:
            break
        n //= 128
    res[len(res) - 1] += 128
    return res


def vb_encode(numbers):
    """
    >>> to_bits(vb_encode([824, 829, 215406]))
    '000001101011100010000101000011010000110010110001'
    """
    bytestream = []
    n_prev = 0
    for n in numbers:
        gap = n - n_prev
        bytestream += vb_encode_number(gap)
        n_prev = n
    return bytestream


def vb_decode(bits):
    """
    >>> vb_decode('000001101011100010000101000011010000110010110001')
    [824, 829, 215406]
    """
    gaps = []
    n = 0
    for head in range(0, len(bits), 8):
        byte = int(bits[head:(head + 8)], 2)
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            gaps.append(n)
            n = 0
    for i in range(1, len(gaps)):
        gaps[i] += gaps[i - 1]
    return gaps


if __name__ == '__main__':
    import doctest
    doctest.testmod()
