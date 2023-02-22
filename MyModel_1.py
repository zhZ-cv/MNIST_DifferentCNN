# -*- codeing = utf-8 -*-
# @Time : 2023/2/21 18:27
# @Author : MOTR
# @File : MyModel_1.py
# @Software : PyCharm
from ModelTrain import modelTrain
from torch.nn import Module
from torch import nn, load


class MyModel(Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 5, (5, 5))
        self.conv2 = nn.Conv2d(5, 10, (5, 5))
        self.fc1 = nn.Linear(160, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)

    def forward(self, x):
        y = self.pool(self.relu(self.conv1(x)))
        y = self.pool(self.relu(self.conv2(y)))
        y = y.view(y.shape[0], -1)
        y = self.relu(self.fc1(y))
        return y


if __name__ == '__main__':
    model = MyModel()
    # continue the training
    # parametersDict = load('mnist_0.9885_MyModel_1.pth')
    # model.load_state_dict(parametersDict)
    modelTrain = modelTrain(model, 'MyModel_1', 128)
    modelTrain.train(100)
