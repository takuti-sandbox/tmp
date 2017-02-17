import numpy as np

"""SLIM: Sparse Linear Model

LibRec implementation:
https://github.com/guoguibing/librec/blob/2.0.0/core/src/main/java/net/librec/recommender/cf/ranking/SLIMRecommender.java

[1] Xia Ning and George Karypis, SLIM: Sparse Linear Methods for Top-N Recommender Systems, ICDM 2011.
[2] Friedman et al., Regularization Paths for Generalized Linear Models via Coordinate Descent, Journal of Statistical Software, 2010.

"""


class SLIM:

    def __init__(self, A, n_user, n_item, l1_reg=0.1, l2_reg=0.1):
        self.A = A
        self.n_user = n_user
        self.n_item = n_item

        self.W = np.zeros((self.n_item, self.n_item))

        self.l1_reg = l1_reg
        self.l2_reg = l2_reg

    def predict(self, u, i, i_exclude):
        """Make prediction for a pair of user `u` and item `i`, except for item `i_exclude`.
        """
        pred = 0.

        # Only consider items that user `u` has rated before.
        # This makes top-N recommendation faster.
        for j in range(self.n_item):
            rj = self.A[u, j]
            if rj == 0. or j == i_exclude:
                continue

            pred += (rj * self.W[j, i])

        return pred

    def update_i(self, i):
        """Update coefficients for item `i`.
        """
        loss = 0

        # Using only some nearest-neighbors makes SLIM better,
        # but, currently all items are considered.
        nn_items = set(range(self.n_item))
        nn_items.remove(i)

        # For each nearest-neighbor item, update coefficents by coordinate descent.
        for j in nn_items:
            s_grad = s_rate = errors = 0.

            cnt = 0

            # For each user who has rated the nearest-neighbor item `j`.
            for u in range(self.n_user):
                rj = self.A[u, j]
                if rj == 0.:  # skip un-rated element
                    continue

                # Get this user's rating for item `i`.
                ri = self.A[u, i]

                # Compute error between actual rating and prediction for a user-item pair.
                # Item `j` can be ignored from prediction.
                error = ri - self.predict(u, i, j)

                # Accumulates.
                s_grad += (rj * error)
                s_rate += (rj * rj)
                errors += (error * error)

                cnt += 1

            # Compute mean value of the accumulated values.
            s_grad /= cnt
            s_rate /= cnt
            errors /= cnt

            # Accumulated loss can be used to check convergence.
            coeff = self.W[j, i]
            loss += (errors + 0.5 * self.l2_reg * coeff * coeff + self.l1_reg * coeff)

            # Update a coefficient for a pair of item `i` and its neighbor `j`.
            update = self.__soft_thresholding(s_grad, self.l1_reg) / (self.l2_reg + s_rate)
            self.W[j, i] = update

        return loss

    def __soft_thresholding(self, z, r):
        """The soft-thresholding operator (e.g., Eq. (6) in [2]).
        """
        if r < abs(z):
            if z > 0.:
                return z - r
            else:
                return z + r
        return 0.
