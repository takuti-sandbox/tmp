"""http://pytorch.org/tutorials/beginner/nlp/deep_learning_tutorial.html
"""

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(1)


def affine_map():
    lin = nn.Linear(5, 3)
    data = autograd.Variable(torch.randn(2, 5))
    print(data)  # X (2x5)
    # `lin.weight`: A (5x3)
    # `lin.bias`: b (3x1)
    print(lin(data))  # AX + b (2x3)


def relu():
    data = autograd.Variable(torch.randn(2, 2))
    print(data)
    print(F.relu(data))  # max(0, x)


if __name__ == '__main__':
    print('Affine map')
    affine_map()

    print('ReLU')
    relu()
