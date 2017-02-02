# coding: utf-8
import itertools
import math


primes = set([])


def is_prime(n):
    """n > 2

    """
    if n in primes:
        return -1

    for i in xrange(2, (int(math.sqrt(n)) + 1) + 1):
        if n % i == 0:
            return i
    primes.add(n)
    return -1


def convert(bits, base):
    x = base
    ans = 1.  # last 1 bit
    for b in bits[::-1]:
        ans += (b * x)
        x *= base
    ans += x  # first 1 bit
    return ans


def check(bits):
    divisors = [0] * 9
    for base in range(2, 11):
        v = convert(bits, base)

        divisor = is_prime(v)
        if divisor == -1:
            return False, []
        divisors[base - 2] = divisor

    return True, divisors


def solve(t, N, J):
    print 'Case #%d:' % (t + 1)
    cnt = 0
    for bits in set(itertools.product([0, 1], repeat=(N - 2))):
        flg, divisors = check(bits)
        if not flg:
            continue

        print '%s %s' % (''.join(map(str, bits)), ' '.join(map(str, divisors)))

        cnt += 1
        if cnt == J:
            return


def main():
    T = input()
    for t in xrange(T):
        N, J = [int(v) for v in raw_input().rstrip().split(' ')]
        solve(t, N, J)


if __name__ == '__main__':
    main()
