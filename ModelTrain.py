# -*- codeing = utf-8 -*-
# @Time : 2023/2/13 15:20
# @Author : MOTR
# @File : ModelTrain.py
# @Software : PyCharm
import torch
from torchvision.datasets import mnist
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
import os

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class modelTrain:
    def __init__(self, model, modelName, batch_size=256, MaxAcc=0, deleteLowAcc=True):
        self.model = model
        self.modelName = modelName
        self.model.to(device)
        self.batch_size = batch_size
        self.MaxAcc = MaxAcc
        self.deleteLowAcc = deleteLowAcc

    def train(self, epoch):
        train_loader = DataLoader(mnist.MNIST(root='./train', train=True, transform=ToTensor()), batch_size=self.batch_size)
        loss_fn = CrossEntropyLoss()
        sgd = SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        for current_epoch in range(epoch):
            print(f'======== current_epoch: {current_epoch} ========')
            self.model.train()
            for idx, (train_x, train_label) in enumerate(train_loader):
                sgd.zero_grad()
                train_x = train_x.to(device)
                train_label = train_label.to(device)
                predict_y = self.model(train_x.float())
                loss = loss_fn(predict_y, train_label.long())
                if idx % int(60000/self.batch_size/4) == 0:
                    print('idx: {}, loss: {}'.format(idx, loss.sum().item()))
                loss.backward()
                sgd.step()
            self.test()

    def test(self):
        test_loader = DataLoader(mnist.MNIST(root='./test', train=False, transform=ToTensor()), batch_size=self.batch_size)
        correct_num = 0
        self.model.eval()
        for idx, (test_x, test_label) in enumerate(test_loader):
            test_x = test_x.to(device)
            test_label = test_label.to(device)
            predict_y = self.model(test_x.float())
            _, predict_y = torch.max(predict_y.data, 1)
            correct_num += (predict_y == test_label).sum().item()
        accuracy = correct_num / 10000
        if accuracy > self.MaxAcc:
            try:
                os.remove(f'mnist_{self.MaxAcc}_{self.modelName}.pth')
            except:
                pass
            # torch.save(self.model.state_dict(), f'mnist_{accuracy}_{self.modelName}.pth')
            self.MaxAcc = accuracy
        print(f'accuracy: {accuracy}')
