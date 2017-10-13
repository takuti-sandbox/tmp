import numpy as np
import torch


class MatrixFactorization(torch.nn.Module):

    def __init__(self, n_user, n_item, k=20):
        super().__init__()

        self.user_factors = torch.nn.Embedding(n_user, k, sparse=True)
        self.item_factors = torch.nn.Embedding(n_item, k, sparse=True)

    def forward(self, user, item):
        return (self.user_factors(user) * self.item_factors(item)).sum(1)


def main():
    # 5 users * 6 items
    R = np.array([[5, 0, 1, 1, 0, 2],
                  [0, 2, 0, 4, 0, 4],
                  [4, 5, 0, 1, 1, 2],
                  [0, 0, 3, 5, 2, 0],
                  [2, 0, 1, 0, 4, 4]])
    n_user, n_item = R.shape

    model = MatrixFactorization(n_user, n_item)
    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-6)

    for each in range(3):
        for user in range(n_user):
            for item in range(n_item):
                if R[user, item] == 0.:
                    continue

                model.zero_grad()

                user_variable = torch.autograd.Variable(torch.LongTensor([np.long(user)]))
                item_variable = torch.autograd.Variable(torch.LongTensor([np.long(item)]))
                rating = torch.autograd.Variable(torch.FloatTensor([np.float(R[user, item])]))

                prediction = model(user_variable, item_variable)

                loss = loss_function(prediction, rating)

                loss.backward()

                optimizer.step()

    for user in range(n_user):
        for item in range(n_item):
            if R[user, item] == 0.:
                continue

            user_variable = torch.autograd.Variable(torch.LongTensor([np.long(user)]))
            item_variable = torch.autograd.Variable(torch.LongTensor([np.long(item)]))

            prediction = model(user_variable, item_variable)
            print(user, item, R[user, item], prediction)


if __name__ == '__main__':
    main()
