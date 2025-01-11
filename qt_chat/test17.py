import sys  
import markdown  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser  
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MarkdownViewer(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  

    def initUI(self):  
        self.setWindowTitle('Markdown + Math Example')  
        self.setGeometry(100, 100, 800, 600)  

        central_widget = QWidget()  
        self.setCentralWidget(central_widget)  
        layout = QVBoxLayout(central_widget)  

        # 创建 QWebEngineView  
        self.webView = QWebEngineView()  

        # 读取 Markdown 文件并转换为 HTML  
        with open('test.md', 'r', encoding='utf-8') as f:  
            md_content = f.read()  
            html_content = markdown.markdown(md_content, extensions=['markdown.extensions.fenced_code'])  

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
                <script type="text/javascript" async
                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.1.2/es5/tex-mml-chtml.js">
                </script>  
            </head>  
            """  

            full_html_content = f"{mathjax_cdn}<body>\n{html_content}\n</body>\n</html>\n"

        self.webView.setHtml(full_html_content)  
        layout.addWidget(self.webView)  
        print(html_content)

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    viewer = MarkdownViewer()  
    viewer.show()  
    sys.exit(app.exec_())  