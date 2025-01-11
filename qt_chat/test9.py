import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QTextDocument
from PyQt5.QtWebEngineWidgets import QWebEngineView  
#import markdown2  
  
class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        text = '''# 欢迎来到Markdown世界
    这是一篇简单的Markdown文档示例，用于展示Markdown的基本语法和功能。  
## 标题2
### 标题3
    Markdown是一种轻量级标记语言，它允许人们使用易读易写的纯文本格式编写文档，然后转换成有效的HTML。Markdown的语法简洁明了，易于学习和使用。
## 段落
    这是第一个段落。Markdown使用空行来分隔段落，所以你可以简单地按下回车键来开始一个新的段落。
    这是第二个段落。你可以在段落中添加**粗体**或*斜体*文本，以及[超链接](https://www.example.com)。
## 列表
### 无序列表
- 项目1
- 项目2
- 子项目1
- 子项目2
- 项目3
### 有序列表
1. 第一步
2. 第二步
3. 第三步
## 代码块
    你可以使用三个反引号来创建一个代码块。例如：
```python  
def hello_world():  
print("Hello, World!")

数学公式：
$$E = mc^2$$
$$\sum_{i=1}^n a_i$$
$$\\frac{a}{b} = c$$
积分公式：
$$\int_{a}^{b} f(x) \ dx = F(b) - F(a)$$
求导公式：
$$\\frac{d}{dx} e^x = e^x$$
'''

        #self.setGeometry(100, 100, 1000, 1000)  
        # Create a central widget and set the layout  
        central_widget = QWidget()  
        self.setCentralWidget(central_widget)  
        layout = QVBoxLayout(central_widget)  
        # Create a QWebEngineView to display the HTML content  
        self.web_view = WebEngineView()  
        layout.addWidget(self.web_view)  

        #self.textEdit = QTextEdit()
        #layout.addWidget(self.textEdit)

        #documentStr = QTextDocument('锄禾日当午')
        #htmlStr = documentStr.toHtml()

        # Set the HTML content in the QWebEngineView  
        #self.web_view.setHtml(htmlStr)  

        #self.textEdit.setHtml(htmlStr)

        documentText = QTextDocument(text)
        htmlText = documentText.toHtml()
        print(htmlText)

        self.web_view.setHtml(htmlText)

        #self.textEdit.setHtml(htmlText)
        #self.textEdit.setMarkdown(text)

        layout.setContentsMargins(5, 5, 5, 5)
        central_widget.setFixedSize(self.web_view.width() + 10, self.web_view.height() + 10)
        #central_widget.setFixedSize(self.textEdit.width() + 10, self.textEdit.height() + 10)
        self.setFixedSize(central_widget.size())

class WebEngineView(QWebEngineView):
    def __init__(self, isUser=True, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.isUser = isUser
        self.isColorful = False

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        if self.isColorful:
            brush.setColor(QColor(119, 221, 255))
        else:
            if self.isUser:
                brush.setColor(QColor(255, 238, 153))
            else:
                brush.setColor(QColor(209, 187, 255))
        #add rect and set brush
        if self.isUser:
            path.addRect(self.rect().width() - 15, self.rect().y(), 15, 15)
        else:
            path.addRect(self.rect().x(), self.rect().y(), 15, 15)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())
