import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import json

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        # 初始HTML内容，包含一个用于追加内容的div
        self.html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                #content {
                    white-space: pre-wrap; /* 保留空白和换行 */
                    word-wrap: break-word; /* 长单词换行 */
                }
            </style>
        </head>
        <body>
            <div id="content"></div>
        </body>
        </html>
        """
        self.web_view.setHtml(self.html_content)
        
        # 一个按钮用于模拟追加内容
        self.add_content_button = QPushButton("Add Content")
        self.add_content_button.clicked.connect(self.add_content)
        self.layout.addWidget(self.add_content_button)
        
        self.setLayout(self.layout)
        
        # 等待页面加载完成再执行JavaScript
        self.web_view.page().loadFinished.connect(self.on_load_finished)
        
    def on_load_finished(self, ok):
        if ok:
            # 页面加载完成后立即滚动到底部（虽然此时还没有新内容）
            self.scroll_to_bottom()
        
    def add_content(self):
        # 要追加的新内容
        new_content = "This is a new line of text.\n\n\n"
        js_new_content = json.dumps(new_content)
        print(js_new_content)
        # 使用JavaScript追加内容并滚动到底部
        js = f'''
        var contentDiv = document.getElementById('content');
        contentDiv.innerHTML += {js_new_content};
        contentDiv.scrollBottom = contentDiv.scrollHeight;
        '''
        self.web_view.page().runJavaScript(js)
        
    def scroll_to_bottom(self):
        # 这个方法在需要时可以用来手动滚动到底部（例如，在内容大量更新后）
        js = """
        var contentDiv = document.getElementById('content');
        contentDiv.scrollBottom = contentDiv.scrollHeight;
        """
        self.web_view.page().runJavaScript(js)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())