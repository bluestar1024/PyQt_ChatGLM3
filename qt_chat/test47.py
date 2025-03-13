import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt


class ParentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 父窗口设置
        self.setWindowTitle("Parent Widget")
        self.resize(400, 300)
        self.setObjectName('parent')
        self.setStyleSheet("#parent { border-bottom-left-radius: 20px; background-color: lightblue; }")

        # 子窗口设置
        self.child_widget = QWidget(self)
        self.child_widget.resize(100, 100)
        self.child_widget.setStyleSheet("background-color: pink; border: 1px solid black;")

        # 初始化子窗口位置（在父窗口左侧外部，与父窗口底部对齐）
        self.child_widget.move(-100, 200)

        # 创建按钮
        self.button = QPushButton("Start Animation", self)
        self.button.clicked.connect(self.start_animation)
        self.button.resize(150, 30)
        self.button.move(125, 250)  # 按钮位置
        self.button.setStyleSheet("background-color: pink;")

        # 创建动画
        self.animation = QPropertyAnimation(self.child_widget, b"geometry")
        self.animation.setDuration(2000)  # 动画时长为2秒

    def start_animation(self):
        """ # 起始位置：子窗口在父窗口左侧外部，与父窗口底部对齐
        start_x = -self.child_widget.width()
        start_y = self.height() - self.child_widget.height()

        # 结束位置：子窗口移动到父窗口内部，经过左下角
        end_x = self.width() - self.child_widget.width()
        end_y = self.height() - self.child_widget.height() """

        self.animation.setStartValue(QRect(-100, 200, 100, 100))
        self.animation.setEndValue(QRect(300, 200, 100, 100))
        self.animation.start()


class ChildWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        """ self.initUI()

    def initUI(self):
        # 子窗口样式
        self.setStyleSheet("background-color: pink; border: 1px solid black;") """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    parent_widget = ParentWidget()
    parent_widget.show()
    sys.exit(app.exec_())
