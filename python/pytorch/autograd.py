import torch
from torch.autograd import Variable


def tutorial():
    """http://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html
    """

    # [x1, x2; x3, x4] = [1, 1; 1, 1]
    x = Variable(torch.ones(2, 2), requires_grad=True)

    # [y1, y2; y3, y4] = [x+2, x+2; x+2, x+2]
    y = x + 2

    # zi = 3 * (xi + 2)^2
    z = y * y * 3

    # out = 1/4 * (z1 + z2 + z3 + z4)
    #     = 1/4 * (3 * (x1 + 2)^2 + 3 * (x2 + 2)^2 + 3 * (x3 + 2)^2 + 3 * (x4 + 2)^2)
    out = z.mean()

    # d(out)
    out.backward()

    # d(out) / d(xi) = 1/4 * 2 * 3 * (xi + 2) = 3/2 * (xi + 2) = 4.5 (because xi = 1)
    print(x.grad)


def single_x():
    # x = 1
    x = Variable(torch.ones(1), requires_grad=True)

    # y = x + 2
    y = x + 2

    # z = 3 * (x + 2)^2
    z = y * y * 3

    # out = 1/1 * z = z = 3 * (x + 2)^2
    out = z.mean()

    # d(out)
    out.backward()

    # d(out)/dx = 6 * (x + 2) = 18 (because x = 1)
    print(x.grad)


if __name__ == '__main__':
    single_x()
