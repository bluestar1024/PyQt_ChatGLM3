
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QEventLoop, QObject, pyqtSignal, QEvent, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
 
class QWebEngineView_New(QWebEngineView):
    js_result = pyqtSignal(str)
    def __init__(self, parent=None):
        super(QWebEngineView_New, self).__init__(parent)
        self.load(QtCore.QUrl())
        self.setObjectName('web_view')
        self.focusProxy().installEventFilter(self)
        """ self.installEventFilter(self) """
        """ self.setMouseTracking(True) #追踪鼠标
        self._glwidget = None """

    """ def focusProxy(self):
        return self """

    def eventFilter(self, source, event):
        #  QWebEngineView 覆盖了 event() 方法，所以它没有调用 QWidget 事件处理程序
        """ if event.type() == QEvent.MouseButtonPress:
            print(f'eventtype:{event.type()} ChildAdded: {QEvent.ChildAdded} MouseButtonPress:{QEvent.MouseButtonPress}')
            print(source is self._glwidget)
        if event.type() == QEvent.ChildAdded and event.child().isWidgetType():
            self._glwidget = event.child()
            self._glwidget.installEventFilter(self) """
        if event.type() == QEvent.MouseButtonPress:
            #print(Qt.LeftButton)
            #print(QEvent.MouseButtonPress)
            #print('event_type:', event.type())
            print('obj parent:', source.parent().objectName())
            print('mousePress pos:', event.pos())
            custom_event = QEvent(QEvent.MouseButtonPress)  
            QCoreApplication.postEvent(source.parent(), custom_event)  
            """ pos = event.pos()
            self._run_javascript(pos.x(), pos.y()) """
            """ QWebEngineView_New.mousePressEvent(self, event) """
        return QWebEngineView.eventFilter(self, source, event)

    def mousePressEvent(self, event):
        print('view mousePressEvent')
        QWebEngineView.mousePressEvent(self, event)
        event.ignore()

    """ def _run_javascript(self, x, y):
        # 在这里写入你的 JavaScript 代码
        # js_code = "alert('Hello from JavaScript!');"
        js_code = '''function myFunction(){return document.elementFromPoint(%s, %s).textContent;}myFunction();'''
        js_code = js_code % (x, y)
        # self.fatherWindow.tabWidget.currentWidget().page().runJavaScript(js_code, self.js_callback)
        self.page().runJavaScript(js_code, self.js_callback)
 
    def js_callback(self, result):
        # 获取点击部位的内容
        if not result:
            return
        jsresult = result.replace('\n', '')
        print('jsresult :', jsresult )
        self.js_result.emit(jsresult ) # 将内容传给信号槽 """

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.web_view = QWebEngineView_New()
        self.web_view.load(QtCore.QUrl("https://www.baidu.com"))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.web_view)  
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)
        self.resize(600, 400)

        print(self.web_view.hasFocus())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('window mousePressEvent')
            QMainWindow.mousePressEvent(self, event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  
