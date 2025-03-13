import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        # 设置A窗口为圆角矩形
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)

        # 设置A窗口的布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 左侧边距为0

        # 添加QListWidget、QTextEdit和QPushButton
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: lightblue;")
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("background-color: lightgreen;")
        self.button = QPushButton("Toggle Sidebar")
        self.button.setStyleSheet("background-color: pink;")

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)

        # 创建B部件
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: lightgray;")
        self.sidebar.setFixedWidth(100)  # 设置B部件的宽度
        self.sidebar.setFixedHeight(self.height())  # 设置B部件的高度与A窗口相同

        # 初始位置：B部件在A窗口左侧外面
        self.sidebar.move(-self.sidebar.width(), 0)

        # 设置按钮点击事件
        self.button.clicked.connect(self.toggle_sidebar)

        # 动画对象
        self.animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.animation.setDuration(5000)  # 动画时长300ms
        self.animation.setEasingCurve(QEasingCurve.OutQuad)  # 设置动画曲线
        self.animation.valueChanged.connect(self.animationMove)

        self.sidebar_visible = False

    def toggle_sidebar(self):
        if self.sidebar_visible:
            # 隐藏B部件
            self.animation.setStartValue(self.sidebar.geometry())
            self.animation.setEndValue(QRect(-self.sidebar.width(), 0, self.sidebar.width(), self.sidebar.height()))
            self.layout.setContentsMargins(0, 0, 0, 0)  # 恢复左侧边距为0
        else:
            # 显示B部件
            self.animation.setStartValue(self.sidebar.geometry())
            self.animation.setEndValue(QRect(0, 0, self.sidebar.width(), self.sidebar.height()))
            self.layout.setContentsMargins(self.sidebar.width(), 0, 0, 0)  # 设置左侧边距为B部件的宽度

        self.animation.start()
        self.sidebar_visible = not self.sidebar_visible

    def animationMove(self, rect):
        self.list_widget.resize(self.width() - rect.x() - self.sidebar.width(), self.list_widget.height())
        self.text_edit.resize(self.width() - rect.x() - self.sidebar.width(), self.text_edit.height())
        self.button.resize(self.width() - rect.x() - self.sidebar.width(), self.button.height())
        self.layout.setContentsMargins(rect.x() + self.sidebar.width(), 0, 0, 0)

    def resizeEvent(self, event):
        print('resizeEvent')
        # 当A窗口大小改变时，调整B部件的高度
        self.sidebar.setFixedHeight(self.height())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    """ window.resize(400, 300) """
    window.show()
    sys.exit(app.exec_())