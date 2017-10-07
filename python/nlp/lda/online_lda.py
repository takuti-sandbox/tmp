import numpy as np
from scipy.special import psi


def dirichlet_expectation_1d(arr):
    return psi(arr) - psi(np.sum(arr))


def dirichlet_expectation_2d(arr):
    """E[log(theta)] for theta ~ Dir(arr).

    For the digamma function `psi`:

    ---

    n_rows = arr.shape[0]
    n_cols = arr.shape[1]

    d_exp = np.empty_like(arr)
    for i in range(n_rows):
        row_total = 0
        for j in range(n_cols):
            row_total += arr[i, j]
        psi_row_total = psi(row_total)

        for j in range(n_cols):
            d_exp[i, j] = psi(arr[i, j]) - psi_row_total

    return d_exp
    """
    return psi(arr) - psi(np.sum(arr, 1))[:, np.newaxis]


class OnlineLDA:

    def __init__(self, tau0=1024, kappa=.7, n_topics=10, batch_size=1):
        self.total_samples = 0
        self.n_topics = n_topics
        self.batch_size = batch_size

        self.tau0 = tau0 + 1
        self.kappa = kappa
        self.update_count = 0

    def partial_fit(self, X):
        """
        Args:
            X (numpy 2d array): document-word matrix.
        """

        # check whether all elements in X are non-negative
        assert np.where(X < 0.)[0].size == 0, 'X should be a non-negative matrix.'

        n_samples, n_features = X.shape

        # for initial partial fitting, initialize the parameters
        if not hasattr(self, 'lambda_'):
            self.__init_latent_vars(n_features)

        for head in range(0, n_samples, self.batch_size):
            self.total_samples += self.batch_size
            tail = head + self.batch_size
            self.__train_em(X[head:tail, :])

    def __init_latent_vars(self, n_features):
        # initialize w/ uniform
        self.topic_word_prior = 1 / self.n_topics
        self.lambda_ = np.random.gamma(100, 1 / 100, (self.n_topics, n_features))
        self.exp_E_log_beta = dirichlet_expectation_2d(self.lambda_)

    def __train_em(self, X):
        _, suff_stats = self.__e_step(X)
        self.__m_step(X, suff_stats)

    def __e_step(self, X):
        n_samples, n_features = X.shape

        # initialize the variational distribution q(theta|gamma) for this mini-batch
        gamma_ = np.random.gamma(100, 1 / 100, (n_samples, self.n_topics))

        # exp(E[log(theta)])
        exp_E_log_theta = np.exp(dirichlet_expectation_2d(gamma_))

        # sufficient statistics
        suff_stats = np.zeros(self.lambda_.shape)

        for d in range(n_samples):
            ids = np.nonzero(X[d, :])[0]
            counts = X[d, ids]  # word counts in a document

            gammad = gamma_[d, :]
            exp_E_log_theta_d = exp_E_log_theta[d, :]
            exp_E_log_beta_d = self.exp_E_log_beta[:, ids]

            # The optimal phi_{dwk} is proportional to
            # expElogthetad_k * expElogbetad_w. phinorm is the normalizer.
            # phinorm is size of second dimension of expElogbetad
            # (number of words in the batch)
            phi_norm = np.dot(exp_E_log_theta_d, exp_E_log_beta_d) + 1e-100

            for it in range(10):
                last_gammad = gammad.copy()

                gammad = exp_E_log_theta_d * np.dot(counts / phi_norm, exp_E_log_beta_d.T)
                exp_E_log_theta_d = np.exp(dirichlet_expectation_1d(gammad))
                phi_norm = np.dot(exp_E_log_theta_d, exp_E_log_beta_d) + 1e-100

                # if gamma hasn't changed so much
                mean_change = np.mean(abs(gammad - last_gammad))
                if mean_change < 0.001:
                    break

            # update
            gamma_[d, :] = gammad

            suff_stats[:, ids] += np.outer(exp_E_log_theta_d, counts / phi_norm)

        suff_stats *= self.exp_E_log_beta

        return gamma_, suff_stats

    def __m_step(self, X, suff_stats):
        rho = np.power(self.tau0 + self.update_count, -self.kappa)

        doc_ratio = self.total_samples / X.shape[0]

        self.lambda_ *= (1 - rho)
        self.lambda_ += (rho * (self.topic_word_prior + doc_ratio * suff_stats))

        self.exp_E_log_beta = np.exp(dirichlet_expectation_2d(self.lambda_))
        self.update_count += 1
