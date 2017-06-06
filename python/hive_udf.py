import hashlib
import sys


for line in sys.stdin:
    line = line.strip()
    (name, address, age) = line.split('\t')

    x = hashlib.sha256(name.encode())
    name = x.hexdigest()

    print('\t'.join([name, address, age]))
