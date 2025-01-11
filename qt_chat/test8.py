import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QTextBrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QTextDocument
from PyQt5.QtWebEngineWidgets import QWebEngineView
import mistune

class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        text = """
# 一级标题
## 二级标题
这是一个段落，包含一些 *Markdown* 语法。
## LaTeX公式：
$$E = mc^2$$
$$\sum_{i=1}^n a_i$$
$$\\frac{a}{b} = c$$
积分公式：
$$\int_{a}^{b} f(x) \ dx = F(b) - F(a)$$
求导公式：
$$\\frac{d}{dx} e^x = e^x$$
"""

        # 使用 mistune 将 Markdown 转换为 HTML
        markdown = mistune.create_markdown()
        html_content = markdown(text)

        # 添加 MathJax CDN 链接到 HTML 头部
        mathjax_cdn = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Markdown with MathJax</title>
            <script type="text/javascript" async
                src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
            </script>
        </head>
        """

        # 将转换后的 HTML 内容添加到 body 中
        full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>"

        #self.setGeometry(100, 100, 1000, 1000)  
        # Create a central widget and set the layout  
        central_widget = QWidget()  
        self.setCentralWidget(central_widget)  
        layout = QVBoxLayout(central_widget)  
        # Create a QWebEngineView to display the HTML content  
        #self.textEdit = QTextEdit()  
        #layout.addWidget(self.textEdit)

        self.textBrowser = QTextBrowser()
        layout.addWidget(self.textBrowser)

        # textEdit
        #self.textBrowser.setMarkdown(text)
        '''documentText = QTextDocument(text)
        htmlText = documentText.toHtml()
        self.textEdit.setHtml(htmlText)
        print(htmlText)'''
        self.textBrowser.setHtml(full_html_content)

        self.textBrowser.setReadOnly(True)
        self.textBrowser.setLineWrapMode(QTextEdit.NoWrap)
        self.textBrowser.setStyleSheet("background-color: white; font-family: Arial; font-size: 14px;")
        self.textBrowser.setFixedWidth(800)
        self.textBrowser.setFixedHeight(600)
        # Set the layout margins and central widget size  
        layout.setContentsMargins(5, 5, 5, 5)
        central_widget.setFixedSize(self.textBrowser.width() + 10, self.textBrowser.height() + 10)
        self.setFixedSize(central_widget.size())

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())
