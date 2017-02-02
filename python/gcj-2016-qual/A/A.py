# coding: utf-8


def solve(N):
    s = set([])
    prev = set([N])
    N_ = N
    while True:
        for c in str(N_):
            s.add(c)
        if len(s) == 10:
            break
        N_ += N
        if N_ in prev:
            return 'INSOMNIA'
        prev.add(N_)
    return N_


def main():
    T = input()
    for i in xrange(T):
        N = input()
        print 'Case #%s: %s' % (i + 1, solve(N))

if __name__ == '__main__':
    main()
