import markdown  
import markdown2  
import mistune
from markdown_it import MarkdownIt  
import sys  
import markdown  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextBrowser  
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MarkdownViewer(QMainWindow):  
    def __init__(self):  
        super().__init__()  

        # 定义Markdown文本，其中包含LaTeX公式  
        markdown_text = r"""  
# 指数函数的导数  

在这里，我们展示了指数函数的导数:  

$$  
\frac{d}{dx} e^x = e^x  
$$  
| 表头   |   表头 |  表头  |
| :----- | -----: | :----: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |
"""  

        self.setWindowTitle('Markdown + Math Example')  
        self.setGeometry(100, 100, 800, 600)  

        central_widget = QWidget()  
        self.setCentralWidget(central_widget)  
        layout = QVBoxLayout(central_widget)  

        # 创建 QWebEngineView  
        self.webView = QWebEngineView()  

        # 初始化 Markdown-It 解析器  
        #md = MarkdownIt()  

        # 解析 Markdown 到 HTML  
        #html_content = md.parse(self.text)  

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

        # 转换Markdown为HTML  
        # 使用markdown2库的'code-friendly'扩展，这个扩展可以正确处理\字符  
        html_output = markdown.markdown(markdown_text, extras=["fenced-code-blocks", "table", "mathjax"])  

        #markdown = mistune.create_markdown()
        #html_content = markdown(markdown_text)

        # 打印转换后的HTML  
        print(html_output)  

        full_html_content = f"{mathjax_cdn}<body>\n{html_output}\n</body>\n</html>\n"

        html_text_2 = '''
<h1>指数函数的导数</h1>  
<p>在这里，我们展示了指数函数的导数:</p>  
<div class="math">  
    $   
    \frac{d}{dx} e^x = e^x   
    $  
</div>  
'''
        self.webView.setHtml(full_html_content)  
        layout.addWidget(self.webView)  
        # 打印生成的 HTML  
        #print(full_html_content)  

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    viewer = MarkdownViewer()  
    viewer.show()  
    sys.exit(app.exec_())  