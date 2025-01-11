import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # 加载包含MathJax的HTML页面
        mathjax_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head>
        <body>
            <div>
                $$E = mc^2$$
            </div>
        </body>
        </html>
        """

        formula_html = '''
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MathJax 示例</title>
            <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            <h1>MathJax 渲染示例</h1>

            <p>这是一个行内公式：\( E = mc^2 \)</p>

            <p>这是一个块级公式：</p>
            \[
            \int_{a}^{b} f(x) \, dx = F(b) - F(a)
            \]

            <p>你还可以使用其他 LaTeX 公式，比如：\( \\frac{d}{dx} e^x = e^x \)</p>
        </body>
        </html>
        '''
        self.browser.setHtml(formula_html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())