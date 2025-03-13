import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 去掉标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明背景

        # 设置窗口大小
        self.resize(400, 300)

        # 添加一个标签作为内容
        label = QLabel("这是一个无标题栏的圆角窗口", self)
        label.setStyleSheet("color: black; font-size: 16px;")
        label.adjustSize()
        label.move(20, 20)

        """ # 设置窗口的圆角样式
        self.setStyleSheet('''
        MainWindow {
            background-color: rgba(0, 200, 0, 100); /* 透明背景 */
            border: 2px solid #FF0000; /* 红色边框 */
            border-radius: 20px; /* 圆角半径 */
        }
        ''') """

    def paintEvent(self, event):
        # 使用 QPainter 绘制圆角矩形
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 设置圆角矩形的路径
        path = QPainterPath()
        path.addRoundedRect(0, 0, 400, 300, 20, 20)  # 圆角半径为 20

        # 设置背景颜色
        painter.fillPath(path, Qt.green)  # 半透明背景

        # 如果需要绘制边框，可以取消注释以下代码
        painter.strokePath(path, QColor(255, 0, 0))  # 红色边框


if __name__ == "__main__":
    app = QApplication(sys.argv)
    """ # 设置窗口的圆角样式
    app.setStyleSheet('''
    QMainWindow {
        background-color: rgba(0, 0, 0, 0); /* 透明背景 */
        border: 2px solid #FF0000; /* 红色边框 */
        border-radius: 20px; /* 圆角半径 */
    }
    ''') """
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
