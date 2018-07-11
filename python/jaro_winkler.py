def jaro_winkler(s1, s2, p=0.1):
    """Jaro-Winkler similarity.

    - https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
    - https://github.com/tonytonyjan/jaro_winkler/blob/master/ext/jaro_winkler/jaro.c

    >>> jaro_winkler('ABC', '')
    0.0
    >>> jaro_winkler('ABC', 'DEF')
    0.0
    >>> jaro_winkler('ABC', 'ABC')
    1.0
    >>> jaro_winkler('CRATE', 'TRACE') < jaro_winkler('CRATE', 'CRACE')
    True
    """
    if s1 == s2:
        return 1.

    jaro_sim = jaro(s1, s2)

    ell = 0
    for i in range(min(4, min(len(s1), len(s2)))):
        if s1[i] != s2[i]:
            break
        ell += 1

    return jaro_sim + ell * p * (1 - jaro_sim)


def jaro(s1, s2):
    l1, l2 = len(s1), len(s2)

    if l1 == 0 or l2 == 0:
        return 0.

    # longer sentence is set to s2
    if l1 > l2:
        s1, s2 = s2, s1
        l1, l2 = l2, l1

    window_size = l2 // 2 - 1

    s1_matched, s2_matched = [0] * l1, [0] * l2

    match_count = 0
    for i in range(l1):
        left = i - window_size if (i >= window_size) else 0
        right = i + window_size if (i + window_size <= l2 - 1) else l2 - 1
        if right > l2 - 1:
            right = l2 - 1
        for j in range(left, right + 1):
            if s1[i] == s2[j]:
                match_count += 1
                s1_matched[i] = 1
                s2_matched[j] = 1
                break

    if match_count == 0:
        return 0.

    transposition_count = 0
    k = 0
    for i in range(l1):
        if s1_matched[i]:
            j = k
            while j < l2:
                if s2_matched[j]:
                    k = j + 1
                    break
                j += 1
            if s1[i] != s2[j]:
                transposition_count += 1

    m = match_count
    t = transposition_count / 2
    return (m / l1 + m / l2 + (m - t) / m) / 3


if __name__ == '__main__':
    import doctest
    doctest.testmod()
