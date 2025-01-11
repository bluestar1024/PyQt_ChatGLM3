import sys, os
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout, QLineEdit, qApp, QSplitter
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen
from openai import OpenAI

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        #self.centralWidget = QWidget()
        #self.setCentralWidget(self.centralWidget)
        #self.mainVLayout = QVBoxLayout()
        #self.centralWidget.setLayout(self.mainVLayout)
        self.splitter = QSplitter(Qt.Vertical, self)
        self.splitter.setFixedSize(800, 500)
        self.splitter.setChildrenCollapsible(False)
        self.label = QLabel('老猫最帅')
        self.label.setMinimumSize(200, 100)
        self.label.resize(800, 200)
        #self.label.setFixedSize(800, 200)
        self.textEdit = QTextEdit()
        self.textEdit.setMinimumSize(200, 100)
        self.textEdit.resize(800, 300)
        #self.textEdit.setFixedSize(800, 300)
        #self.textEdit.move(100, 200)
        self.splitter.addWidget(self.label)
        self.splitter.addWidget(self.textEdit)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
