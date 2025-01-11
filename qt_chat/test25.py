import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QVBoxLayout, QWidget  
import markdown2  # 请确保已安装 markdown2 库  

class MarkdownToHtmlConverter(QMainWindow):  
    def __init__(self):  
        super().__init__()  

        self.setWindowTitle("Markdown Table to HTML Converter")  
        self.setGeometry(100, 100, 800, 600)  

        # Create a QTextBrowser to display the rendered HTML  
        self.text_browser = QTextBrowser()  

        # Sample Markdown with a table  
        markdown_text = """  
        # Sample Markdown Table  

        | Name    | Age | City      |  
        |---------|-----|-----------|  
        | Alice   | 30  | New York  |  
        | Bob     | 25  | Los Angeles|  
        | Charlie | 35  | Chicago   |  
        """  

        # Convert Markdown to HTML  
        html_content = markdown2.markdown(markdown_text)  

        # Wrap the HTML content in a simple HTML structure for better rendering  
        full_html = f"""  
        <html>  
        <head>  
            <meta charset="utf-8">  <!-- 确保字符编码为 UTF-8 -->  
            <style>  
                body {{  
                    font-family: Arial, sans-serif;  
                    margin: 20px;  
                }}  
                table {{  
                    width: 100%;  
                    border-collapse: collapse;  
                    margin-top: 20px;  
                }}  
                th, td {{  
                    border: 1px solid black;  
                    padding: 8px;  
                    text-align: left;  
                }}  
                th {{  
                    background-color: #f2f2f2;  
                }}  
            </style>  
        </head>  
        <body>  
            {html_content}  
        </body>  
        </html>  
        """  

        # Set HTML content in QTextBrowser  
        self.text_browser.setHtml(full_html)  

        # Set up layout  
        layout = QVBoxLayout()  
        layout.addWidget(self.text_browser)  

        container = QWidget()  
        container.setLayout(layout)  
        self.setCentralWidget(container)  

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    viewer = MarkdownToHtmlConverter()  
    viewer.show()  
    sys.exit(app.exec_())