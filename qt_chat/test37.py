import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget  
from PyQt5.QtWebEngineWidgets import QWebEngineView  

class ChatWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  

        self.setWindowTitle("Chat Application")  
        self.setGeometry(100, 100, 600, 400)  

        self.web_view = QWebEngineView()  
        self.web_view.setHtml("<html><body><div id='chat'></div></body></html>")  

        self.button = QPushButton("Add Message")  
        self.button.clicked.connect(self.add_message)  

        layout = QVBoxLayout()  
        layout.addWidget(self.web_view)  
        layout.addWidget(self.button)  

        container = QWidget()  
        container.setLayout(layout)  
        self.setCentralWidget(container)  

    def add_message(self):  
        # 添加新消息  
        new_message = "<p>New message at the bottom!</p>"  
        js_code = f"""  
            var chat = document.getElementById('chat');  
            chat.innerHTML += '{new_message}';  
            window.scrollTo(0, document.body.scrollHeight);  
        """  
        self.web_view.page().runJavaScript(js_code)  

if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    window = ChatWindow()  
    window.show()  
    sys.exit(app.exec_())