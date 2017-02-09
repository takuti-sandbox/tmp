import numpy as np

"""SLIM: Sparse Linear Model

LibRec implementation: https://github.com/guoguibing/librec/blob/2.0.0/core/src/main/java/net/librec/recommender/cf/ranking/SLIMRecommender.java

"""

n_iter = 100
l1_reg = l2_reg = 0.1

n_user, n_item = 3, 5

A = np.array([[0, 2, 0, 1, 0],
              [0, 1, 1, 2, 1],
              [2, 0, 0, 1, 2]])

W = np.zeros((n_item, n_item))


def predict(u, i, i_exclude):
    """Make prediction for a pair of user `u` and item `i`, except for item `i_exclude`.
    """

    pred = 0.

    # Only consider items that user `u` has rated before.
    # This makes top-N recommendation faster.
    for j in range(n_item):
        rj = A[u, j]
        if rj == 0. or j == i_exclude:
            continue

        pred += (rj * W[j, i])

    return pred


def update_i(i):
    """Update coefficients for item `i`.
    """
    global loss

    # Using only some nearest-neighbors makes SLIM better,
    # but, currently all items are considered.
    nn_items = set(range(n_item))
    nn_items.remove(i)

    # For each nearest-neighbor item, update coefficents by coordinate descent.
    for j in nn_items:
        s_grad = s_rate = errors = 0.

        cnt = 0

        # For each user who has rated the nearest-neighbor item `j`.
        for u in range(n_user):
            rj = A[u, j]
            if rj == 0.:  # skip un-rated element
                continue

            # Get this user's rating for item `i`.
            ri = A[u, i]

            # Compute error between actual rating and prediction for a user-item pair.
            # Item `j` can be ignored from prediction.
            error = ri - predict(u, i, j)

            # Accumulates.
            s_grad += (rj * error)
            s_rate += (rj * rj)
            errors += (error + error)

            cnt += 1

        # Compute mean value of the accumulated values.
        s_grad /= cnt
        s_rate /= cnt
        errors /= cnt

        # Accumulated loss can be used to check convergence.
        coeff = W[j, i]
        loss += (errors + 0.5 * l2_reg * coeff * coeff + l1_reg * coeff)

        # Update a coefficient for a pair of item `i` and its neighbor `j`.
        update = 0.
        if l1_reg < abs(s_grad):
            if s_grad > 0.:
                update = (s_grad - l1_reg) / (l2_reg + s_rate)
            else:
                update = (s_grad + l1_reg) / (l2_reg + s_rate)
        W[j, i] = update


def is_converged(it):
    global loss_last

    delta = abs(loss_last - loss)
    loss_last = loss

    print(it, loss, delta)

    return (delta < 1e-3) if it > 1 else False


loss_last = float('inf')
for it in range(n_iter):
    # Can be used to check convergence.
    loss = 0.

    # Update the coefficients for each item.
    # This operation is parallelizable if coefficients `W` is protected correctly.
    for i in range(n_item):
        update_i(i)

    if is_converged(it):
        break

A_ = np.dot(A, W)
print(np.sqrt(sum(sum((A - A_) ** 2)) / A.size))  # RMSE
