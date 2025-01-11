import sys
import mistune
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel

class MarkdownConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown to HTML Converter")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.convert_button = QPushButton("Convert to HTML", self)
        self.convert_button.clicked.connect(self.convert_markdown)
        self.layout.addWidget(self.convert_button)

        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def convert_markdown(self):
        # 获取用户输入的Markdown文本
        markdown_text = self.text_edit.toPlainText()

        # 使用mistune将Markdown转换为HTML
        markdown = mistune.create_markdown()
        html_content = markdown(markdown_text)

        # 添加MathJax的CDN链接
        html_with_mathjax = f"""
        <html>
        <head>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # 显示结果
        self.result_label.setText(html_with_mathjax)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = MarkdownConverter()
    converter.show()
    sys.exit(app.exec_())
