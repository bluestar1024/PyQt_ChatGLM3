import sys, os
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout, QLineEdit, qApp, QSplitter
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen
from openai import OpenAI

class TextLabel(QLabel):
    textSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TextLabel, self).__init__(parent)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def mouseReleaseEvent(self, event):
        QLabel.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            if self.hasSelectedText():
                self.textSelected.emit(self.selectedText())

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        self.clip = QApplication.clipboard()
        self.label = TextLabel(self)
        self.label.setText('老猫最帅')
        self.label.setGeometry(100, 100, 100, 50)
        self.label.textSelected.connect(self.printText)

    def printText(self, text):
        print(text)
        self.clip.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
