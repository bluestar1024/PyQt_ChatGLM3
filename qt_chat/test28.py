import sys, os
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QAbstractSpinBox, QGridLayout, QLineEdit, QSplitter, QToolTip, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve, QEvent, QPoint, pyqtProperty, QTimer, QUrl
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen, QCursor, QFontDatabase, QTextDocument, QTextOption
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__() 
        self.webEngineView = QWebEngineView(self)
        self.webEngineView.setUrl(QUrl("http://www.baidu.com"))

        self.webEngineView.page().loadFinished.connect(self.setSize)

        self.webEngineView.resize(800, 400)
        self.resize(800, 400)

        # 将网页内容放大到200%
        #view.setZoomFactor(2.0)

        # 或者将网页内容缩小到50%
        #self.webEngineView.setZoomFactor(0.5)

    def adjustWidth(self, width):
        #self.webEngineView.resize(width, self.webEngineView.height())
        if width:
            print('w_width:', width)
            print('w_height:', self.webEngineView.height())
            print('p_width:', self.webEngineView.page().contentsSize().toSize().width())
            print('p_height:', self.webEngineView.page().contentsSize().toSize().height())
            self.webEngineView.resize(width, self.webEngineView.height())
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            print('view_width:', width)
            print('view_height:', self.webEngineView.height())
            print('p_width:', self.webEngineView.page().contentsSize().toSize().width())
            print('p_height:', self.webEngineView.page().contentsSize().toSize().height())
            '''pageWidth = width
            print('pageWidth', pageWidth)
            viewWidth = self.webEngineView.width()
            print('viewWidth', viewWidth)
            self.zoomFactorWidth = viewWidth / pageWidth
            print('zoomFactorWidth', self.zoomFactorWidth)'''

    def adjustHeight(self, height):
        #self.webEngineView.resize(self.webEngineView.height(), height)
        if height:
            print('h_width:', self.webEngineView.width())
            print('h_height:', height)
            print('p_width:', self.webEngineView.page().contentsSize().toSize().width())
            print('p_height:', self.webEngineView.page().contentsSize().toSize().height())
            self.webEngineView.resize(self.webEngineView.width(), height)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            print('view_width:', self.webEngineView.width())
            print('view_height:', height)
            print('p_width:', self.webEngineView.page().contentsSize().toSize().width())
            print('p_height:', self.webEngineView.page().contentsSize().toSize().height())

    def setSize(self, success):
        if success:
            print('setSize')
            """ QTimer.singleShot(100, lambda: self.webEngineView.page().runJavaScript("document.body.scrollWidth", self.adjustWidth))
            QTimer.singleShot(100, lambda: self.webEngineView.page().runJavaScript("document.body.scrollHeight", self.adjustHeight)) """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
