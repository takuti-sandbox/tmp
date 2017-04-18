import numpy as np


"""ref: https://satomacoto.blogspot.jp/2009/10/pythonplsa.html
"""


class PLSA:

    def __init__(self, D, K):
        self.D = D
        self.K = K

        self.n_doc, self.n_word = D.shape

        self.normalize = lambda ary: (ary / np.sum(ary))

        self.Pdwz = np.random.random((self.n_doc, self.n_word, self.K))  # P(z|d,w)
        self.Pzw = np.random.random((self.K, self.n_word))  # P(w|z)
        self.Pzd = np.random.random((self.K, self.n_doc))  # P(d|z)
        self.Pz = self.normalize(np.random.random(self.K))  # P(z)

    def train(self, n_iter=1000, eps=1e-5):
        prevL = float('-inf')
        for it in range(n_iter):
            self.e_step()
            self.m_step()

            L = self.loglikelihood()
            perp = self.perplexity()
            print('Iter %d: log-likelihood = %f, perplexity = %f' % (it + 1, L, perp))
            print(self.Pzw)
            if abs(L - prevL) < eps:
                break
            prevL = L

    def e_step(self):
        for d in range(self.n_doc):
            for w in range(self.n_word):
                for z in range(self.K):
                    self.Pdwz[d, w, z] = self.Pz[z] * self.Pzd[z, d] * self.Pzw[z, w]
                self.Pdwz[d, w] = self.normalize(self.Pdwz[d, w])

    def m_step(self):
        for z in range(self.K):
            # update P(w|z)
            for w in range(self.n_word):
                self.Pzw[z, w] = 0.
                for d in range(self.n_doc):
                    self.Pzw[z, w] += (self.D[d, w] * self.Pdwz[d, w, z])
            self.Pzw[z] = self.normalize(self.Pzw[z])

            # update P(d|z)
            for d in range(self.n_doc):
                self.Pzd[z, d] = 0.
                for w in range(self.n_word):
                    self.Pzd[z, d] += (self.D[d, w] * self.Pdwz[d, w, z])
            self.Pzd[z] = self.normalize(self.Pzd[z])

            # update P(z)
            self.Pz[z] = 0.
            for d in range(self.n_doc):
                for w in range(self.n_word):
                    self.Pz[z] += (self.D[d, w] * self.Pdwz[d, w, z])
            self.Pz = self.normalize(self.Pz)

    def loglikelihood(self):
        L = 0.

        for d in range(self.n_doc):
            for w in range(self.n_word):
                # comput P(d, w) = \Sigma_z P(z) P(w|z) P(d|z)
                Pdw = 0.
                for z in range(self.K):
                    Pdw += (self.Pz[z] * self.Pzw[z, w] * self.Pzd[z, d])

                # L = \Sigma_d \Sigma_z n(d,w) * log(P(d,w))
                L += (self.D[d, w] * np.log(Pdw))

        return L

    def perplexity(self):
        numer = 0.
        denom = 0.

        for d in range(self.n_doc):
            for w in range(self.n_word):
                Pdw = 0.
                for z in range(self.K):
                    Pdw += self.Pzw[z, w] * self.Pz[z]
                numer += (self.D[d, w] * np.log(Pdw))
                denom += self.D[d, w]

        return np.exp(-1. * numer / denom)


def main():
    D = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 1, 2, 1]])
    p = PLSA(D, 2)
    p.train()
    print(p.Pz)
    print(p.Pzd)
    print(p.Pzw)
    print(p.Pdwz)


if __name__ == '__main__':
    main()
