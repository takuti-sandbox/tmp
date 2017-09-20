"""http://pytorch.org/tutorials/beginner/nlp/deep_learning_tutorial.html
"""

import torch
import torch.autograd as autograd
import torch.nn as nn


torch.manual_seed(1)

lin = nn.Linear(5, 3)
data = autograd.Variable(torch.randn(2, 5))
print(data)  # X (2x5)
print(lin.weight)  # A (5x3)
print(lin.bias)  # b (3x1)
print(lin(data))  # AX + b (2x3)
