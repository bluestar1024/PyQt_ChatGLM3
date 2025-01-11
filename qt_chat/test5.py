import sys, os
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout, QLineEdit, qApp, QSplitter, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(10, 250, 10))
        #Pen
        pen = QPen()
        pen.setColor(Qt.blue)
        pen.setWidth(10)
        #QPainter setting
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainHLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainHLayout)
        self.subWidget = QWidget()
        self.mainHLayout.addWidget(self.subWidget)
        self.subWidget.setStyleSheet('''
        QWidget{
            background-color: rgba(200, 200, 200, 100%);
        }
        ''')
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, 0)
        self.effect.setColor(Qt.blue)
        self.effect.setBlurRadius(20)
        self.subWidget.setGraphicsEffect(self.effect)

        self.subVLayout = QVBoxLayout()
        self.subWidget.setLayout(self.subVLayout)
        self.subVLayout.addWidget(QPushButton('按钮一'))
        self.subVLayout.addWidget(QPushButton('按钮二'))
        self.subVLayout.addWidget(QPushButton('按钮三'))
        self.subVLayout.addWidget(QLabel('标签一'))
        '''self.effect2 = QGraphicsDropShadowEffect()
        self.effect2.setOffset(-10, -10)
        self.effect2.setColor(Qt.blue)
        self.effect2.setBlurRadius(10)
        self.subWidget.setGraphicsEffect(self.effect2)'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
