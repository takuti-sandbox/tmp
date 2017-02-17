import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import safe_sparse_dot

"""SLIM: Sparse Linear Model

LibRec implementation:
https://github.com/guoguibing/librec/blob/2.0.0/core/src/main/java/net/librec/recommender/cf/ranking/SLIMRecommender.java

[1] Xia Ning and George Karypis, SLIM: Sparse Linear Methods for Top-N Recommender Systems, ICDM 2011.
[2] Friedman et al., Regularization Paths for Generalized Linear Models via Coordinate Descent, Journal of Statistical Software, 2010.

"""


class SLIM:

    def __init__(self, A, n_user, n_item, l1_reg=0.1, l2_reg=0.1):
        self.A = sp.lil_matrix(A)
        self.n_user = n_user
        self.n_item = n_item

        self.W = sp.lil_matrix((self.n_item, self.n_item))

        self.l1_reg = l1_reg
        self.l2_reg = l2_reg

    def update_i(self, i):
        """Update coefficients for item `i`.
        """
        loss = 0

        # Using only some nearest-neighbors makes SLIM better,
        # but, currently all items are considered.
        nn_items = set(range(self.n_item))

        # For each nearest-neighbor item, update coefficents by coordinate descent.
        for j in nn_items:
            if i == j:
                continue

            # skip users who did not rate item `j`
            nz = self.A[:, j].nonzero()[0]
            nnz = nz.size

            # Compute error between actual rating and prediction for a user-item pair.
            # Item `j` should be ignored from prediction.
            ii = list(nn_items - set([j]))
            pred = safe_sparse_dot(self.A[nz, :][:, ii], self.W[ii, i])
            error = (self.A[nz, i] - pred).toarray().reshape(nnz,)  # (nnz, )

            # Compute mean of accumulated values over the users who rated item `j`.
            errors = np.dot(error, error) / nnz
            s_grad = (self.A[nz, j].T * error)[0] / nnz
            s_rate = (self.A[nz, j].T * self.A[nz, j])[0, 0] / nnz

            # Accumulated loss can be used to check convergence.
            coeff = self.W[j, i]
            loss += (errors + 0.5 * self.l2_reg * coeff * coeff + self.l1_reg * coeff)

            # Update a coefficient for a pair of item `i` and its neighbor `j`.
            # Utilizing the soft-thresholding operator (e.g., Eq. (6) in [2]).
            update = 0.
            if self.l1_reg < abs(s_grad):
                if s_grad > 0.:
                    update = (s_grad - self.l1_reg) / (self.l2_reg + s_rate)
                else:
                    update = (s_grad + self.l1_reg) / (self.l2_reg + s_rate)
            self.W[j, i] = update

        return loss
