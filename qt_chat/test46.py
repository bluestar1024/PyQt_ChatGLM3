import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class CustomTitleBar(QWidget):
    """自定义标题栏"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.closeButton = QPushButton("X", self)
        self.closeButton.clicked.connect(self.parent.close)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 180);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QPushButton {
                border: none;
                font-size: 16px;
                background: rgba(255, 0, 0, 180);
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 255);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.mPos = event.globalPos() - self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.parent.mPos:
            self.parent.move(event.globalPos() - self.parent.mPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.parent.mPos = None
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mPos = None
        self.initUI()

    def initUI(self):
        # 设置窗口透明化和无边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 创建自定义标题栏
        self.titleBar = CustomTitleBar(self)
        self.titleBar.setParent(self)

        # 创建主内容区域
        self.mainFrame = QFrame(self)
        self.mainFrame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 255);
                border-radius: 10px;
                border: 1px solid lightgray;
            }
        """)

        # 布局设置
        layout = QVBoxLayout(self)
        layout.addWidget(self.titleBar)
        layout.addWidget(self.mainFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def paintEvent(self, event):
        """绘制圆角矩形窗口"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 255, 255, 255)))
        painter.drawRoundedRect(self.rect(), 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.titleBar.geometry().contains(event.pos()):
            self.mPos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.move(event.globalPos() - self.mPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mPos = None
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())
