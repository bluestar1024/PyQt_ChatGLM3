import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, 
                            QListWidgetItem, QLabel, QVBoxLayout, QWidget, 
                            QScrollBar)
from PyQt5.QtCore import Qt, QTimer

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Demo")
        self.setGeometry(100, 100, 400, 600)
        
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建聊天列表控件
        self.chat_list = QListWidget()
        self.chat_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        layout.addWidget(self.chat_list)
        
        # 初始化消息计数器
        self.message_count = 0
        
        # 设置定时器模拟持续接收消息
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_new_message)
        self.timer.start(1000)  # 每秒添加一条消息

    def add_new_message(self):
        """添加新消息到聊天窗口"""
        self.message_count += 1
        message = f"Message {self.message_count}: {'This is a test message. ' * (self.message_count % 3)}"
        
        # 创建列表项
        item = QListWidgetItem()
        self.chat_list.addItem(item)
        
        # 创建消息标签
        label = QLabel(message)
        label.setMargin(8)
        label.setWordWrap(True)
        label.setStyleSheet("""
            background-color: #e1f5fe;
            border-radius: 8px;
            border: 1px solid #b3e5fc;
        """)
        
        # 计算合适的大小并设置到列表项
        label.adjustSize()
        item.setSizeHint(label.sizeHint())
        
        # 将标签设置为列表项的部件
        self.chat_list.setItemWidget(item, label)
        
        # 获取滚动条并判断位置
        scroll_bar = self.chat_list.verticalScrollBar()
        at_bottom = scroll_bar.value() == scroll_bar.maximum()
        
        # 自动滚动到底部（如果之前已经在底部）
        if at_bottom:
            self.chat_list.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())