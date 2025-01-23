import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction  
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage  
from PyQt5.QtCore import QUrl  


class CustomWebEnginePage(QWebEnginePage):  
    def __init__(self, parent=None):  
        super(CustomWebEnginePage, self).__init__(parent)  
        self.windows = []

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):  
        # 打开新窗口并加载 URL  
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:  
            newView = QWebEngineView()  
            newView.setUrl(url)  
            """ new_view.show()  # 显示新窗口   """
            newWindow= QMainWindow()
            newWindow.setWindowTitle("窗口")  
            newWindow.setCentralWidget(newView)
            newWindow.resize(800, 600)
            newWindow.show()
            self.windows.append(newWindow)
            newWindow.destroyed.connect(lambda: self.windows.remove(newWindow))
            return False  # 阻止当前的 QWebEngineView 跳转  
        return True  # 处理其它导航请求  


class CustomWebEngineView(QWebEngineView):  
    def __init__(self, parent=None):  
        super(CustomWebEngineView, self).__init__(parent)  
        self.setPage(CustomWebEnginePage(self))  # 将自定义页面设置给视图  


class MainWindow(QMainWindow):  
    def __init__(self, parent=None):  
        super(MainWindow, self).__init__(parent)  
        self.setWindowTitle("Markdown Links in QWebEngineView")  
        
        # 布局  
        central_widget = QWidget()  
        layout = QVBoxLayout(central_widget)  
        
        # 创建定制的QWebEngineView  
        self.browser = CustomWebEngineView(self)  
        
        # 加载Markdown转换后的HTML内容  
        markdown_content = """  
        <html>  
        <body>  
        <h1>Markdown Links Example</h1>  
        <p>This is a link to <a href='https://www.iconfont.cn/collections/index?spm=a313x.home_index.1998910419.38.58a33a81FSDbgx'>Example Domain</a>.</p>  
        </body>  
        </html>  
        """  
        self.browser.setHtml(markdown_content)  
        
        layout.addWidget(self.browser)  
        self.setCentralWidget(central_widget)  

        # 登出操作  
        quit_action = QAction("Quit", self)  
        quit_action.triggered.connect(QApplication.instance().quit)  
        self.menuBar().addAction(quit_action)  

        self.resize(800, 600)

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())