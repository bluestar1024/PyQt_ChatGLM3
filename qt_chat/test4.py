from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout  
  
class ExampleApp(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
  
    def initUI(self):  
        btn = QPushButton('Hover Over Me', self)  
        btn.setToolTip("鼠标悬停文本")  # 直接设置工具提示  
        btn.resize(btn.sizeHint())  
        btn.move(50, 50)  
  
        layout = QVBoxLayout(self)  
        layout.addWidget(btn)  
  
        self.setGeometry(300, 300, 300, 200)  
        self.setWindowTitle('Hover Button Example')  
        self.show()  
  
if __name__ == '__main__':  
    app = QApplication([])  
    ex = ExampleApp()  
    app.exec_()