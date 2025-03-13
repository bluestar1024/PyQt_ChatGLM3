import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, QRect, QEasingCurve, QPropertyAnimation
from PyQt5.QtGui import QPainter, QBrush, QPen


class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.list_widget = QListWidget()
        self.text_edit = QTextEdit()
        self.button = QPushButton("Move B")

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)

        self.setFixedSize(400, 300)
        """ self.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 20px;") """

    def connectButtonClick(self, fun):
        self.button.clicked.connect(fun)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.gray, 2))
        painter.drawRoundedRect(self.rect(), 20, 20)


""" class SideWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 300)
        self.setStyleSheet("background-color: lightblue;")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground) """


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle("Animated Layout Example")

        self.a_widget = RoundedWidget(self)
        self.a_widget.connectButtonClick(self.on_button_clicked)
        self.b_widget = QWidget(self)
        self.b_widget.setFixedSize(100, 300)
        self.b_widget.setStyleSheet("background-color: pink;")

        self.b_widget.move(-100, 0)
        self.b_widget.raise_()

        """ self.a_widget.setParent(self)
        self.a_widget.move(0, 0) """

    def on_button_clicked(self):
        animation = QPropertyAnimation(self.b_widget, b"geometry")
        animation.setDuration(2000)
        """ animation.setEasingCurve(QEasingCurve.InOutQuad) """

        start_rect = QRect(-100, 0, 100, 300)
        end_rect = QRect(0, 0, 100, 300)

        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()

        # Adjust layout margins
        self.a_widget.layout.setContentsMargins(100, 0, 0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
