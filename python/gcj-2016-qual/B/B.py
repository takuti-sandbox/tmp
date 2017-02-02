# coding: utf-8


def solve(s):
    cnt = 0

    while True:
        if '-' not in s:
            break

        tail = 1
        while tail < len(s) and s[tail] == s[0]:
            tail += 1

        s_ = ''
        for i in range(tail - 1, -1, -1):
            s_ += ('-' if s[i] == '+' else '+')

        s = s_ + s[tail:]
        cnt += 1

    return cnt


def main():
    T = input()
    for t in xrange(T):
        s = raw_input().rstrip()
        print 'Case #%d: %d' % (t + 1, solve(s))


if __name__ == '__main__':
    main()
