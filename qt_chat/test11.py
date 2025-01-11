import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown with LaTeX")
        self.setGeometry(100, 100, 800, 600)

        # 创建一个容器
        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        # 创建 QWebEngineView 控件
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)

        # 设置 Markdown 和 LaTeX 内容
        markdown_text = """
# 一级标题
## 二级标题
这是一个段落，包含一些 *Markdown* 语法。
## LaTeX 公式：
$$E = mc^2$$
$$\\frac{a}{b} = c$$
"""

        # 将 Markdown 转换为 HTML，并加载到 QWebEngineView 中
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body style="padding: 20px;">
            {markdown_text}        </body>
        </html>
        """
        self.web_view.setHtml(str(html_content))

if __name__ == "__main__":# <em>Markdown</em> 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())