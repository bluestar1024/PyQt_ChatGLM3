import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QPushButton, QHBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置无边框和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 创建背景容器
        self.background = QFrame(self)
        self.background.setObjectName("backgroundFrame")
        self.background.setStyleSheet(
            """
            #backgroundFrame {
                background-color: rgb(67, 94, 134);
                border-radius: 15px;
            }
            """
        )

        # 设置背景容器的大小和位置
        self.background.setGeometry(10, 10, self.width() - 20, self.height() - 20)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.background.setGraphicsEffect(shadow)

        # 创建自定义标题栏
        self.create_custom_title_bar()

        # 设置背景容器为中央部件
        self.setCentralWidget(self.background)
        print(self.background.geometry())
        print(self.geometry())

    def create_custom_title_bar(self):
        # 创建标题栏
        self.title_bar = QFrame(self.background)
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setStyleSheet(
            """
            #titleBar {
                background-color: rgb(45, 45, 45);
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                height: 40px;
            }
            """
        )
        self.title_bar.setGeometry(0, 0, self.background.width(), 40)

        # 创建标题标签
        title_label = QLabel("Custom Title Bar", self.title_bar)
        title_label.setStyleSheet("color: white; font-size: 16px; margin-left: 10px; margin-top: 10px;")
        title_label.setAlignment(Qt.AlignVCenter)

        # 创建关闭按钮
        close_button = QPushButton("X", self.title_bar)
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(244, 67, 54);
                border-radius: 5px;
            }
            """
        )
        close_button.setFixedSize(30, 30)
        close_button.move(self.title_bar.width() - 40, 5)

        close_button.clicked.connect(self.close)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 动态更新背景容器的大小和样式
        self.background.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        self.title_bar.resize(self.background.width(), 40)

    """ def changeEvent(self, event):
        super().changeEvent(event)

        if event.type() == Qt.WindowStateChange:
            if self.isMaximized() or self.isFullScreen():
                # 禁用圆角样式
                self.background.setStyleSheet("")
            else:
                # 恢复圆角样式
                self.background.setStyleSheet(
                    '''
                    #backgroundFrame {
                        background-color: rgb(67, 94, 134);
                        border-radius: 15px;
                    }
                    '''
                ) """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomMainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
