"""Matrix Factorization using PyTorch

http://blog.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
"""

import random
import numpy as np
import torch
from torch import autograd, nn, optim


class MatrixFactorization(nn.Module):

    def __init__(self, n_user, n_item, k=20):
        super().__init__()

        self.user_factors = nn.Embedding(n_user, k, sparse=True)
        self.item_factors = nn.Embedding(n_item, k, sparse=True)

    def forward(self, user, item):
        return (self.user_factors(user) * self.item_factors(item)).sum(1)


def load_ml100k():
    with open('/Users/kitazawa/data/movielens/ml-100k/u.data') as f:
        return list(map(lambda l: l.rstrip().split('\t'), f.readlines()))


def as_long_tensor(val):
    return torch.LongTensor([np.long(val)])


def as_float_tensor(val):
    return torch.FloatTensor([np.long(val)])


def main():
    data = load_ml100k()
    n_user, n_item = 943, 1682

    model = MatrixFactorization(n_user + 1, n_item + 1)  # +1 for unused "0" index
    loss_function = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-2)

    last_accum_loss = float('inf')
    for epoch in range(10):
        accum_loss = 0
        random.shuffle(data)
        for sample in data:
            u, i, r = sample[0], sample[1], sample[2]

            model.zero_grad()

            user = autograd.Variable(as_long_tensor(u))
            item = autograd.Variable(as_long_tensor(i))
            rating = autograd.Variable(as_float_tensor(r))

            prediction = model(user, item)

            loss = loss_function(prediction, rating)
            accum_loss += loss.data[0]

            loss.backward()

            optimizer.step()

        print(epoch + 1, accum_loss)
        if abs(accum_loss - last_accum_loss) < 1e-3:
            break
        last_accum_loss = accum_loss

    err = 0.
    for sample in data:
        u, i, r = sample[0], sample[1], sample[2]
        user = autograd.Variable(as_long_tensor(u))
        item = autograd.Variable(as_long_tensor(i))
        prediction = model(user, item)
        err += abs(prediction.data[0] - np.float(r))
    print('MAE = {}'.format(err / len(data)))


if __name__ == '__main__':
    main()
