import numpy as np
import numpy.linalg as ln


def similarity(x, y):
    return np.inner(x, y) / (ln.norm(x, ord=2) * ln.norm(y, ord=2))


user_a = np.array([5, 0, 1, 1, 0, 2])
user_b = np.array([0, 2, 0, 4, 0, 4])
user_c = np.array([4, 5, 0, 1, 1, 2])

print(similarity(user_a, user_b))  # 0.359210604054
print(similarity(user_a, user_c))  # 0.654953146328
