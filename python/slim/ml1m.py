import numpy as np
from slim import SLIM


print('load data...')

PATH_TO_ML1M = '/Users/kitazawa/data/ml-1m/ratings.dat'
with open(PATH_TO_ML1M) as f:
    lines = list(map(lambda l: l.rstrip().split('::'), f.readlines()))
    np.random.shuffle(lines)

n_user, n_item = 6040, 3900

n_sample = len(lines)
n_train = int(n_sample * 0.8)
n_test = n_sample - n_train

A = np.zeros((n_user, n_item))

user_ids, item_ids = {}, {}
cnt_u, cnt_i = 0, 0
for l in lines[:n_train]:
    user_id, item_id, rating, timestamp = int(l[0]), int(l[1]), float(l[2]), int(l[3])

    if user_id not in user_ids:
        user_ids[user_id] = cnt_u
        cnt_u += 1
    u = user_ids[user_id]

    if item_id not in item_ids:
        item_ids[item_id] = cnt_i
        cnt_i += 1
    i = item_ids[item_id]

    A[u, i] = rating

print('initialize SLIM recommender...')
l1_reg = l2_reg = 0.1
slim = SLIM(A, n_user, n_item, l1_reg, l2_reg)

print('start training...')
n_iter = 100
loss_last = float('inf')
for it in range(n_iter):
    # Can be used to check convergence.
    loss = 0.

    # Update the coefficients for each item.
    # This operation is parallelizable if coefficients `W` is protected correctly.
    for i in range(n_item):
        loss += slim.update_i(i)

    delta = abs(loss_last - loss)
    loss_last = loss
    if it > 1 and delta < 1e-3:
        break

print('evaluate...')
A_ = np.dot(slim.A, slim.W)
err = 0.
for l in lines[n_train:]:
    user_id, item_id, rating, timestamp = int(l[0]), int(l[1]), float(l[2]), int(l[3])
    u = user_ids[user_id]
    i = item_ids[item_id]
    err += ((A_[u, i] - rating) ** 2)
print(np.sqrt(err / n_test))  # RMSE
