from markdown_it import MarkdownIt  
import sys  
import markdown  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser  
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MarkdownViewer(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        # Markdown 文本  
        self.text = """  
        # Hello, Markdown!  
        这是一个包含公式的示例：$E=mc^2$  
        $$\sum_{i=1}^n a_i$$
        $$\frac{a}{b} = c$$
        积分公式：
        $$\int_{a}^{b} {f(x)} \, \mathrm{d}x = F(b) - F(a)$$
        微分公式：
        $$\frac{d}{dx} e^x = e^x$$
        """  

        self.initUI()  

    def initUI(self):  
        self.setWindowTitle('Markdown + Math Example')  
        self.setGeometry(100, 100, 800, 600)  

        central_widget = QWidget()  
        self.setCentralWidget(central_widget)  
        layout = QVBoxLayout(central_widget)  

        # 创建 QWebEngineView  
        self.webView = QWebEngineView()  

        # 初始化 Markdown-It 解析器  
        md = MarkdownIt()  

        # 解析 Markdown 到 HTML  
        html_content = md.parse(self.text)  

        # 添加 MathJax 支持  
        mathjax_cdn = """  
        <html>  
        <head>  
            <script type="text/javascript">
                MathJax = {
                    tex: {
                        inlineMath: [["$", "$"], ["\\(", "\\)"]],
                        displayMath: [["$$", "$$"], ["\\[", "\\]"]]
                    },
                    svg: {
                        fontCache: 'global'
                    }
                };
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>  
        """  

        full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>\n"

        self.webView.setHtml(full_html_content)  
        layout.addWidget(self.webView)  
        # 打印生成的 HTML  
        print(full_html_content)  

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    viewer = MarkdownViewer()  
    viewer.show()  
    sys.exit(app.exec_())  