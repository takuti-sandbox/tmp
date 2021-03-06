"""Matrix Factorization using PyTorch

http://blog.ethanrosenthal.com/2017/06/20/matrix-factorization-in-pytorch/
"""

import csv
import random
import numpy as np
import torch
from torch import autograd, nn, optim
from concurrent import futures

from logging import getLogger, StreamHandler, Formatter, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)s : %(process)d : %(message)s'))
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class MatrixFactorization(object):

    def __init__(self, n_user, n_item, k=20, lr=1e-6, weight_decay=0.):
        self.user_factors = np.random.rand(n_user, k)
        self.item_factors = np.random.rand(n_item, k)
        self.lr = lr
        self.weight_decay = weight_decay

    def predict(self, user, item):
        return np.inner(self.user_factors[user], self.item_factors[item])

    def __call__(self, user, item, rating):
        err = rating - self.predict(user, item)

        user_factor, item_factor = self.user_factors[user], self.item_factors[item]
        next_user_factor = user_factor - self.lr * (-2. * (err * item_factor - self.weight_decay * user_factor))
        next_item_factor = item_factor - self.lr * (-2. * (err * user_factor - self.weight_decay * item_factor))

        self.user_factors[user], self.item_factors[item] = next_user_factor, next_item_factor

        return err


def run_mf(samples_train, samples_test, n_user, n_item):
    logger.info('mf : start training')

    model = MatrixFactorization(n_user, n_item, k=20, lr=1e-3)

    last_accum_loss = float('inf')
    for epoch in range(10):
        accum_loss = 0
        random.shuffle(samples_train)
        for u, i, r in samples_train:
            accum_loss += model(u, i, r)

        logger.info('mf : epoch = {:2d}, accum. error = {}'.format(epoch + 1, accum_loss))
        if abs(accum_loss - last_accum_loss) < 1e-3:
            break
        last_accum_loss = accum_loss

    accum_absolute_error, accum_squared_error = 0., 0.
    for u, i, r in samples_test:
        prediction = model.predict(u, i)

        accum_absolute_error += abs(prediction - r)
        accum_squared_error += (prediction - r) ** 2
    mae = accum_absolute_error / len(samples_test)
    rmse = np.sqrt(accum_squared_error / len(samples_test))
    logger.info('mf : MAE = {}, RMSE = {}'.format(mae, rmse))


class MatrixFactorizationPyTorch(nn.Module):

    def __init__(self, n_user, n_item, k=20):
        super().__init__()

        self.user_factors = nn.Embedding(n_user, k, sparse=True)
        self.item_factors = nn.Embedding(n_item, k, sparse=True)

    def forward(self, user, item):
        # inner product of 1xN and 1xM tensors
        return (self.user_factors(user) * self.item_factors(item)).sum(1)


def as_long_tensor(val):
    return torch.LongTensor([np.long(val)])


def as_float_tensor(val):
    return torch.FloatTensor([np.long(val)])


def run_mf_pytorch(samples_train, samples_test, n_user, n_item):
    logger.info('mf_pytorch : start training')

    model = MatrixFactorizationPyTorch(n_user, n_item, k=20)
    loss_function = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-2)

    last_accum_loss = float('inf')
    for epoch in range(10):
        accum_loss = 0
        random.shuffle(samples_train)
        for u, i, r in samples_train:
            model.zero_grad()

            user = autograd.Variable(as_long_tensor(u))
            item = autograd.Variable(as_long_tensor(i))
            rating = autograd.Variable(as_float_tensor(r))  # target

            prediction = model(user, item)

            loss = loss_function(prediction, rating)
            accum_loss += loss.data[0]

            loss.backward()

            optimizer.step()

        logger.info('mf_pytorch : epoch = {:2d}, accum. loss = {}'.format(epoch + 1, accum_loss))
        if abs(accum_loss - last_accum_loss) < 1e-3:
            break
        last_accum_loss = accum_loss

    accum_absolute_error, accum_squared_error = 0., 0.
    for u, i, r in samples_test:
        user = autograd.Variable(as_long_tensor(u))
        item = autograd.Variable(as_long_tensor(i))

        prediction = model(user, item)

        accum_absolute_error += abs(prediction.data[0] - r)
        accum_squared_error += (prediction.data[0] - r) ** 2
    mae = accum_absolute_error / len(samples_test)
    rmse = np.sqrt(accum_squared_error / len(samples_test))
    logger.info('mf_pytorch : MAE = {}, RMSE = {}'.format(mae, rmse))


def load_ml100k():
    samples = []
    with open('/Users/kitazawa/data/movielens/ml-100k/u.data', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            u, i, r = int(row[0]) - 1, int(row[1]) - 1, float(row[2])
            samples.append((u, i, r))
    return samples


if __name__ == '__main__':
    samples = load_ml100k()
    n_user, n_item = 943, 1682

    # 8:2 train/test splitting
    random.shuffle(samples)
    tail_train = int(len(samples) * 0.8)
    samples_train = samples[:tail_train]
    samples_test = samples[tail_train:]

    with futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(run_mf,
                             samples_train.copy(), samples_test.copy(),
                             n_user, n_item)
        f2 = executor.submit(run_mf_pytorch,
                             samples_train.copy(), samples_test.copy(),
                             n_user, n_item)
        f1.result()
        f2.result()
