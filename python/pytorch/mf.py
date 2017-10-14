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


def as_long_tensor(val):
    return torch.LongTensor([np.long(val)])


def as_float_tensor(val):
    return torch.FloatTensor([np.long(val)])


def main():
    # 5 users * 6 items
    R = np.array([[5, 0, 1, 1, 0, 2],
                  [0, 2, 0, 4, 0, 4],
                  [4, 5, 0, 1, 1, 2],
                  [0, 0, 3, 5, 2, 0],
                  [2, 0, 1, 0, 4, 4]])
    n_user, n_item = R.shape

    model = MatrixFactorization(n_user, n_item)
    loss_function = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-6)

    last_accum_loss = float('inf')
    indices = list(zip(range(n_user), range(n_item)))
    while True:
        accum_loss = 0
        random.shuffle(indices)
        for u, i in indices:
            r = R[u, i]
            if r == 0.:
                continue

            model.zero_grad()

            user = autograd.Variable(as_long_tensor(u))
            item = autograd.Variable(as_long_tensor(i))
            rating = autograd.Variable(as_float_tensor(r))

            prediction = model(user, item)

            loss = loss_function(prediction, rating)
            accum_loss += loss.data[0]

            loss.backward()

            optimizer.step()

        if abs(accum_loss - last_accum_loss) < 1e-3:
            break
        last_accum_loss = accum_loss

    for u in range(n_user):
        for i in range(n_item):
            user = autograd.Variable(as_long_tensor(u))
            item = autograd.Variable(as_long_tensor(i))
            prediction = model(user, item)
            print(u, i, R[u, i], prediction.data[0])


if __name__ == '__main__':
    main()
