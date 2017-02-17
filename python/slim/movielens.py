import numpy as np
import scipy.sparse as sp
import multiprocessing as mp
from sklearn.utils.extmath import safe_sparse_dot


def load_data():
    """
    # ML1M
    n_user, n_item = 6040, 3900

    PATH = '/Users/kitazawa/data/ml-1m/ratings.dat'
    with open(PATH) as f:
        lines = list(map(lambda l: l.rstrip().split('::'), f.readlines()))
        np.random.shuffle(lines)
    """

    # ML100k
    n_user, n_item = 943, 1682
    PATH = '/Users/kitazawa/data/ml-100k/u.data'
    with open(PATH) as f:
        lines = list(map(lambda l: l.rstrip().split('\t'), f.readlines()))
        np.random.shuffle(lines)

    n_train = int(len(lines) * 0.8)

    user_ids, item_ids = {}, {}
    cnt_u, cnt_i = 0, 0

    A = sp.lil_matrix((n_user, n_item))
    test_samples = []

    for j, l in enumerate(lines):
        user_id, item_id, rating, timestamp = int(l[0]), int(l[1]), float(l[2]), int(l[3])

        if user_id not in user_ids:
            user_ids[user_id] = cnt_u
            cnt_u += 1
        u = user_ids[user_id]

        if item_id not in item_ids:
            item_ids[item_id] = cnt_i
            cnt_i += 1
        i = item_ids[item_id]

        if j < n_train:
            A[u, i] = rating
        else:
            test_samples.append((u, i, rating))

    return A, sp.lil_matrix((n_item, n_item)), test_samples


def update_i(i):
    """Update coefficients for item `i`.
    """
    loss = 0

    # Using only some nearest-neighbors makes SLIM better,
    # but, currently all items are considered.
    nn_items = set(range(n_item)[:5])

    # For each nearest-neighbor item, update coefficents by coordinate descent.
    for j in nn_items:
        if i == j:
            continue

        # skip users who did not rate item `j`
        nz = A[:, j].nonzero()[0]
        nnz = nz.size

        # Compute error between actual rating and prediction for a user-item pair.
        # Item `j` should be ignored from prediction.
        ii = list(nn_items - set([j]))
        pred = safe_sparse_dot(A[nz, :][:, ii], W[ii, i])
        error = (A[nz, i] - pred).toarray().reshape(nnz,)  # (nnz, )

        # Compute mean of accumulated values over the users who rated item `j`.
        errors = np.dot(error, error) / nnz
        s_grad = (A[nz, j].T * error)[0] / nnz
        s_rate = (A[nz, j].T * A[nz, j])[0, 0] / nnz

        # Accumulated loss can be used to check convergence.
        coeff = W[j, i]
        loss += (errors + 0.5 * l2_reg * coeff * coeff + l1_reg * coeff)

        # Update a coefficient for a pair of item `i` and its neighbor `j`.
        # Utilizing the soft-thresholding operator (e.g., Eq. (6) in [2]).
        update = 0.
        if l1_reg < abs(s_grad):
            if s_grad > 0.:
                update = (s_grad - l1_reg) / (l2_reg + s_rate)
            else:
                update = (s_grad + l1_reg) / (l2_reg + s_rate)
        W[j, i] = update

    return loss


def evaluate():
    A_ = safe_sparse_dot(A, W)

    err = 0.
    for u, i, r in test_samples:
        err += ((A_[u, i] - r) ** 2)

    return np.sqrt(err / len(test_samples))  # RMSE


print('load data...')
A, W, test_samples = load_data()
n_user, n_item = A.shape

print('start training...')
l1_reg = l2_reg = 0.1
n_iter = 100
loss_last = float('inf')
for it in range(n_iter):
    pool = mp.Pool(mp.cpu_count())
    loss = sum(pool.map(update_i, range(n_item)))
    pool.close()
    pool.join()

    delta = abs(loss_last - loss)
    loss_last = loss
    if it > 1 and delta < 1e-3:
        break

print('evaluate...')
print(evaluate())
