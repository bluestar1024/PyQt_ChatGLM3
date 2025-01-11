'''import sys  
from PyQt5.QtWidgets import QApplication, QWidget  
from PyQt5.QtGui import QPainter, QColor, QLinearGradient  
from PyQt5.QtCore import Qt, QRect  
  
class BlurSideEffectWidget(QWidget):  
    def __init__(self, parent=None):  
        super(BlurSideEffectWidget, self).__init__(parent)  
  
    def paintEvent(self, event):  
        painter = QPainter(self)  
  
        # 绘制正常矩形  
        rect = QRect(10, 10, 200, 100)  
        painter.setPen(Qt.black)  
        painter.setBrush(QColor(255, 255, 255))  
        painter.drawRect(rect)  
  
        # 在矩形的一侧绘制渐变以模拟模糊效果  
        # 这里我们选择右侧  
        gradient_rect = QRect(rect.right(), rect.top(), 50, rect.height())  # 渐变矩形的位置和大小  
        gradient = QLinearGradient(gradient_rect.topLeft(), gradient_rect.bottomRight())  
        gradient.setColorAt(0, QColor(255, 255, 255, 255))  # 起始颜色（完全透明）  
        gradient.setColorAt(1, QColor(255, 255, 255, 0))    # 结束颜色（完全透明）  
        # 注意：这里的透明度设置可能需要根据实际效果进行调整  
        # 由于我们想要的是“模糊”效果，所以实际上应该使用半透明的颜色，但这里为了演示，我们使用了从完全不透明到完全透明的渐变  
  
        # 绘制渐变  
        painter.setBrush(gradient)  
        painter.setPen(Qt.NoPen)  
        painter.drawRect(gradient_rect)  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    widget = BlurSideEffectWidget()  
    widget.resize(300, 200)  # 设置窗口大小  
    widget.show()  
    sys.exit(app.exec_())'''


'''import sys  
from PyQt5.QtWidgets import QApplication, QWidget  
from PyQt5.QtGui import QPainter, QColor, QLinearGradient  
from PyQt5.QtCore import Qt, QRect  
  
class BlurSideEffectWidget(QWidget):  
    def __init__(self, parent=None):  
        super(BlurSideEffectWidget, self).__init__(parent)  
        # 设置窗口为无边框  
        self.setWindowFlags(Qt.FramelessWindowHint)  
        # 设置背景透明（可选，因为QWidget默认背景就是透明的）  
        self.setAttribute(Qt.WA_TranslucentBackground)  
  
    def paintEvent(self, event):  
        painter = QPainter(self)  
  
        # 绘制正常矩形  
        rect = QRect(10, 10, 200, 100)  
        painter.setPen(Qt.black)  
        painter.setBrush(QColor(255, 255, 255))  
        painter.drawRect(rect)  
  
        # 在矩形的一侧绘制渐变以模拟模糊效果  
        # 这里我们选择右侧  
        gradient_rect = QRect(rect.right(), rect.top(), 50, rect.height())  
        gradient = QLinearGradient(gradient_rect.topLeft(), gradient_rect.bottomRight())  
        gradient.setColorAt(0, QColor(255, 255, 255, 255))  # 起始颜色（不透明）  
        gradient.setColorAt(1, QColor(255, 255, 255, 0))    # 结束颜色（透明）  
  
        # 绘制渐变  
        painter.setBrush(gradient)  
        painter.setPen(Qt.NoPen)  
        painter.drawRect(gradient_rect)  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    widget = BlurSideEffectWidget()  
    # 设置窗口大小（可选，因为你可以通过调整矩形大小来控制显示区域）  
    widget.resize(300, 200)  
    widget.show()  
    sys.exit(app.exec_())'''


'''import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget  
from PyQt5.QtGui import QPainter, QColor, QLinearGradient  
from PyQt5.QtCore import Qt, QRect  
  
# 自定义控件，用于绘制矩形和阴影  
class BlurEffectWidget(QWidget):  
    def __init__(self, parent=None):  
        super(BlurEffectWidget, self).__init__(parent)  
        # 设置背景透明（可选，但QWidget默认背景就是透明的）  
        self.setAttribute(Qt.WA_TranslucentBackground)  
  
    def paintEvent(self, event):  
        painter = QPainter(self)  
  
        # 绘制正常矩形  
        rect = QRect(10, 10, 200, 100)  
        painter.setPen(Qt.black)  
        painter.setBrush(QColor(255, 255, 255))  
        painter.drawRect(rect)  
  
        # 在矩形的一侧绘制渐变以模拟阴影效果  
        # 这里我们选择右侧  
        gradient_rect = QRect(rect.right(), rect.top(), 50, rect.height())  
        gradient = QLinearGradient(gradient_rect.topLeft(), gradient_rect.bottomRight())  
        gradient.setColorAt(0, QColor(255, 255, 255, 128))  # 起始颜色（半透明）  
        gradient.setColorAt(1, QColor(255, 255, 255, 0))    # 结束颜色（透明）  
  
        # 绘制渐变  
        painter.setBrush(gradient)  
        painter.setPen(Qt.NoPen)  
        painter.drawRect(gradient_rect)  
  
# 自定义QMainWindow  
class MainWindow(QMainWindow):  
    def __init__(self):  
        super(MainWindow, self).__init__()  
  
        # 创建自定义控件  
        self.blurEffectWidget = BlurEffectWidget(self)  
  
        # 设置中央控件  
        self.setCentralWidget(self.blurEffectWidget)  
  
        # 设置窗口为无边框（可选）  
        self.setWindowFlags(Qt.FramelessWindowHint)  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
  
    # 创建并显示窗口  
    mainWindow = MainWindow()  
    mainWindow.resize(300, 200)  # 设置窗口大小  
    mainWindow.show()  
  
    sys.exit(app.exec_())'''


import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget  
from PyQt5.QtGui import QPainter, QColor, QLinearGradient  
from PyQt5.QtCore import Qt, QRect  
  
# 自定义控件，用于绘制矩形和阴影  
class BlurEffectWidget(QWidget):  
    def __init__(self, parent=None):  
        super(BlurEffectWidget, self).__init__(parent)  
        # 设置背景透明（对于QWidget，这通常是默认的，但明确设置也无妨）  
        self.setAttribute(Qt.WA_TranslucentBackground)  
  
    def paintEvent(self, event):  
        painter = QPainter(self)  
  
        # 绘制正常矩形  
        rect = QRect(10, 10, 200, 100)  
        painter.setPen(Qt.black)  
        painter.setBrush(QColor(255, 255, 255))  
        painter.drawRect(rect)  
  
        # 绘制阴影（渐变）  
        gradient_rect = QRect(rect.right(), rect.top(), 50, rect.height())  
        gradient = QLinearGradient(gradient_rect.topLeft(), gradient_rect.bottomRight())  
        gradient.setColorAt(0, QColor(0, 0, 0, 128))  # 起始颜色（半透明的黑色）  
        gradient.setColorAt(1, QColor(0, 0, 0, 0))    # 结束颜色（透明）  
  
        # 绘制渐变  
        painter.setBrush(gradient)  
        painter.setPen(Qt.NoPen)  
        painter.drawRect(gradient_rect)  
  
# 自定义QMainWindow  
class MainWindow(QMainWindow):  
    def __init__(self):  
        super(MainWindow, self).__init__()  
  
        # 创建自定义控件  
        self.blurEffectWidget = BlurEffectWidget(self)  
  
        # 设置中央控件  
        self.setCentralWidget(self.blurEffectWidget)  
  
        # 移除标题栏和边框  
        self.setWindowFlags(Qt.FramelessWindowHint)  
  
        # 这一步是可选的，用于确保窗口在屏幕上居中显示  
        # 注意：这不会影响窗口的透明性，只是调整了位置  
        self.setGeometry(100, 100, 300, 200)  # x, y, width, height  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
  
    # 创建并显示窗口  
    mainWindow = MainWindow()  
    mainWindow.show()  
  
    sys.exit(app.exec_())