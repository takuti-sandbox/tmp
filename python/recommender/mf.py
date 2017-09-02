import numpy as np

# 5 users * 6 items
R = np.array([[5, 0, 1, 1, 0, 2],
              [0, 2, 0, 4, 0, 4],
              [4, 5, 0, 1, 1, 2],
              [0, 0, 3, 5, 2, 0],
              [2, 0, 1, 0, 4, 4]])
n_user, n_item = R.shape

# represent user/item characteristics in a lower dimensional space
k = 2

P = np.random.rand(n_user, k)
Q = np.random.rand(n_item, k)

last_accum_err = float('inf')

while True:
    accum_err = 0

    for user in range(n_user):
        for item in range(n_item):
            if R[user, item] == 0:
                continue

            p, q = P[user], Q[item]

            err = R[user, item] - np.inner(p, q)
            accum_err += err

            next_p = p - 0.1 * (-2. * (err * q - 0.01 * p))
            next_q = q - 0.1 * (-2. * (err * p - 0.01 * q))

            P[user], Q[user] = next_p, next_q

    if abs(accum_err - last_accum_err) < 1e-3:
        break
    last_accum_err = accum_err

print(np.dot(P, Q.T))
# [[ 1.44089222  2.10861345  1.35586737  1.30939713  2.25707035  1.10801462]
#  [ 1.93053648  3.03696723  1.89003927  1.94703341  3.2410682   1.5074436 ]
#  [ 1.93037675  3.08600948  1.90697021  1.99171424  3.2913027   1.51264917]
#  [ 1.95476578  3.09267286  1.91985778  1.98747126  3.29976689  1.52826493]
#  [ 2.27963689  3.58058058  2.22988788  2.29405565  3.82145282  1.77943416]]
