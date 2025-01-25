import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView  
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):  
    def __init__(self):  
        super(MainWindow, self).__init__()  

        # 设置窗口  
        self.setWindowTitle("QWebEngineView 字体大小设置")  
        self.setGeometry(100, 100, 800, 600)  

        # 创建 QWebEngineView  
        self.browser = QWebEngineView()  
        self.browser.setUrl(QUrl("http://www.baidu.com"))  # 你可以改成任何你想要加载的 URL  

        # 设置字体大小  
        font = QFont()  
        font.setPixelSize(50)
        self.browser.setFont(font)
        """ font.setPointSize(14)  # 设置字体大小为14点  
        self.browser.settings().setDefaultFontSize(14)  # 设置默认字体大小   """

        # 布局  
        layout = QVBoxLayout()  
        layout.addWidget(self.browser)  

        container = QWidget()  
        container.setLayout(layout)  
        self.setCentralWidget(container)  

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())