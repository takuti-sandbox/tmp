"""http://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html
"""

import torch
from torch.autograd import Variable


x = Variable(torch.ones(2, 2), requires_grad=True)
y = x + 2

z = y * y * 3  # 3 * (x + 2)^2
out = z.mean()  # single from 3 * (1 + 2)^2

out.backward()

print(x.grad)
