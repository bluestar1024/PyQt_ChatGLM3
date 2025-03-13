import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QProxyStyle, QMainWindow, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class CustomMenuStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        if element == self.PE_FrameMenu:
            # 自定义菜单边框样式
            option.rect.adjust(-1, -1, 1, 1)  # 扩展边框范围
            painter.setRenderHint(painter.Antialiasing, True)
            painter.drawRoundedRect(option.rect, 10, 10)  # 绘制圆角矩形
            return
        super().drawPrimitive(element, option, painter, widget)

class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel("右键点击我", self)
        self.label.move(50, 50)
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置上下文菜单策略
        self.label.customContextMenuRequested.connect(self.showContextMenu)  # 连接信号与槽

        """ self.label.setStyle(CustomMenuStyle()) """

    def showContextMenu(self, pos):
        menu = CustomMenu(self.label)
        action1 = menu.addAction("选项1")
        action1.setShortcut("Ctrl+1")  # 设置快捷键
        action1.setToolTip("这是选项1")  # 设置提示信息
        action2 = menu.addAction("选项2")
        menu.addSeparator()  # 添加分割线
        action3 = menu.addAction("选项3")

        # 设置菜单项的样式
        action1.setIcon(QIcon("cut.png"))  # 设置图标
        action2.setCheckable(True)  # 设置为可勾选
        action3.setEnabled(False)  # 设置为不可用

        # 连接信号与槽
        action1.triggered.connect(lambda: print("选项1被点击"))

        # 显示菜单
        menu.exec_(self.label.mapToGlobal(pos))  # 将局部坐标转换为全局坐标


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
    * {
        outline: none;
    }
    QMenu {
        background-color: lightblue;
        border: none;
        border-radius: 15px;
        padding: 5px;  /* 菜单内边距 */
    }
    QMenu::item {
        padding: 5px;
    }
    QMenu::item:selected {
        background-color: lightgreen;
    }
    """)

    ex = Example()
    ex.show()
    sys.exit(app.exec_())
