# -*- codeing = utf-8 -*-
# @Time : 2023/2/20 10:52
# @Author : MOTR
# @File : QATModel.py
# @Software : PyCharm
import torch


def ToComplementForm(num):
    addCode = ''
    if num < 0:
        num = 128 + num
        addCode += '1'
    trueForm_0 = bin(num)
    trueForm_1 = trueForm_0.replace('0b', '')
    trueForm_0 = trueForm_1.replace('-', '')
    while len(addCode) + len(trueForm_0) < 8:
        addCode += '0'
    complementForm = addCode + trueForm_0 + '\n'
    return complementForm


# write parameters to txt in the form of eight-bit complement
def writeToFile(dataList, floorName, num1, num2, num3=None):
    path = 'new_parameters_10channel/'
    if num3:
        for i in range(num1):
            for j in range(num3):
                fileName = path + f'{floorName}_{i}_{j}.txt'
                f = open(fileName, 'w+', encoding='utf-8')
                m = (i * num3 + j) * num2
                for k in range(num2):
                    data = dataList[m + k]
                    data1 = ToComplementForm(data)
                    f.write(data1)
                f.close()
    else:
        for i in range(num1):
            fileName = path + f'{floorName}_{i}.txt'
            f = open(fileName, 'w+', encoding='utf-8')
            m = i * num2
            for j in range(num2):
                data = dataList[m + j]
                data1 = ToComplementForm(data)
                f.write(data1)
            f.close()


# transform weight and bias from float to int8
def floatToInt(numList):
    newList =[]
    for num in numList:
        if num >= 1:
            newNum = 127
        elif num <= -1:
            newNum = -128
        else:
            newNum = int(num * 128)
        newList.append(newNum)
    return newList


# examine the parameters' shape
def examineTheShape():
    print(parametersDict['conv1.weight'].shape)
    print(parametersDict['conv2.weight'].shape)
    print(parametersDict['fc1.weight'].shape)
    print(parametersDict['conv1.bias'].shape)
    print(parametersDict['conv2.bias'].shape)
    print(parametersDict['fc1.bias'].shape)


def quantizationModel():
    parametersDict['conv1.weight'] = torch.IntTensor(floatToInt(conv1_weight)).view(3, 1, 3, 3)
    parametersDict['conv2.weight'] = torch.IntTensor(floatToInt(conv2_weight)).view(6, 3, 3, 3)
    parametersDict['fc1.weight'] = torch.IntTensor(floatToInt(fc1_weight)).view(10, 150)
    parametersDict['conv1.bias'] = torch.IntTensor(floatToInt(b1))
    parametersDict['conv2.bias'] = torch.IntTensor(floatToInt(b2))
    parametersDict['fc1.bias'] = torch.IntTensor(floatToInt(b3))
    torch.save(parametersDict, f'mnist_int8_{fileName}')


def writeToTXT():
    writeToFile(conv1_weight, 'W_CONV1', 3, 9)
    writeToFile(conv2_weight, 'W_CONV2', 6, 9, 3)
    writeToFile(fc1_weight, 'W_FC1', 10, 150)
    writeToFile(b1, 'B_CONV1', 1, 3)
    writeToFile(b2, 'B_CONV2', 1, 6)
    writeToFile(b3, 'B_FC1', 1, 10)


if __name__ == '__main__':
    fileName = '0.9843_MyModel_0.pth'
    parametersDict = torch.load(f'mnist_{fileName}')
    conv1_weight = parametersDict['conv1.weight'].view(-1).tolist()
    conv2_weight = parametersDict['conv2.weight'].view(-1).tolist()
    fc1_weight = parametersDict['fc1.weight'].view(-1).tolist()
    b1 = parametersDict['conv1.bias'].tolist()
    b2 = parametersDict['conv2.bias'].tolist()
    b3 = parametersDict['fc1.bias'].tolist()

