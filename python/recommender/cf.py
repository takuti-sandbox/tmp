import numpy as np
import numpy.linalg as ln


def similarity(x, y):
    return np.inner(x, y) / (ln.norm(x, ord=2) * ln.norm(y, ord=2))


# 5 users * 6 items
A = np.array([[5, 0, 1, 1, 0, 2],
              [0, 2, 0, 4, 0, 4],
              [4, 5, 0, 1, 1, 2],
              [0, 0, 3, 5, 2, 0],
              [2, 0, 1, 0, 4, 4]])

# user-user similarity matrix
n_user = A.shape[0]
S = np.zeros((n_user, n_user))

for i in range(n_user):
    S[i, i] = 1.
    for j in range(i + 1, n_user):
        S[i, j] = S[j, i] = similarity(A[i], A[j])

print(S)
