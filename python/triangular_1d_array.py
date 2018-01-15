"""Efficiently hold triangular matrix (i.e., symmetric matrix) in a 1d array.

See p. 211 in MMDS Ch. 6: http://infolab.stanford.edu/~ullman/mmds/ch6.pdf
"""


def create_triangular_array(n_items):
    # `n_items` corresponds to the number of rows and columns
    n_elements = n_items * (n_items - 1) // 2  # no need to store self reference
    return [0 for i in range(n_elements)]


def get_triangle_index(i, j, n):
    assert (0 <= i and i < n) and (0 <= j and j < n), 'Indices must be in [0, n).'
    assert i != j, 'Cannot access to the diagonal elements in a matrix.'

    if j < i:  # 0 <= i < j < n_items
        i, j = j, i

    return (i * (n - (i + 1) // 2) + j - i) - 1


if __name__ == '__main__':
    # 3x3 trinangular matrix
    n_items = 3
    mat = [[1, 2, 3],
           [2, 1, 4],
           [3, 4, 1]]

    ary = create_triangular_array(n_items)

    # set elements in `mat` to `ary`
    for i in range(n_items):
        for j in range(n_items):
            if i == j:
                continue
            k = get_triangle_index(i, j, n_items)
            ary[k] = mat[i][j]

    # check if the values are properly stored
    for i in range(n_items):
        s = ''
        for j in range(n_items):
            if i == j:
                s += 'x'  # unstored for diagonal
            else:
                k = get_triangle_index(i, j, n_items)
                s += str(ary[k])
            s += ' '
        print(s)
