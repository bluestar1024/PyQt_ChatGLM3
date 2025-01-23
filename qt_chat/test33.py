from PyQt5 import QtCore,QtGui,QtWidgets,QtWebEngineWidgets
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QtWidgets.QMainWindow.setFixedSize(self,800,400)
        self.webview = WebEngineView()
        self.webview.load(QtCore.QUrl("https://www.baidu.com"))
        self.setCentralWidget(self.webview)
class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    windows = [] #创建一个容器存储每个窗口，不然会崩溃，因为是createwindow函数里面的临时变量
    def createWindow(self, QWebEnginePage_WebWindowType):
        newtab =   WebEngineView()
        newwindow= MainWindow()
        newwindow.setCentralWidget(newtab)
        newwindow.show()
        self.windows.append(newwindow)
        return newtab
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
