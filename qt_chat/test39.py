import sys
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, 
                            QListWidgetItem, QLabel, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_timers()
        
    def setup_ui(self):
        self.setWindowTitle("Chat Demo")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.chat_list = QListWidget()
        self.chat_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.chat_list.setStyleSheet("QListWidget { background: #f5f5f5; }")
        layout.addWidget(self.chat_list)
        
        self.message_count = 0
        
    def setup_timers(self):
        # 新消息定时器（每秒添加）
        self.msg_timer = QTimer()
        self.msg_timer.timeout.connect(self.add_new_message)
        self.msg_timer.start(1000)
        
        # 旧消息更新定时器（1.5秒更新）
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_random_message)
        self.update_timer.start(1500)
        
        # 长消息模拟定时器（3秒添加长消息）
        self.long_msg_timer = QTimer()
        self.long_msg_timer.timeout.connect(self.add_long_message)
        self.long_msg_timer.start(3000)

    @pyqtSlot()
    def add_new_message(self):
        """添加新消息到聊天列表底部"""
        self.message_count += 1
        msg = f"[New {self.message_count}] {datetime.now().strftime('%H:%M:%S')}"
        self._create_message_item(msg)
        self._conditional_scroll()

    @pyqtSlot()
    def add_long_message(self):
        """添加长文本消息测试滚动逻辑"""
        self.message_count += 1
        length = random.randint(3, 6)
        msg = f"[Long {self.message_count}] " + "This is a very long message. "*length
        self._create_message_item(msg)
        self._conditional_scroll()

    @pyqtSlot()
    def update_random_message(self):
        """随机选择并更新一条已有消息"""
        if self.message_count == 0:
            return
            
        # 随机选择要更新的消息（优先近期消息）
        index = max(0, self.message_count - 1 - random.randint(0, min(5, self.message_count-1)))
        item = self.chat_list.item(index)
        if not item:
            return
            
        label = self.chat_list.itemWidget(item)
        if label:
            # 保存当前滚动状态
            scroll_bar = self.chat_list.verticalScrollBar()
            old_max = scroll_bar.maximum()
            old_value = scroll_bar.value()
            was_at_bottom = old_value == old_max
            
            # 更新消息内容
            new_text = f"[Updated {index+1}] {datetime.now().strftime('%H:%M:%S')}"
            label.setText(new_text)
            label.adjustSize()
            item.setSizeHint(label.sizeHint())
            
            # 延迟滚动检查以确保布局更新完成
            QTimer.singleShot(0, lambda: self._conditional_scroll(was_at_bottom))

    def _create_message_item(self, message):
        """创建消息项通用方法"""
        item = QListWidgetItem()
        self.chat_list.addItem(item)
        
        label = QLabel(message)
        label.setMargin(10)
        label.setWordWrap(True)
        label.setStyleSheet("""
            QLabel {
                background: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                min-width: 200px;
                max-width: 600px;
            }
        """)
        label.adjustSize()
        item.setSizeHint(label.sizeHint())
        self.chat_list.setItemWidget(item, label)

    def _conditional_scroll(self, force_check=False):
        """
        智能滚动控制
        :param force_check: 强制检查当前是否应该滚动到底部
        """
        scroll_bar = self.chat_list.verticalScrollBar()
        
        if force_check:
            current_pos = scroll_bar.value()
            should_scroll = current_pos == scroll_bar.maximum()
        else:
            # 使用最后记录的滚动位置进行判断
            should_scroll = self._last_was_bottom if hasattr(self, '_last_was_bottom') else False
            
        if should_scroll:
            self.chat_list.scrollToBottom()
            
        # 记录当前滚动状态供下次使用
        self._last_was_bottom = scroll_bar.value() == scroll_bar.maximum()

    def showEvent(self, event):
        """窗口显示时初始化自动滚动状态"""
        self._last_was_bottom = True
        super().showEvent(event)

    def closeEvent(self, event):
        """关闭窗口时停止所有定时器"""
        self.msg_timer.stop()
        self.update_timer.stop()
        self.long_msg_timer.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())