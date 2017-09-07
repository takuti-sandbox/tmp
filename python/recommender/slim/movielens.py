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
    test_samples = {}

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
            if u not in test_samples:
                test_samples[u] = []
            test_samples[u].append((i, rating))

    return A, sp.lil_matrix((n_item, n_item)), test_samples


def update_i(i, k=5):
    """Update coefficients for item `i`.
    """
    wi = W[:, i]  # (n_item, 1)
    loss = 0

    # Using only some nearest-neighbors makes SLIM better,
    # but, for now randomly sampled k items are considered.
    others = set(range(n_item))
    others.remove(i)
    nn_items = set(np.random.choice(list(others), k, replace=False))

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
        pred = safe_sparse_dot(A[nz, :][:, ii], wi[ii, 0])
        error = (A[nz, i] - pred).toarray().reshape(nnz,)  # (nnz, )

        # Compute mean of accumulated values over the users who rated item `j`.
        errors = np.dot(error, error) / nnz
        s_grad = (A[nz, j].T * error)[0] / nnz
        s_rate = (A[nz, j].T * A[nz, j])[0, 0] / nnz

        # Accumulated loss can be used to check convergence.
        coeff = wi[j, 0]
        loss += (errors + 0.5 * l2_reg * coeff * coeff + l1_reg * coeff)

        # Update a coefficient for a pair of item `i` and its neighbor `j`.
        # Utilizing the soft-thresholding operator (e.g., Eq. (6) in [2]).
        update = 0.
        if l1_reg < abs(s_grad):
            if s_grad > 0.:
                update = (s_grad - l1_reg) / (l2_reg + s_rate)
            else:
                update = (s_grad + l1_reg) / (l2_reg + s_rate)
        wi[j, 0] = update

    return wi, loss


def evaluate_mae():
    A_ = safe_sparse_dot(A, W)

    s = 0.
    cnt = 0

    for u, ratings in test_samples.items():
        for i, rating in ratings:
            s += abs(A_[u, i] - rating)
            cnt += 1

    return s / cnt


def evaluate(n=10):
    A_ = safe_sparse_dot(A, W)

    # per-rating hit rates
    rHR = {1: 0., 2: 0., 3: 0., 4: 0., 5: 0.}

    # cumulative hit rates
    cHR = {1: 0., 2: 0., 3: 0., 4: 0., 5: 0.}

    for u, ratings in test_samples.items():
        # sort items in a descending order
        ranked_items = np.argsort(A_[u, :].toarray()[0])[::-1]

        # create top-n list of un-rated items
        rec = set([])
        for i in ranked_items:
            if A[u, i] == 0:
                rec.add(i)
            if len(rec) == n:
                break

        for r_th in [1, 2, 3, 4, 5]:
            truth = set([i for i, r in ratings if r == r_th])
            if len(rec & truth) > 0:
                rHR[r_th] += 1

            truth = set([i for i, r in ratings if r <= r_th])
            if len(rec & truth) > 0:
                cHR[r_th] += 1

    denom = len(test_samples)  # number of testing users
    for r_th in [1, 2, 3, 4, 5]:
        rHR[r_th] /= denom
        cHR[r_th] /= denom

    return rHR, cHR


print('load data...')
A, W, test_samples = load_data()
n_user, n_item = A.shape

print('start training...')
l1_reg = l2_reg = 0.1
n_iter = 100
accum_loss_ = float('inf')
for it in range(n_iter):
    pool = mp.Pool(mp.cpu_count())
    res = pool.map(update_i, range(n_item))
    pool.close()
    pool.join()

    # reduction
    accum_loss = 0
    for i, (wi, loss) in enumerate(res):
        W[:, i] = wi
        accum_loss += loss

    delta = abs(accum_loss_ - accum_loss)
    accum_loss_ = accum_loss
    if it > 1 and delta < 1e-3:
        break

print('evaluate...')

mae = evaluate_mae()
print('MAE: ', mae)

rHR, cHR = evaluate()
print('rHR: ', rHR)
print('cHR: ', cHR)
