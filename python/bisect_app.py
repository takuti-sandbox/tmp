def bisect(arr, val):
    if len(arr) == 0:
        return 0
    if val < arr[0]:
        return 0
    if arr[-1] < val:
        return len(arr)

    lo, hi = 0, len(arr) - 1

    while lo < hi:
        if val == arr[lo]:
            return lo
        elif val == arr[hi]:
            return hi

        mid = (lo + hi) // 2

        if val == arr[mid]:
            return mid
        elif val < arr[mid]:
            hi = mid
        else:
            lo = mid + 1

    return lo


class User(object):

    def __init__(self):
        self.tweets = []

    def tweet(self, datetime, text):
        self.tweets.append((datetime, text))


def last_before(timestamp, arr):
    """
    arr[i] := (timestamp, value)
    """
    pos = bisect(arr, (timestamp, ''))
    if pos == 0:
        return ''
    if pos == len(arr):
        return arr[-1][1]
    if arr[pos][0] == timestamp:
        return arr[pos][1]
    return arr[pos-1][1]


if __name__ == '__main__':
    user = User()
    user.tweet(20201011, 'Hello, world.')
    user.tweet(20201201, 'I am hungry.')
    user.tweet(20201231, 'Sleepy...')
    user.tweet(202101015, 'Happy New Year!')
    print(last_before(20210101, user.tweets))
