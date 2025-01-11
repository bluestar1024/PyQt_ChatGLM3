import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self, math_formula):
        super().__init__()

        self.setWindowTitle('MathJax in PyQt')
        self.setGeometry(100, 100, 800, 600)

        # 创建中心窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建 QWebEngineView
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # 构建包含 MathJax 的 HTML 内容
        mathjax_script = """
        <script type="text/javascript" async
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
        </script>
        """
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            {mathjax_script}
        </head>
        <body>
            <div id="math">
                \\[{math_formula}\\]
            </div>
        </body>
        </html>
        """
        # 将公式插入到 HTML 模板中
        html_content = html_template.format(math_formula=math_formula)

        # 加载 HTML 内容到 QWebEngineView
        self.browser.setHtml(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 传递你想要渲染的数学公式
    window = MainWindow(r'\frac{a}{b} = c')
    window.show()
    sys.exit(app.exec_())