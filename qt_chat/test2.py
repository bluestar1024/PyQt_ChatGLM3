import sys, os
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout, QLineEdit, qApp, QSplitter
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen
from openai import OpenAI

class PushButton(QPushButton):
    def __init__(self, text, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        self.pushButtonList = []
        for i in range(5):
            self.pushButton = PushButton("第{}个按钮".format(i + 1), self)
            self.pushButton.setGeometry(87 * (i + 1) + 100 * i, 100, 100, 50)
            self.pushButton.clicked.connect(self.printButtonText)
            self.pushButtonList.append(self.pushButton)

    def printButtonText(self):
        pushButton = self.sender()
        for i in range(5):
            if pushButton == self.pushButtonList[i]:
                print(self.pushButtonList[i].text())
                self.changeButtonText(pushButton)

    def changeButtonText(self, btn):
        btn.setText('被点击了')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
