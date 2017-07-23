import time


def print_array2d(ary, rows, cols):
    n = len(rows)
    m = len(cols)

    line = '   |'
    for j in range(m):
        line += '  %c' % cols[j]
    print('%s\n%s' % (line, '-' * len(line)))

    for i in range(n):
        line = ' %c |' % rows[i]

        for j in range(m):
            line += '%3d' % ary[i][j]
        print(line)

    for _ in range(n + 2):
        print('\x1b[A', end='')

    time.sleep(1)


def levenshtein(s1, s2):
    l1, l2 = len(s1), len(s2)
    dp = [[0] * (l2 + 1) for i1 in range(l1 + 1)]

    for i1 in range(l1 + 1):
        dp[i1][0] = i1

    for i2 in range(l2 + 1):
        dp[0][i2] = i2

    print_array2d(dp, '-' + s1, '-' + s2)

    for i1 in range(1, l1 + 1):
        for i2 in range(1, l2 + 1):
            cost = 0 if s1[i1 - 1] == s2[i2 - 1] else 1
            dp[i1][i2] = min(dp[i1 - 1][i2] + 1, dp[i1][i2 - 1] + 1, dp[i1 - 1][i2 - 1] + cost)

            print_array2d(dp, '-' + s1, '-' + s2)

    return dp[l1][l2]


if __name__ == '__main__':
    levenshtein('kitten', 'sitting')
