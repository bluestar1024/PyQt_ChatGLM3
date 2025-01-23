import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton  
from PyQt5.QtCore import QEvent, QObject, QCoreApplication  

class CustomEventFilter(QObject):  
    def eventFilter(self, obj, event):  
        if event.type() == QEvent.MouseButtonPress:  
            print(f"Mouse press event caught in {obj}, posting to target.")  
            # 创建一个新的鼠标事件，并将其发送到目标对象  
            custom_event = QEvent(QEvent.MouseButtonPress)  
            QCoreApplication.postEvent(target_widget, custom_event)  
        return super().eventFilter(obj, event)  

class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.button = QPushButton("Click Me", self)  
        self.button.setGeometry(100, 100, 100, 50)  

        self.button.installEventFilter(CustomEventFilter())  
    
    def event(self, event):  
        if event.type() == QEvent.MouseButtonPress:  
            print("Mouse button pressed on the main window.")  
        return super().event(event)  

target_widget = None  

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    window = MainWindow()  
    target_widget = window.button  # 设置目标widget  
    window.show()  
    sys.exit(app.exec_())
    