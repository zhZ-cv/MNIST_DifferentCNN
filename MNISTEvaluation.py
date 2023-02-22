# -*- codeing = utf-8 -*-
# @Time : 2023/2/10 11:22
# @Author : MOTR
# @File : ModelTrain.py
# @Software : PyCharm
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import wmi
from PIL import Image
import torch
import numpy as np
import time
from MyModel_0 import MyModel as myModel_0
from MyModel_1 import MyModel as myModel_1


class MyQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __int__(self):
        super().__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def connectEvent(self, func):
        self.clicked.connect(func)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 560)
        MainWindow.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonArea = QtWidgets.QWidget(self.centralwidget)
        self.buttonArea.setGeometry(QtCore.QRect(0, 70, 150, 330))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.buttonArea.setFont(font)
        self.buttonArea.setObjectName("buttonArea")
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.conCameraButton = QtWidgets.QPushButton(self.buttonArea)
        self.conCameraButton.setGeometry(QtCore.QRect(10, 160, 130, 50))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.conCameraButton.setFont(font)
        self.conCameraButton.setObjectName("conCameraButton")
        self.conCameraButton.clicked.connect(self.conCamera)
        self.evaluateButton = QtWidgets.QPushButton(self.buttonArea)
        self.evaluateButton.setGeometry(QtCore.QRect(10, 230, 130, 50))
        self.evaluateButton.setObjectName("evaluateButton")
        self.evaluateButton.clicked.connect(self.evaluate)
        self.loadIMGButton = QtWidgets.QPushButton(self.buttonArea)
        self.loadIMGButton.setGeometry(QtCore.QRect(10, 20, 130, 50))
        self.loadIMGButton.setObjectName("loadIMGButton")
        self.loadIMGButton.clicked.connect(self.loadIMG)
        self.deleteIMGButton = QtWidgets.QPushButton(self.buttonArea)
        self.deleteIMGButton.setGeometry(QtCore.QRect(10, 90, 130, 50))
        self.deleteIMGButton.setObjectName("deleteIMGButton")
        self.deleteIMGButton.clicked.connect(self.deleteIMG)
        self.ImgArea = MyQLabel(self.centralwidget)
        self.ImgArea.setGeometry(QtCore.QRect(500, 50, 280, 280))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(28)
        self.ImgArea.setFont(font)
        self.ImgArea.setObjectName("ImgArea")
        self.ImgArea.connectEvent(self.showIMG)
        self.InfoArea = QtWidgets.QWidget(self.centralwidget)
        self.InfoArea.setGeometry(QtCore.QRect(0, 410, 800, 120))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.InfoArea.setFont(font)
        self.InfoArea.setObjectName("InfoArea")
        self.CPUInfoLabel = QtWidgets.QLabel(self.InfoArea)
        self.CPUInfoLabel.setGeometry(QtCore.QRect(10, 0, 610, 120))
        self.CPUInfoLabel.setObjectName("CPUInfoLabel")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(310, 10, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(15)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.fileArea = QtWidgets.QTableWidget(self.centralwidget)
        self.fileArea.setGeometry(QtCore.QRect(160, 50, 320, 350))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fileArea.setFont(font)
        self.fileArea.setObjectName("fileArea")
        self.fileArea.setColumnCount(2)
        self.fileArea.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.fileArea.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.fileArea.setHorizontalHeaderItem(1, item)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        item.setFont(font)
        self.fileArea.setColumnWidth(0, 200)
        self.fileArea.setColumnWidth(1, 45)
        self.resultArea = QtWidgets.QWidget(self.centralwidget)
        self.resultArea.setGeometry(QtCore.QRect(500, 330, 280, 70))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.resultArea.setFont(font)
        self.resultArea.setObjectName("resultArea")
        self.resultLabel = QtWidgets.QLabel(self.resultArea)
        self.resultLabel.setGeometry(QtCore.QRect(40, 0, 200, 30))
        self.resultLabel.setObjectName("resultLabel")
        self.TimeLabel = QtWidgets.QLabel(self.resultArea)
        self.TimeLabel.setGeometry(QtCore.QRect(40, 30, 220, 30))
        self.TimeLabel.setObjectName("TimeLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowOpacity(0.9)
        self.isShow = False
        self.loadIMG()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MNIST图像识别"))
        self.conCameraButton.setText(_translate("MainWindow", "连接摄像"))
        self.evaluateButton.setText(_translate("MainWindow", "开始推理"))
        self.loadIMGButton.setText(_translate("MainWindow", "加载文件"))
        self.deleteIMGButton.setText(_translate("MainWindow", "删除图片"))
        self.ImgArea.setText(_translate("MainWindow", "点击预览图片"))
        cpuInfo = wmi.WMI()
        for cpu in cpuInfo.Win32_Processor():
            self.CPUInfoLabel.setText(_translate("MainWindow", f"CPU序列号:{cpu.ProcessorId.strip()}\nCPU名称:{cpu.Name}\nCPU核心数:{cpu.NumberOfCores}\nCPU时钟频率:{cpu.MaxClockSpeed}GHz"))
        self.titleLabel.setText(_translate("MainWindow", "MNIST图像识别"))
        item = self.fileArea.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "文件名"))
        item = self.fileArea.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "选择"))
        self.resultLabel.setText(_translate("MainWindow", "本次识别结果为："))
        self.TimeLabel.setText(_translate("MainWindow", "本次推理用时：-- μs"))

    def MessageBox(self, msg):
        QtWidgets.QMessageBox.information(self.centralwidget, '提示', msg)

    def getFileName(self, method=1):
        fileName = ""
        rowNum = self.fileArea.rowCount()
        for i in range(rowNum):
            state = self.fileArea.item(i, 1).checkState()
            if state:
                fileName = self.fileArea.item(i, 0).text().replace('.txt', '')
                if method == 1:
                    self.fileArea.item(i, 1).setCheckState(QtCore.Qt.Unchecked)
                break
            else:
                pass
        return fileName

    def showIMG(self):
        fileName = self.getFileName(0)
        if fileName:
            txtToIMG(fileName)
            pixmap = QtGui.QPixmap(f"mnist_data/{fileName}.jpg")
            self.ImgArea.setPixmap(pixmap)
            self.ImgArea.setScaledContents(True)
        else:
            self.MessageBox("未选中任何文件！")

    def loadIMG(self):
        fileList = os.listdir('mnist_data/')
        fileData = []
        for file in fileList:
            if ".txt" in file:
                fileData.append(file)
        loadThread = MyThread(self.fileArea, fileData)
        loadThread.run()
        if self.isShow:
            self.MessageBox("文件加载成功！")
        self.isShow = True

    def deleteIMG(self):
        rowNum = self.fileArea.rowCount()
        for i in range(rowNum):
            state = self.fileArea.item(i, 1).checkState()
            if state:
                fileName = self.fileArea.item(i, 0).text()
                os.remove(fileName)
            else:
                pass
        if self.isShow:
            self.MessageBox("选中文件已被删除！")
            self.isShow = False
            self.loadIMG()
        self.isShow = True

    def evaluate(self):
        fileName = self.getFileName(0)
        if fileName:
            img = Image.open(f"mnist_data/{fileName}.jpg")
            img = np.array(img).astype(np.float32)
            img = np.expand_dims(img, 0)
            img = np.expand_dims(img, 0)
            img = torch.from_numpy(img)
            img = img.to(torch.device("cuda:0"))
            beginTime = time.time()
            output = model(img)
            endTime = time.time()
            # prob = torch.nn.functional.softmax(output, dim=1)
            # prob = Variable(prob)
            # pred = np.argmax(prob)
            _, pred = torch.max(output.data, 1)
            print(pred)
            # exit()
            evaluationTime = int((endTime - beginTime) * 1000000)
            self.TimeLabel.setText(f"本次推理用时：{evaluationTime} μs")
            self.resultLabel.setText(f"本次识别结果为：{pred.item()}")
            self.MessageBox("本次推理完成！")
        else:
            self.MessageBox("未选中任何文件！")

    def conCamera(self):
        self.MessageBox("本功能期待后续开发！")

    def showResult(self, result):
        self.resultLabel.setText(f"本次识别结果为：{result}")

    def showTime(self, evaluateTime):
        self.TimeLabel.setText(f"本次推理用时：{evaluateTime} ms")


class MyThread(QtCore.QThread):

    def __init__(self, fileTable, Data):
        super(MyThread, self).__init__()
        self.fileTable = fileTable
        self.Data = Data

    def run(self):
        m = 0
        self.fileTable.setRowCount(len(self.Data))
        for i in self.Data:
            fileName = QtWidgets.QTableWidgetItem(i)
            self.check = QtWidgets.QTableWidgetItem()
            self.check.setCheckState(QtCore.Qt.Unchecked)
            self.fileTable.setItem(m, 0, fileName)
            self.fileTable.setItem(m, 1, self.check)
            m += 1


def txtToIMG(fileName):
    if not os.path.exists(f"mnist_data/{fileName}.jpg"):
        RGBs = []
        with open(f"mnist_data/{fileName}.txt", "r", encoding="utf-8") as imgFile:
            RGBData = imgFile.readlines()
            for data in RGBData:
                data = data.replace('\n', '')
                RGBNum = 0
                i = 128
                for j in data:
                    if j == '1':
                        RGBNum += i
                    i /= 2
                RGBs.append(RGBNum)
            imgFile.close()
        im = Image.new('L', (28, 28), 0)
        im.putdata(RGBs)
        im.save(f"mnist_data/{fileName}.jpg")


if __name__ == '__main__':
    # model_0
    model = myModel_0()
    parametersDict = torch.load("mnist_0.9843_MyModel_0.pth")
    model.load_state_dict(parametersDict)
    # model_1
    # model = myModel_1()
    # parametersDict = torch.load("mnist_0.9885_MyModel_1.pth")
    # model.load_state_dict(parametersDict)
    model.eval()
    app = QtWidgets.QApplication(sys.argv)
    Main_Window = Ui_MainWindow()
    Main_Window.show()
    sys.exit(app.exec())
