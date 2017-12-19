"""http://michaelnielsen.org/blog/consistent-hashing/"""

import bisect
import hashlib


def my_hash(key):
    """Returns a hash value in a [0, 1) range.
    """
    md5_hash_int = int(hashlib.md5(key.encode('ascii')).hexdigest(), 16)
    n = 1000000
    mod = md5_hash_int % n
    return mod / float(n)  # scale in a [0, 1) range


class ConsistentHash(object):

    def __init__(self, num_machines=1, num_replicas=1):
        self.num_machines = num_machines
        self.num_replicas = num_replicas

        # Allocate each replica (machine) onto a point of the unit circle
        hash_tuples = [(mi, ri, my_hash('{}_{}'.format(mi, ri)))
                       for mi in range(self.num_machines)
                       for ri in range(self.num_replicas)]

        # Sort replica assignment information based on its hash value
        hash_tuples.sort(key=lambda t: t[2])
        self.hash_tuples = hash_tuples

    def get_machine(self, key):
        h = my_hash(key)

        # If a hash value is greater than the largest one (i.e., very close to
        # 1.0 on the unit circle), cyclically back to 0.0.
        if h > self.hash_tuples[-1][2]:
            return self.hash_tuples[0][0]
        hash_values = [t[2] for t in self.hash_tuples]

        # Find the closest hash value and use corresponding machine (replica)
        # to store a value of the key
        index = bisect.bisect_left(hash_values, h)
        return self.hash_tuples[index][0]


def main():
    # Consistent Hashing over 7 machines and 3 replicas for each of them
    ch = ConsistentHash(7, 3)

    print('Allocation:\n(machine, replica, hash)')
    for mi, ri, h in ch.hash_tuples:
        print('({}, {}, {})'.format(mi, ri, h))

    while True:
        key = input('Enter a key: ')
        print('Key `%s` is mapped onto a (scaled) hash value `%f`, and its value would be stored into a machine `%d`' % (key, my_hash(key), ch.get_machine(key)))


if __name__ == '__main__':
    main()
