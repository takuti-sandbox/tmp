import numpy as np
from slim import SLIM


l1_reg = l2_reg = 0.1

n_user, n_item = 3, 5

A = np.array([[0, 2, 0, 1, 0],
              [0, 1, 1, 2, 1],
              [2, 0, 0, 1, 2]])

slim = SLIM(A, n_user, n_item, l1_reg, l2_reg)

loss_last = float('inf')
for it in range(50):
    loss = 0.
    for i in range(n_item):
        loss += slim.update_i(i)

    delta = abs(loss_last - loss)
    loss_last = loss
    if it > 1 and delta < 1e-3:
        break

print(np.dot(slim.A, slim.W).toarray())
