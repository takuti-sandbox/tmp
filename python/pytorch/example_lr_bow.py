"""Logistinc regiression BoW language classifier

http://pytorch.org/tutorials/beginner/nlp/deep_learning_tutorial.html#example-logistic-regression-bag-of-words-classifier
"""

import torch
from torch import autograd, nn, optim
from torch.nn import functional as F

train = [("me gusta comer en la cafeteria".split(), "SPANISH"),
         ("Give it to me".split(), "ENGLISH"),
         ("No creo que sea una buena idea".split(), "SPANISH"),
         ("No it is not a good idea to get lost at sea".split(), "ENGLISH")]

test = [("Yo creo que si".split(), "SPANISH"),
        ("it is lost on me".split(), "ENGLISH")]

word_to_index = dict()
for sentence, _ in train + test:
    for word in sentence:
        if word not in word_to_index:
            word_to_index[word] = len(word_to_index)

label_to_index = {'SPANISH': 0, 'ENGLISH': 1}

VOCAB_SIZE = len(word_to_index)
NUM_LABELS = len(label_to_index)


class BoWClassifier(nn.Module):

    def __init__(self, num_labels, vocab_size):
        super(BoWClassifier, self).__init__()

        # model parameter = affine map (A, b) which projects BoW to label probabilities
        self.linear = nn.Linear(vocab_size, num_labels)

    def forward(self, bow_vec):
        # log Softmax(Ax + b)
        return F.log_softmax(self.linear(bow_vec))


def make_bow_vector(sentence, word_to_index):
    vec = torch.zeros(len(word_to_index))
    for word in sentence:
        vec[word_to_index[word]] += 1
    return vec.view(1, -1)  # 1 x len(word_to_index)


def make_target(label, label_to_index):
    return torch.LongTensor([label_to_index[label]])


model = BoWClassifier(NUM_LABELS, VOCAB_SIZE)

# show parameters which have been initialized in `BoWClassifier.__init__`
# for param in model.parameters():
#    print(param)

# see log probs before training
for sentence, label in test:
    bow_vec = autograd.Variable(make_bow_vector(sentence, word_to_index))
    log_probs = model(bow_vec)
    print(log_probs)

# negative log likelihood loss
# input will be a pair of log probs computed by model and expected label
loss_function = nn.NLLLoss()

# SGD optimizer for the affine map parameters
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(100):
    for sentence, label in train:
        # clear accumulated gradients
        model.zero_grad()

        bow_vec = autograd.Variable(make_bow_vector(sentence, word_to_index))
        target = autograd.Variable(make_target(label, label_to_index))

        # run forward pass; that is, compute affine map and pass through log softmax
        log_probs = model(bow_vec)

        loss = loss_function(log_probs, target)
        loss.backward()  # gradient of loss
        optimizer.step()  # update model parameters

for sentence, label in test:
    bow_vec = autograd.Variable(make_bow_vector(sentence, word_to_index))
    log_probs = model(bow_vec)
    print(log_probs)
