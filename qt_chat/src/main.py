# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:31:44 2024

@author: YXD
"""

import sys, os
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QGridLayout, QLineEdit, QSplitter, QToolTip, QTextEdit, QMenu, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve, QEvent, QPoint, pyqtProperty, QTimer, QCoreApplication, QUrl
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen, QCursor, QFontDatabase, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from openai import OpenAI
import math
import mistune

#test
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
font_file_path = os.path.normpath(os.path.join(current_dir, '..', 'font', 'msyhl.ttc')).replace('\\', '/')
images_dir = os.path.normpath(os.path.join(current_dir, '..', 'images')).replace('\\', '/')
config_file_path = os.path.normpath(os.path.join(current_dir, '..', 'config', 'config.txt'))
mathjax_script_path = os.path.normpath(os.path.join(current_dir, '..', 'mathjax/es5/tex-mml-chtml.js')).replace('\\', '/')
chat_records_dir = os.path.normpath(os.path.join(current_dir, '..', 'chatrecords'))

init_base_url = "http://7613907zg6.vicp.fun:45861/v1"
init_api_key = "EMPTY"
init_model = "deepseek-r1:14b"
maxTokens_minimum = 0
maxTokens_maximum = 32768
init_maxTokens_currentVal = 3000
topP_minimum = 0
topP_maximum = 1
init_topP_currentVal = 0.8
topP_singleStep = 0.01
temperature_minimum = 0.01
temperature_maximum = 1
init_temperature_currentVal = 0.8
temperature_singleStep = 0.01

windowFontSize = 22
textEditFullBGColor = QColor(224, 224, 224)
textEditFullBGTColor = QColor(224, 224, 224, 0)
textEditFullBColor = QColor(100, 100, 100)
textEditFullBTColor = QColor(100, 100, 100, 0)
fulBubbleColor = QColor(119, 221, 255)
userBubbleColor = QColor(16, 149, 222)
aiBubbleColor = QColor(17, 173, 222)

class messageThread(QThread):
    newMessage = pyqtSignal(str)

    def __init__(self, contentInput, context=None, use_stream=True, parent=None):
        super(messageThread, self).__init__(parent)
        #read setting config file
        with open(config_file_path, "r") as f:
            content = f.readlines()
        self.base_url = content[0].strip('\n')
        self.api_key = content[1].strip('\n')
        self.model = content[2].strip('\n')
        self.maxTokens_currentVal = int(content[3].strip('\n'))
        self.topP_currentVal = float(content[4].strip('\n'))
        self.temperature_currentVal = float(content[5].strip('\n'))
        #client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.text = [
            {
                "role": "user",
                "content": contentInput
            }
        ]
        if context:  
            self.text = context + self.text
        self.use_stream = use_stream

    def run(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.text,
            stream=self.use_stream,
            max_tokens=self.maxTokens_currentVal,
            temperature=self.temperature_currentVal,
            presence_penalty=1.1,
            top_p=self.topP_currentVal
        )
        if response:
            if self.use_stream:
                for chunk in response:
                    self.contentOutput = chunk.choices[0].delta.content
                    self.newMessage.emit(self.contentOutput)
            else:
                self.contentOutput = response.choices[0].message.content
                self.newMessage.emit(self.contentOutput)
        else:
            print("Error:", response.status_code)
        return
""" class messageThread(QThread):
    newMessage = pyqtSignal(str)

    def __init__(self, contentInput, context=None, use_stream=True, parent=None):
        super(messageThread, self).__init__(parent)
        self.text = [
            {
                "role": "user",
                "content": contentInput
            }
        ]
        self.use_stream = use_stream

    def run(self):
        self.contentOutput = '锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。\n'
        if self.use_stream:
            for i in range(0, 4):
                self.newMessage.emit(self.contentOutput)
                time.sleep(0.5)
        else:
            self.newMessage.emit(self.contentOutput)
        return """

class PushButton(QPushButton):
    def __init__(self, tipText='', tipOffsetX=10, tipOffsetY=40, parent=None):
        super(PushButton, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.tipText = tipText
        self.tipStartPos = QPoint(self.rect().topLeft().x() - tipOffsetX, self.rect().topLeft().y() - tipOffsetY)

    def mousePressEvent(self, event):
        QPushButton.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QPushButton.mouseReleaseEvent(self, event)
        event.ignore()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            font = QFont()
            font.setPixelSize(18)
            QToolTip.setFont(font)
            QToolTip.showText(self.mapToGlobal(self.tipStartPos), self.tipText, self)
        return QPushButton.event(self, event)

class FunWidget(QWidget):
    def __init__(self, parent=None):
        super(FunWidget, self).__init__(parent)
        #chatRecordsButton PushButton
        self.chatRecordsButton = PushButton(tipText='聊天历史', tipOffsetX=30, tipOffsetY=40)
        self.chatRecordsButton.setFixedSize(30, 30)
        self.chatRecordsButton.setIconSize(QSize(30, 30))
        self.chat_records_images_path = os.path.join(images_dir, 'chat_records.png').replace('\\', '/')
        self.chat_records_hover_images_path = os.path.join(images_dir, 'chat_records_hover.png').replace('\\', '/')
        self.chatRecordsButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url('{self.chat_records_images_path}');
        }}
        QPushButton:hover{{
            border-image: url('{self.chat_records_hover_images_path}');
        }}
        ''')
        #funLeftSubWidget QWidget
        self.funLeftSubWidget = Widget()
        self.funLeftSubWidget.resize(self.chatRecordsButton.width() + 15, self.chatRecordsButton.height() + 6)
        self.funLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #funLeftSubHLayout QHBoxLayout
        self.funLeftSubHLayout = QHBoxLayout()
        self.funLeftSubWidget.setLayout(self.funLeftSubHLayout)
        self.funLeftSubHLayout.addWidget(self.chatRecordsButton)
        self.funLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.funLeftSubHLayout.setContentsMargins(10, 3, 5, 3)
        #newChatButton PushButton
        self.newChatButton = PushButton(tipText='新聊天', tipOffsetX=20, tipOffsetY=40)
        self.newChatButton.setFixedSize(30, 30)
        self.newChatButton.setIconSize(QSize(30, 30))
        self.new_chat_images_path = os.path.join(images_dir, 'new_chat.png').replace('\\', '/')
        self.new_chat_hover_images_path = os.path.join(images_dir, 'new_chat_hover.png').replace('\\', '/')
        self.newChatButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.new_chat_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.new_chat_hover_images_path}");
        }}
        ''')
        #funRightSubWidget QWidget
        self.funRightSubWidget = Widget()
        self.funRightSubWidget.resize(self.newChatButton.width() + 15, self.newChatButton.height() + 6)
        self.funRightSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #funRightSubHLayout QHBoxLayout
        self.funRightSubHLayout = QHBoxLayout()
        self.funRightSubWidget.setLayout(self.funRightSubHLayout)
        self.funRightSubHLayout.addWidget(self.newChatButton)
        self.funRightSubHLayout.setAlignment(Qt.AlignRight)
        self.funRightSubHLayout.setContentsMargins(5, 3, 10, 3)
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.mainHLayout.addWidget(self.funLeftSubWidget)
        self.mainHLayout.addWidget(self.funRightSubWidget)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        #FunWidget adjust size
        self.resize(1200, 36)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def connectChatRecordsButtonClick(self, fun):
        self.chatRecordsButton.clicked.connect(fun)

    def connectNewChatButtonClick(self, fun):
        self.newChatButton.clicked.connect(fun)

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.resize(1171, 492)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet('''
        QListWidget{
            border: none;
            background: transparent;
        }
        QListWidget::item{
            background: transparent;
        }
        QListWidget::item:active{
            background: transparent;
        }
        QListWidget::item:selected{
            background: transparent;
        }
        QListWidget::item:hover{
            background: transparent;
        }
        QScrollBar{
            width: 25px;
        }
        ''')
        #setMouseTracking
        self.setMouseTracking(True)
        #verticalScrollBar
        self.verticalScrollBar().rangeChanged.connect(self.onScrollBarRangeChanged)
        self.verticalScrollBar().valueChanged.connect(self.onScrollBarValueChanged)
        self.scrollAutoChange=True
        self.scrollChangeUplimit = 200

    def onScrollBarRangeChanged(self, min, max):
        if self.scrollAutoChange:
            self.verticalScrollBar().setValue(max)

    def onScrollBarValueChanged(self, value):
        if self.verticalScrollBar().maximum() - self.verticalScrollBar().value() >= self.scrollChangeUplimit:
            self.scrollAutoChange = False
        else:
            self.scrollAutoChange = True

    def scrollTo(self, index, hint=QListWidget.EnsureVisible):
        # 重写方法，不执行任何滚动操作
        pass

    def mouseMoveEvent(self, event):
        QListWidget.mouseMoveEvent(self, event)
        event.ignore()

    def mousePressEvent(self, event):
        QListWidget.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QListWidget.mouseReleaseEvent(self, event)
        event.ignore()

class SendButton(QPushButton):
    def __init__(self, tipText='', tipOffsetX=10, tipOffsetY=40, parent=None):
        super(SendButton, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.tipText = tipText
        self.tipStartPos = QPoint(self.rect().topLeft().x() - tipOffsetX, self.rect().topLeft().y() - tipOffsetY)

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            font = QFont()
            font.setPixelSize(18)
            QToolTip.setFont(font)
            QToolTip.showText(self.mapToGlobal(self.tipStartPos), self.tipText, self)
        return QPushButton.event(self, event)

class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.resize(1130, 158)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setPlaceholderText("按Shift+Enter换行、按Enter提交")
        self.sendButton = SendButton(tipText='发送', tipOffsetX=10, tipOffsetY=40)
        self.sendButton.setFixedSize(30, 30)
        self.sendButton.setIconSize(QSize(30, 30))
        self.gLayout = QGridLayout()
        self.setLayout(self.gLayout)
        self.gLayout.setRowStretch(0, 1)
        self.gLayout.setColumnStretch(0, 1)
        self.gLayout.addWidget(self.sendButton, 1, 1)
        self.gLayout.setContentsMargins(10, 10, 25, 10)
        self.gLayout.setSpacing(0)
        self.textChanged.connect(self.sendButtonShow)
        self.send_images_path = os.path.join(images_dir, 'send.png').replace('\\', '/')
        self.send_hover_images_path = os.path.join(images_dir, 'send_hover.png').replace('\\', '/')
        self.send_disable_images_path = os.path.join(images_dir, 'send_disable.png').replace('\\', '/')
        self.sendButton.setStyleSheet(f'''
        QPushButton{{
            border: none;
            image: url("{self.send_images_path}");
        }}
        QPushButton:disabled{{
            border: none;
            image: url("{self.send_disable_images_path}");
        }}
        ''')
        self.setStyleSheet('''
        QTextEdit{
            border: none;
            background :transparent;
            font-size: 22px;
            selection-background-color: rgb(23, 171, 227);
        }
        QScrollBar{
            width: 25px;
        }
        ''')
        #setMouseTracking
        self.setMouseTracking(True)

    def contextMenuEvent(self, event):
        menu = CustomMenu(self)
        menu.setStyleSheet('''
        QMenu {
            background-color: lightblue;
            border: none;
            border-radius: 15px;
            padding: 5px;  /* 菜单内边距 */
        }
        ''')
        action1 = menu.addAction("剪切")
        action1.setShortcut("Ctrl+x")
        action1_images_path = os.path.join(images_dir, 'cut.png').replace('\\', '/')
        action1.setIcon(QIcon(f"{action1_images_path}"))
        action1.triggered.connect(lambda: self.cut())
        action2 = menu.addAction("复制")
        action2.setShortcut("Ctrl+c")
        action2_images_path = os.path.join(images_dir, 'menu_copy.png').replace('\\', '/')
        action2.setIcon(QIcon(f"{action2_images_path}"))
        action2.triggered.connect(lambda: self.copy())
        action3 = menu.addAction("粘贴")
        action3.setShortcut("Ctrl+v")
        action3_images_path = os.path.join(images_dir, 'paste.png').replace('\\', '/')
        action3.setIcon(QIcon(f"{action3_images_path}"))
        action3.triggered.connect(lambda: self.paste())
        menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event):
        QTextEdit.mouseMoveEvent(self, event)
        event.ignore()

    def mousePressEvent(self, event):
        QTextEdit.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QTextEdit.mouseReleaseEvent(self, event)
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if event.modifiers() == Qt.ShiftModifier:
                QTextEdit.keyPressEvent(self, event)
            else:
                self.emitSendButtonClicked()
                event.accept()
        elif event.key() == Qt.Key_Enter:
            self.emitSendButtonClicked()
            event.accept()
        else:
            QTextEdit.keyPressEvent(self, event)

    def connectSendButtonClick(self, fun):
        self.sendButton.clicked.connect(fun)

    def emitSendButtonClicked(self):
        self.sendButton.clicked.emit()

    def enableSendButton(self):
        self.sendButton.setEnabled(True)

    def disableSendButton(self):
        self.sendButton.setEnabled(False)

    def sendButtonIsEnable(self):
        return self.sendButton.isEnabled()

    def sendButtonShow(self):
        if self.toPlainText() == '':
            self.sendButton.setStyleSheet(f'''
            QPushButton{{
                border: none;
                image: url("{self.send_images_path}");
            }}
            QPushButton:disabled{{
                border: none;
                image: url("{self.send_disable_images_path}");
            }}
            ''')
        else:
            self.sendButton.setStyleSheet(f'''
            QPushButton{{
                border: none;
                image: url("{self.send_hover_images_path}");
            }}
            QPushButton:disabled{{
                border: none;
                image: url("{self.send_disable_images_path}");
            }}
            ''')

class TextEditFull(QWidget):
    def __init__(self, parent=None):
        super(TextEditFull, self).__init__(parent)
        self.setMinimumHeight(80)
        #TextEdit
        self.textEdit = TextEdit()
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.mainHLayout.addWidget(self.textEdit)
        self.mainHLayout.setContentsMargins(15, 15, 15, 15)
        #TextEditFull adjust size
        self.resize(self.textEdit.width() + 30, self.textEdit.height() + 30)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #background color
        self.BGColor = textEditFullBGColor
        #AnimationBackgroundColor QPropertyAnimation
        self.AnimationBackgroundColor = QPropertyAnimation(self, b'backgroundColor')
        self.AnimationBackgroundColor.setDuration(400)
        self.AnimationBackgroundColor.setEasingCurve(QEasingCurve.OutQuad)
        #border color
        self.BColor = textEditFullBTColor
        #AnimationBorderColor QPropertyAnimation
        self.AnimationBorderColor = QPropertyAnimation(self, b'borderColor')
        self.AnimationBorderColor.setDuration(400)
        self.AnimationBorderColor.setEasingCurve(QEasingCurve.OutQuad)
        #backgroundColorIsLight
        self.backgroundColorIsLight = False
        #setMouseTracking
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPen
        pen = QPen(self.BColor)
        painter.setPen(pen)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.BGColor)
        painter.setBrush(brush)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self.BGColor

    @backgroundColor.setter
    def backgroundColor(self, color):
        self.BGColor = color

    @pyqtProperty(QColor)
    def borderColor(self):
        return self.BColor

    @borderColor.setter
    def borderColor(self, color):
        self.BColor = color
        self.repaint()

    def backgroundColorShowLight(self):
        if not self.backgroundColorIsLight:
            self.backgroundColorIsLight = True
            self.AnimationBackgroundColor.setStartValue(textEditFullBGColor)
            self.AnimationBackgroundColor.setEndValue(textEditFullBGTColor)
            self.AnimationBackgroundColor.start()
            self.AnimationBorderColor.setStartValue(textEditFullBTColor)
            self.AnimationBorderColor.setEndValue(textEditFullBColor)
            self.AnimationBorderColor.start()

    def backgroundColorShowDark(self):
        if self.backgroundColorIsLight:
            self.backgroundColorIsLight = False
            self.AnimationBackgroundColor.setStartValue(textEditFullBGTColor)
            self.AnimationBackgroundColor.setEndValue(textEditFullBGColor)
            self.AnimationBackgroundColor.start()
            self.AnimationBorderColor.setStartValue(textEditFullBColor)
            self.AnimationBorderColor.setEndValue(textEditFullBTColor)
            self.AnimationBorderColor.start()

    def clearFocus(self):
        self.textEdit.clearFocus()

    def resetWidgetSize(self):
        self.textEdit.resize(self.width() - 30, self.height() - 30)

    def toPlainText(self):
        return self.textEdit.toPlainText()

    def clearText(self):
        self.textEdit.clear()

    def connectSendButtonClick(self, fun):
        self.textEdit.connectSendButtonClick(fun)

    def enableSendButton(self):
        self.textEdit.enableSendButton()

    def disableSendButton(self):
        self.textEdit.disableSendButton()

    def sendButtonIsEnable(self):
        return self.textEdit.sendButtonIsEnable()

class ImageLabel(QLabel):
    def __init__(self, isUser=True, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setFixedSize(32, 32)
        user_images_path = os.path.join(images_dir, 'user.png').replace('\\', '/')
        ai_images_path = os.path.join(images_dir, 'ai.png').replace('\\', '/')
        if isUser:
            self.setPixmap(QPixmap(f"{user_images_path}"))
        else:
            self.setPixmap(QPixmap(f"{ai_images_path}"))

class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(CustomWebEngineView, self).__init__(parent)
        self.windows = []

    def createWindow(self, _type):
        newView = CustomWebEngineView()
        newWindow= QMainWindow()
        newWindow.setCentralWidget(newView)
        newWindow.resize(1200, 800)
        newWindow.show()
        self.windows.append(newWindow)
        newWindow.destroyed.connect(lambda: self.windows.remove(newWindow))
        return newView

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        self.windows = []

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        # 打开新窗口并加载 URL  
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            newView = CustomWebEngineView()
            newView.setUrl(url)
            newWindow= QMainWindow()
            newWindow.setCentralWidget(newView)
            newWindow.resize(1200, 800)
            newWindow.destroyed.connect(lambda: self.windows.remove(newWindow))
            newWindow.show()
            self.windows.append(newWindow)
            return False  # 阻止当前的 QWebEngineView 跳转
        return True  # 处理其它导航请求

class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.setPage(WebEnginePage(self))  # 将自定义页面设置给视图
        self.page().setBackgroundColor(Qt.transparent)
        self.load(QUrl())
        self.focusProxy().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.focusProxy() and  event.type() == QEvent.MouseButtonRelease:
            newMouseEvent = QMouseEvent(event.type(), event.pos(), event.button(), event.buttons(), event.modifiers())
            QCoreApplication.postEvent(obj.parent(), newMouseEvent)
        return QWebEngineView.eventFilter(self, obj, event)

    def connectPageLoadFinished(self, fun):
        self.page().loadFinished.connect(fun)

    def contextMenuEvent(self, event):
        # 忽略右键上下文菜单事件
        event.ignore()

    def wheelEvent(self, event):
        # 获取滚动的像素值
        delta_y = event.angleDelta().y()
        # 获取当前的垂直滚动位置
        current_scroll_value = self.parent().parent().parent().listWidget.verticalScrollBar().value()
        min_scroll_value = self.parent().parent().parent().listWidget.verticalScrollBar().minimum()
        max_scroll_value = self.parent().parent().parent().listWidget.verticalScrollBar().maximum()
        # 计算新的滚动位置
        new_scroll_value = current_scroll_value - delta_y * 3
        if new_scroll_value < min_scroll_value:
            new_scroll_value = min_scroll_value
        elif new_scroll_value > max_scroll_value:
            new_scroll_value = max_scroll_value
        # 设置新的滚动位置
        self.parent().parent().parent().listWidget.verticalScrollBar().setValue(new_scroll_value)
        # 需要调用 accept() 来防止事件传递
        event.accept()

class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        QLabel.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QLabel.mouseReleaseEvent(self, event)
        event.ignore()

    def contextMenuEvent(self, event):
        # 忽略右键上下文菜单事件
        event.ignore()

class TextShow(QWidget):
    setSizeFinished = pyqtSignal()
    setTexting = pyqtSignal(bool)

    def __init__(self, text, isUser=True, maxWidth=650, parent=None):
        super(TextShow, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = CustomLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        self.font.setPixelSize(windowFontSize)
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)
        self.mainHLayout = QHBoxLayout()
        self.webEngineView = WebEngineView()
        self.webEngineView.connectPageLoadFinished(self.onPageLoadFinished)
        self.isLabel = True
        if not self.text == '':
            textWidth = 0
            textHeight = int(self.font_metrics.height())
            count = self.text.count('\n')
            textList = self.text.split('\n', count)
            maxTempTextWidth = 0
            for i in range(0, count + 1):
                if int(self.font_metrics.width(textList[i])) > maxTempTextWidth:
                    maxTempTextWidth = int(self.font_metrics.width(textList[i]))
            if (maxTempTextWidth + 4) < self.maxWidth:
                labelWidth = maxTempTextWidth + 4
                labelHeight = (count + 1) * (textHeight + 3) - 3
            else:
                for i in range(0, count + 1):
                    if i != count:
                        tempTextWidth = self.font_metrics.width(textList[i] + ' ')
                        tempTextWidth = math.ceil(tempTextWidth / (self.maxWidth - 24)) * (self.maxWidth - 24)
                    else:
                        tempTextWidth = self.font_metrics.width(textList[i])
                    textWidth += int(tempTextWidth)
                labelWidth = self.maxWidth
                labelHeight = int(math.ceil(textWidth / (self.maxWidth - 24)) * (textHeight + 3) - 3)
            self.label.setText(self.text)
            self.label.setFixedSize(labelWidth, labelHeight)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(labelWidth + 10, labelHeight + 10)
        else:
            self.label.setFixedSize(windowFontSize, windowFontSize)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(windowFontSize + 10, windowFontSize + 10)
        self.isUser = isUser
        self.isColorful = False

    def onPageLoadFinished(self, success):
        js = """
        function getPageHeight() {
            var body = document.body;
            var html = document.documentElement;
            var width = Math.max(body.scrollWidth, body.offsetWidth,
                                html.clientWidth, html.scrollWidth, html.offsetWidth);
            var height = Math.max(body.scrollHeight, body.offsetHeight,
                                html.clientHeight, html.scrollHeight, html.offsetHeight);
            var content = document.querySelector('.content');
            if (content) {
                width = content.offsetWidth;
                height = content.offsetHeight;
            }
            return [width, height];
        }
        getPageHeight();
        """
        if success:
            self.webEngineView.page().runJavaScript("document.body.style.overflow = 'hidden';")
            self.webEngineView.page().runJavaScript(js, self.updateSize)

    def updateSize(self, result):
        width, height = result
        if width != 0 and height != 0:
            self.webEngineView.setFixedSize(width, height)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            self.setSizeFinished.emit()

    def getAlignmentClass(self, format_string):
        # 根据对齐格式返回相应的class名
        if ':-' in format_string and '-:' in format_string:
            return 'center-align'  # 居中对齐
        elif ':-' in format_string:
            return 'left-align'   # 左对齐
        elif '-:' in format_string:  
            return 'right-align'  # 右对齐
        else:  
            return ''

    def getTable(self, text):
        tableText = ''
        tableItemList = []
        tableItemList1 = []
        tableAlignList = []
        i = 0
        r = 0
        row = 0
        row_full = 0
        column = 0
        tableIsComplete = False
        while(i < len(text)):
            if text[i] == '|':
                tableText += '|'
                j = i
                k = j + 1
                while(k < len(text)):
                    if text[k] == '|':
                        tableText += text[j + 1 : k] + '|'
                        tableItemList.append(text[j + 1 : k].strip(' '))
                        j = k
                    k += 1
                break
            i += 1
        for index, tableItem in enumerate(tableItemList):
            if '\n' in tableItem:
                row_full += 1
            else:
                if row_full == 0:
                    column += 1
                if index == len(tableItemList) - 1:
                    row_full += 1
        if row_full > 1:
            row = row_full - 1
        else:
            row = row_full
        if row >= 1:
            tableItemList1 = tableItemList1 + tableItemList[0 : column]
        if row_full >= 2:
            tableAlignList = tableItemList[column + 1 : 2 * (column + 1) - 1]
        if row >= 2:
            for r in range(1, row):
                tableItemList1 = tableItemList1 + tableItemList[(r + 1) * (column + 1) : (r + 2) * (column + 1) - 1]
            if '\n' in tableItemList[-1]:
                if len(tableItemList) == row_full * (column + 1):
                    tableIsComplete = True
            else:
                if len(tableItemList) == row_full * (column + 1) - 1:
                    tableIsComplete = True
        return tableText, tableItemList1, tableAlignList, row, column, tableIsComplete

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        if self.isColorful:
            brush.setColor(fulBubbleColor)
        else:
            if self.isUser:
                brush.setColor(userBubbleColor)
            else:
                brush.setColor(aiBubbleColor)
        #add rect and set brush
        if self.isUser:
            path.addRect(self.rect().width() - 15, self.rect().y(), 15, 15)
        else:
            path.addRect(self.rect().x(), self.rect().y(), 15, 15)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def htmlReplaceText(self, text):
        markdown_content = text.replace('\$', '\\\$')
        markdown_content = markdown_content.replace('\frac', '\\frac')
        markdown_content = markdown_content.replace('\,', '\\\,')
        markdown_content = markdown_content.replace('\alpha', '\\alpha')
        markdown_content = markdown_content.replace('\beta', '\\beta')
        markdown_content = markdown_content.replace('\theta', '\\theta')
        markdown_content = markdown_content.replace('\nu', '\\nu')
        markdown_content = markdown_content.replace('\rho', '\\rho')
        markdown_content = markdown_content.replace('\tau', '\\tau')
        return markdown_content

    def toggleWidget(self):
        markdown_content = ''
        self.html_text = ''
        self.full_html_text = ''
        initWidth = self.font_metrics.width(self.text) + 16
        if initWidth > self.maxWidth:
            self.webEngineView.setFixedWidth(self.maxWidth)
        else:
            if self.text == '':
                self.webEngineView.setFixedSize(38, 73)
            else:
                self.webEngineView.setFixedWidth(int(initWidth))
        # 添加 MathJax CDN 链接到 HTML 头部
        self.mathjax_cdn = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script type="text/javascript">
                    MathJax = {{
                        options: {{
                            enableMenu: false
                        }},
                        tex: {{
                            inlineMath: [["$", "$"], ["\\(", "\\)"]],
                            displayMath: [["$$", "$$"], ["\\[", "\\]"]]
                        }},
                        svg: {{
                            fontCache: 'global'
                        }}
                    }};
                </script>
                <script type="text/javascript"
                    src="{mathjax_script_path}">
                </script>
                <style>
                    table {{
                        width: 50%;
                        border-collapse: collapse;
                        margin: 10px 0;
                    }}  
                    th, td {{
                        border: 1px solid #000;
                        padding: 8px;
                    }}
                    th {{
                        background-color: #b0b0b0;
                    }}
                    .left-align {{ text-align: left; }}
                    .center-align {{ text-align: center; }}
                    .right-align {{ text-align: right; }}
                </style>
                <style>
                    body, html {{
                        margin: 0;
                        padding: 0;
                        width: 100%;
                        height: 100%;
                        box-sizing: border-box;
                        font-size: 22px;
                    }}
                    .content {{
                        width: auto;
                        height: auto;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    }}
                </style>
            </head>
        """
        self.markdown = mistune.create_markdown(escape=False, renderer='html')
        if not self.text == '':
            tableText, tableItemList, tableAlignList, row, column, tableIsComplete= self.getTable(self.text)
            if tableIsComplete:
                textList = self.text.split(tableText, 1)
                markdown_content = self.htmlReplaceText(textList[0])
                # 使用 mistune 将 Markdown 转换为 HTML
                self.html_text = self.markdown(markdown_content)
                self.html_text += """
                    <table>
                        <thead>
                            <tr>
                """
                # 添加表头  
                for i in range(column):
                    self.html_text += f"<th class='{self.getAlignmentClass(tableAlignList[i])}'>{tableItemList[i]}</th>"
                self.html_text += """
                            </tr>
                        </thead>
                        <tbody>
                """
                # 添加数据行
                for i in range(1, row):
                    self.html_text += "<tr>"
                    for j in range(column):
                        self.html_text += f"<td class='{self.getAlignmentClass(tableAlignList[j])}'>{tableItemList[i * column + j]}</td>"
                    self.html_text += "</tr>"
                self.html_text += """
                        </tbody>
                    </table>
                """
                markdown_content = self.htmlReplaceText(textList[1])
                # 使用 mistune 将 Markdown 转换为 HTML
                self.html_text += self.markdown(markdown_content)
            else:
                markdown_content = self.htmlReplaceText(self.text)
                # 使用 mistune 将 Markdown 转换为 HTML
                self.html_text = self.markdown(markdown_content)
            # 将转换后的 HTML 内容添加到 body 中
            self.full_html_text = f"{self.mathjax_cdn}<body>\n<div class='content'>\n{self.html_text}\n</div>\n</body>\n</html>\n"
            baseUrl = QUrl.fromLocalFile(os.path.dirname(os.path.abspath(__file__)) + '/')
            if self.isLabel:
                self.mainHLayout.removeWidget(self.label)
                self.label.deleteLater()
                self.mainHLayout.addWidget(self.webEngineView)
            self.webEngineView.setHtml(str(self.full_html_text), baseUrl)
            self.isLabel = False
            self.setTexting.emit(self.isLabel)
        else:
            if self.isLabel:
                self.mainHLayout.removeWidget(self.label)
                self.label.deleteLater()
                self.mainHLayout.addWidget(self.webEngineView)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            self.setSizeFinished.emit()
            self.isLabel = False
            self.setTexting.emit(self.isLabel)

    def setText(self, text):
        self.setTexting.emit(self.isLabel)
        self.text = text.strip('\n')
        if not self.text == '':
            textWidth = 0
            textHeight = int(self.font_metrics.height())
            count = self.text.count('\n')
            textList = self.text.split('\n', count)
            maxTempTextWidth = 0
            for i in range(0, count + 1):
                if int(self.font_metrics.width(textList[i])) > maxTempTextWidth:
                    maxTempTextWidth = int(self.font_metrics.width(textList[i]))
            if (maxTempTextWidth + 4) < self.maxWidth:
                labelWidth = maxTempTextWidth + 4
                labelHeight = (count + 1) * (textHeight + 3) - 3
            else:
                for i in range(0, count + 1):
                    if i != count:
                        tempTextWidth = self.font_metrics.width(textList[i] + ' ')
                        tempTextWidth = math.ceil(tempTextWidth / (self.maxWidth - 24)) * (self.maxWidth - 24)
                    else:
                        tempTextWidth = self.font_metrics.width(textList[i])
                    textWidth += int(tempTextWidth)
                labelWidth = self.maxWidth
                labelHeight = int(math.ceil(textWidth / (self.maxWidth - 24)) * (textHeight + 3) - 3)
            self.label.setText(self.text)
            self.label.setFixedSize(labelWidth, labelHeight)
            self.setFixedSize(labelWidth + 10, labelHeight + 10)
        else:
            self.label.setFixedSize(windowFontSize, windowFontSize)
            self.setFixedSize(windowFontSize + 10, windowFontSize + 10)

    def connectSetTexting(self, fun):
        self.setTexting.connect(fun)

    def getWebEngineView(self):
        return self.webEngineView

    def hasSelectedText(self):
        if self.isLabel:
            return self.label.hasSelectedText()
        else:
            return self.webEngineView.hasSelection()

    def getSelectedText(self):
        if self.isLabel:
            return self.label.selectedText()
        else:
            return self.webEngineView.selectedText()

class TextWidget(QWidget):
    def __init__(self, parent=None):
        super(TextWidget, self).__init__(parent)
        self.setMouseTracking(True)

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super(LoadingWidget, self).__init__(parent)
        self.setFixedSize(68, 26)
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.subWidgetList = []
        for _ in range(3):
            subWidget = QWidget()
            subWidget.setFixedSize(16, 16)
            self.mainHLayout.addWidget(subWidget)
            self.subWidgetList.append(subWidget)
        self.mainHLayout.setContentsMargins(5, 5, 5, 5)
        self.mainHLayout.setSpacing(5)
        #QTimer
        self.loadingTimer = QTimer(self)
        self.loadingTimer.timeout.connect(self.loadingShow)
        self.loadingTimer.start(400)
        self.loadingNum = 0

    def loadingShow(self):
        for subWidget in self.subWidgetList:
            subWidget.setStyleSheet('''
                border: none;
                border-radius: 8px;
                background-color: rgb(150, 150, 150);
            ''')
        self.subWidgetList[self.loadingNum].setStyleSheet('''
            border: none;
            border-radius: 8px;
            background-color: rgb(80, 80, 80);
        ''')
        self.loadingNum = (self.loadingNum + 1) % 3

class CopyButton(QPushButton):
    def __init__(self, tipText='', tipOffsetX=10, tipOffsetY=40, parent=None):
        super(CopyButton, self).__init__(parent)
        self.parent = parent
        self.setCursor(Qt.PointingHandCursor)
        #QClipboard
        self.clip = QApplication.clipboard()
        #QToolTip
        self.tipText = tipText
        self.tipStartPos = QPoint(self.rect().topLeft().x() - tipOffsetX, self.rect().topLeft().y() - tipOffsetY)

    def mousePressEvent(self, event):
        if self.parent.hasSelectedText():
            self.clip.setText(self.parent.getSelectedText())
        else:
            self.clip.setText(self.parent.getText())
        QPushButton.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QPushButton.mouseReleaseEvent(self, event)
        event.ignore()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            font = QFont()
            font.setPixelSize(18)
            QToolTip.setFont(font)
            QToolTip.showText(self.mapToGlobal(self.tipStartPos), self.tipText, self)
        return QPushButton.event(self, event)

class MessageWidget(QWidget):
    def __init__(self, text, copyFun, renewResponseFun, listWidget, isUser=True, textMaxWidth=780, parent=None):
        super(MessageWidget, self).__init__(parent)
        self.listWidget = listWidget
        self.text = text
        self.textMaxWidth = textMaxWidth
        self.isUser = isUser
        #ImageLabel
        self.imageLabel = ImageLabel(isUser=self.isUser)
        #TextShow
        self.textShow = TextShow(text, isUser=self.isUser, maxWidth=textMaxWidth)
        #loadingWidgetIsRemove
        self.loadingWidgetIsRemove = True
        #renewResponseButtonIsRemove
        self.renewResponseButtonIsRemove = True
        #textWidget QWidget
        self.textWidget = TextWidget()
        #textLayout QHBoxLayout
        self.textLayout = QVBoxLayout()
        self.textWidget.setLayout(self.textLayout)
        self.textLayout.addWidget(self.textShow)
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        #subVLayout QVBoxLayout
        self.subVLayout1 = QVBoxLayout()
        self.subVLayout1.setAlignment(Qt.AlignTop)
        self.subVLayout1.setContentsMargins(0, 0, 0, 0)
        self.subVLayout2 = QVBoxLayout()
        self.subVLayout2.setAlignment(Qt.AlignTop)
        self.subVLayout2.setContentsMargins(0, 0, 0, 0)
        #CopyButton
        self.copyButton = CopyButton(tipText='复制', tipOffsetX=15, tipOffsetY=40, parent=self)
        self.copyButton.setFixedSize(16, 16)
        self.copy_images_path = os.path.join(images_dir, 'copy.png').replace('\\', '/')
        self.copy_hover_images_path = os.path.join(images_dir, 'copy_hover.png').replace('\\', '/')
        self.copyButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.copy_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.copy_hover_images_path}");
        }}
        ''')
        self.copyButton.clicked.connect(copyFun)
        #renewResponseButton PushButton
        self.renewResponseButton = PushButton(tipText='重新生成响应', tipOffsetX=50, tipOffsetY=40)
        self.renewResponseButton.setFixedSize(16, 16)
        self.renew_response_images_path = os.path.join(images_dir, 'renewResponse.png').replace('\\', '/')
        self.renew_response_hover_images_path = os.path.join(images_dir, 'renewResponse_hover.png').replace('\\', '/')
        self.renewResponseButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.renew_response_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.renew_response_hover_images_path}");
        }}
        ''')
        self.renewResponseButton.clicked.connect(renewResponseFun)
        #funWidget QWidget
        self.funWidget = QWidget()
        #funHLayout QHBoxLayout
        self.funHLayout = QHBoxLayout()
        self.funWidget.setLayout(self.funHLayout)
        self.funHLayout.addWidget(self.copyButton)
        self.copyButton.hide()
        self.funHLayout.setContentsMargins(5, 5, 5, 5)
        if self.isUser:
            self.funWidget.setFixedSize(26, 26)
        else:
            self.funHLayout.addWidget(self.renewResponseButton)
            self.renewResponseButton.hide()
            self.funHLayout.setSpacing(10)
            self.funWidget.setFixedSize(52, 26)
            #renewResponseButtonIsRemove
            self.renewResponseButtonIsRemove = False
        #funWidgetIsShow
        self.funWidgetIsShow = False
        #setMouseTracking
        self.setMouseTracking(True)
        #add imageLabel and textWidget
        if self.isUser:
            self.textLayout.addWidget(self.funWidget)
            self.textLayout.setSpacing(0)
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            self.subVLayout1.addWidget(self.textWidget)
            self.subVLayout2.addWidget(self.imageLabel)
        else:
            self.subVLayout1.addWidget(self.imageLabel)
            self.loadingWidget = LoadingWidget()
            self.textLayout.addWidget(self.loadingWidget)
            self.textLayout.setSpacing(0)
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height())
            self.subVLayout2.addWidget(self.textWidget)
            #loadingWidgetIsRemove
            self.loadingWidgetIsRemove = False
        #mainHLayout add subVLayout
        self.mainHLayout.addLayout(self.subVLayout1)
        self.mainHLayout.addLayout(self.subVLayout2)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.setSpacing(5)
        #main widget set size
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def connectSetTexting(self, fun):
        self.textShow.connectSetTexting(fun)

    def toggleWidget(self):
        self.textShow.toggleWidget()

    def connectSetSizeFinished(self, fun):
        self.textShow.setSizeFinished.connect(fun)

    def setSize(self):
        if self.isUser:
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
        else:
            if self.loadingWidgetIsRemove:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            else:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def setText(self, text):
        self.text = text
        self.textShow.setText(self.text)
        if self.isUser:
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
        else:
            if self.loadingWidgetIsRemove:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            else:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def getText(self):
        return self.text

    def getIsUser(self):
        return self.isUser

    def getTextShow(self):
        return self.textShow

    def getTextWidget(self):
        return self.textWidget

    def getCopyButton(self):
        return self.copyButton

    def removeLoadingWidget(self):
        if not self.isUser and not self.loadingWidgetIsRemove:
            self.textLayout.removeWidget(self.loadingWidget)
            self.loadingWidget.deleteLater()
            self.loadingWidgetIsRemove = True
            self.textLayout.addWidget(self.funWidget)
            self.textLayout.setSpacing(0)
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def showFunWidget(self):
        if not self.funWidgetIsShow:
            if self.loadingWidgetIsRemove:
                self.copyButton.show()
                if not self.renewResponseButtonIsRemove:
                    self.renewResponseButton.show()
                self.funWidgetIsShow = True

    def hideFunWidget(self):
        if self.funWidgetIsShow:
            self.copyButton.hide()
            if not self.renewResponseButtonIsRemove:
                self.renewResponseButton.hide()
            self.funWidgetIsShow = False

    def removeRenewResponseButton(self):
        if not self.isUser and not self.renewResponseButtonIsRemove:
            self.funHLayout.removeWidget(self.renewResponseButton)
            self.renewResponseButton.deleteLater()
            self.renewResponseButtonIsRemove = True
            self.funWidget.setFixedSize(26, 26)

    def hasSelectedText(self):
        return self.textShow.hasSelectedText()

    def getSelectedText(self):
        return self.textShow.getSelectedText()

    def showColorful(self):
        self.textShow.isColorful = True
        self.textShow.repaint()

    def showDefaultColor(self):
        self.textShow.isColorful = False
        self.textShow.repaint()

class ItemWidget(QWidget):
    def __init__(self, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.setMouseTracking(True)

class PrintLabel(QWidget):
    def __init__(self, text, parent=None):
        super(PrintLabel, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = QLabel()
        self.font = QFont()
        self.font.setPixelSize(windowFontSize)
        self.font.setBold(True)
        self.label.setFont(self.font)
        self.palette = self.label.palette()
        self.palette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.label.setPalette(self.palette)
        self.label.setAlignment(Qt.AlignCenter)
        self.mainHLayout = QHBoxLayout()
        if not self.text == '':
            self.label.setText(self.text)
            self.label.adjustSize()
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(self.label.width() + 10, self.label.height() + 10)
        else:
            self.label.resize(windowFontSize, windowFontSize)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(windowFontSize + 10, windowFontSize + 10)
        #printTimer QTimer
        self.printTimer = QTimer(self)
        self.printTimer.timeout.connect(self.printEnd)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.white)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def setText(self, text):
        self.text = text.strip('\n')
        if not self.text == '':
            self.label.setText(self.text)
            self.label.adjustSize()
            self.setFixedSize(self.label.width() + 10, self.label.height() + 10)
        else:
            self.label.resize(windowFontSize, windowFontSize)
            self.setFixedSize(windowFontSize + 10, windowFontSize + 10)

    def printStart(self):
        #show PrintLabel
        self.show()
        #start printTimer
        self.printTimer.start(2000)

    def printEnd(self):
        #stop printTimer
        self.printTimer.stop()
        #hide PrintLabel
        self.hide()

class Label(QLabel):
    def __init__(self, parent=None):
        super(Label, self).__init__(parent)
        self.setFixedHeight(32)
        self.font = QFont()
        self.font.setPixelSize(windowFontSize)
        self.font.setBold(True)
        self.setFont(self.font)
        self.palette = self.palette()
        self.palette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.setPalette(self.palette)

class SettingEdit(QLineEdit):
    def __init__(self, parent=None):
        super(SettingEdit, self).__init__(parent)
        self.setFixedHeight(32)
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, 10)
                self.setFont(self.font)

class SpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(SpinBox, self).__init__(parent)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        up_arrow_images_path = os.path.join(images_dir, 'up_arrow.png').replace('\\', '/')
        down_arrow_images_path = os.path.join(images_dir, 'down_arrow.png').replace('\\', '/')
        self.setStyleSheet(f'''
        QSpinBox{{
            border: 2px solid rgb(23, 171, 227);
            border-radius: 8px;
            background: transparent;
            font: 22px, bold;
            color: rgb(23, 171, 227);
            selection-background-color: rgb(23, 171, 227);
        }}
        QSpinBox::up-button{{
            width: 16px;
            height: 16px;
            border-image: url("{up_arrow_images_path}");
        }}
        QSpinBox::up-button:pressed{{
            margin-top: 1px;
        }}
        QSpinBox::down-button{{
            width: 16px;
            height: 16px;
            border-image: url("{down_arrow_images_path}");
        }}
        QSpinBox::down-button:pressed{{
            margin-bottom: 1px;
        }}
        ''')

    def mousePressEvent(self, event):
        QSpinBox.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QSpinBox.mouseReleaseEvent(self, event)
        event.ignore()

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        up_arrow_images_path = os.path.join(images_dir, 'up_arrow.png').replace('\\', '/')
        down_arrow_images_path = os.path.join(images_dir, 'down_arrow.png').replace('\\', '/')
        self.setStyleSheet(f'''
        QDoubleSpinBox{{
            border: 2px solid rgb(23, 171, 227);
            border-radius: 8px;
            background: transparent;
            font: 22px, bold;
            color: rgb(23, 171, 227);
            selection-background-color: rgb(23, 171, 227);
        }}
        QDoubleSpinBox::up-button{{
            width: 16px;
            height: 16px;
            border-image: url("{up_arrow_images_path}");
        }}
        QDoubleSpinBox::up-button:pressed{{
            margin-top: 1px;
        }}
        QDoubleSpinBox::down-button{{
            width: 16px;
            height: 16px;
            border-image: url("{down_arrow_images_path}");
        }}
        QDoubleSpinBox::down-button:pressed{{
            margin-bottom: 1px;
        }}
        ''')

    def mousePressEvent(self, event):
        QDoubleSpinBox.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QDoubleSpinBox.mouseReleaseEvent(self, event)
        event.ignore()

class Slider(QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.setFixedHeight(26)
        self.setOrientation(Qt.Horizontal)
        self.setStyleSheet('''
        QSlider::groove:horizontal{
            height: 8px;
            border-radius: 4px;
            background-color: rgb(150, 150, 150);
        }
        QSlider::handle:horizontal{
            width: 26px;
            margin: -9px 0px -9px 0px;
            border-radius: 13px;
            background-color: rgb(80, 80, 80);
        }
        QSlider::handle:hover:horizontal{
            background-color: rgb(100, 100, 100);
        }
        QSlider::sub-page:horizontal{
            border-radius: 4px;
            background-color: rgb(23, 171, 227);
        }
        ''')

    def mousePressEvent(self, event):
        QSlider.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QSlider.mouseReleaseEvent(self, event)
        event.ignore()

class LineEdit(QLineEdit):
    def __init__(self):
        super(LineEdit, self).__init__()
        self.setFixedSize(1200 // 3 - 80, 30)
        self.setPlaceholderText("输入搜索词")
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, 10)
                self.setFont(self.font)
        #searchButton QPushButton
        self.searchButton = PushButton(tipText='搜索', tipOffsetX=10, tipOffsetY=40, parent=self)
        self.searchButton.setFixedSize(30, 30)
        self.search_images_path = os.path.join(images_dir, 'search.png').replace('\\', '/')
        self.searchButton.setIcon(QIcon(f"{self.search_images_path}"))
        self.searchButton.setIconSize(QSize(30, 30))
        self.searchButton.move(0, 0)
        #LineEdit
        self.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QLineEdit{
            border: none;
            border-radius: 5px;
            background: #b8b8b8;
            self.padding-left: 30px;
        }
        ''')

    def connectSearchButtonClick(self, fun):
        self.searchButton.clicked.connect(fun)

class ChatRecordsWidget(QWidget):
    def __init__(self, parent=None):
        super(ChatRecordsWidget, self).__init__(parent)
        self.resize(1200 // 3, 764)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, 10)
        #QLabel
        self.label = QLabel()
        self.label.resize(self.width() - 70, 50)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        font = QFont()
        font.setPixelSize(30)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setText("聊天历史")
        self.label.setAlignment(Qt.AlignLeft)
        #settingButton PushButton
        self.settingButton = PushButton(tipText='设置', tipOffsetX=10, tipOffsetY=40)
        self.settingButton.setFixedSize(30, 30)
        self.settingButton.setIconSize(QSize(30, 30))
        self.setting_images_path = os.path.join(images_dir, 'setting.png').replace('\\', '/')
        self.setting_hover_images_path = os.path.join(images_dir, 'setting_hover.png').replace('\\', '/')
        self.settingButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.setting_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.setting_hover_images_path}");
        }}
        ''')
        #buttonWidget QWidget
        self.buttonWidget = Widget()
        self.buttonWidget.resize(30, 50)
        self.buttonWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #buttonVLayout QVBoxLayout
        self.buttonVLayout = QVBoxLayout()
        self.buttonWidget.setLayout(self.buttonVLayout)
        self.buttonVLayout.addWidget(self.settingButton)
        self.buttonVLayout.setAlignment(Qt.AlignTop)
        self.buttonVLayout.setContentsMargins(0, 0, 0, 20)
        #headWidget QWidget
        self.headWidget = Widget()
        self.headWidget.resize(self.width() - 40, 50)
        self.headWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #headHLayout QHBoxLayout
        self.headHLayout = QHBoxLayout()
        self.headWidget.setLayout(self.headHLayout)
        self.headHLayout.addWidget(self.label)
        self.headHLayout.addWidget(self.buttonWidget)
        self.headHLayout.setContentsMargins(0, 0, 0, 0)
        self.headHLayout.setStretch(0, 1)
        self.headHLayout.setStretch(1, 0)
        #LineEdit
        self.lineEdit = LineEdit()
        #clearAllButton QPushButton
        self.clearAllButton = PushButton(tipText='删除所有记录', tipOffsetX=50, tipOffsetY=40)
        self.clearAllButton.setFixedSize(30, 30)
        self.clearAllButton.setIconSize(QSize(30, 30))
        self.clear_all_images_path = os.path.join(images_dir, 'clearAll.png').replace('\\', '/')
        self.clear_all_hover_images_path = os.path.join(images_dir, 'clearAll_hover.png').replace('\\', '/')
        self.clearAllButton.setStyleSheet(f'''
        QPushButton{{
            border: none;
            border-radius: 5px;
            background: #e0e0e0;
            image: url("{self.clear_all_images_path}");
        }}
        QPushButton:hover{{
            background: #b8b8b8;
            image: url("{self.clear_all_hover_images_path}");
        }}
        ''')
        #searchWidget QWidget
        self.searchWidget = QWidget()
        self.searchWidget.resize(self.width() - 40, 30)
        self.searchWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #searchHLayout QHBoxLayout
        self.searchHLayout = QHBoxLayout()
        self.searchWidget.setLayout(self.searchHLayout)
        self.searchHLayout.addWidget(self.lineEdit)
        self.searchHLayout.addWidget(self.clearAllButton)
        self.searchHLayout.setContentsMargins(0, 0, 0, 0)
        self.searchHLayout.setSpacing(10)
        self.searchHLayout.setStretch(0, 1)
        self.searchHLayout.setStretch(1, 0)
        #QListWidget
        self.listWidget = QListWidget()
        self.listWidget.setFixedSize(self.width() - 40, self.height() - 110)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget.setStyleSheet('''
        QListWidget{
            border: none;
            background: transparent;
        }
        QScrollBar{
            width: 20px;
        }
        ''')
        #mainWidget QWidget
        self.mainWidget = Widget(self)
        self.mainWidget.resize(1200 // 3, 764)
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.headWidget)
        self.mainVLayout.addWidget(self.searchWidget)
        self.mainVLayout.addWidget(self.listWidget)
        self.mainVLayout.setContentsMargins(20, 10, 20, 0)
        self.mainVLayout.setSpacing(10)
        self.mainVLayout.setStretch(0, 0)
        self.mainVLayout.setStretch(1, 0)
        self.mainVLayout.setStretch(2, 1)
        #setMouseTracking
        self.setMouseTracking(True)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(208, 208, 208))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

    def connectSettingButtonClick(self, fun):
        self.settingButton.clicked.connect(fun)

    def connectLineEditTextChanged(self, fun):
        self.lineEdit.textChanged.connect(fun)

    def connectSearchButtonClick(self, fun):
        self.lineEdit.connectSearchButtonClick(fun)

    def connectClearAllButtonClick(self, fun):
        self.clearAllButton.clicked.connect(fun)

    def connectListItemClick(self, fun):
        self.listWidget.itemClicked.connect(fun)

    def resetWidgetSize(self, width, height):
        self.lineEdit.setFixedSize(width - 80, 30)
        self.listWidget.setFixedSize(width - 40, height - 110)
        self.mainWidget.resize(width, height)
        self.resize(width, height)

    def getLineEditText(self):
        return self.lineEdit.text()

    def addListItem(self, string):
        self.chatRecordItem = QListWidgetItem(string)
        self.listWidget.insertItem(0, self.chatRecordItem)
        self.chatRecordItem.setSizeHint(QSize(self.listWidget.width(), 60))
        self.chatRecordItem.setFont(self.font)
        return self.chatRecordItem

    def delAllListItems(self):
        return self.listWidget.clear()

    def listItemSetData(self, item, string):
        item.setData(Qt.UserRole, QVariant(string))

    def listItemToString(self, item):
        return item.data(Qt.UserRole)

class SettingWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(208, 208, 208))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

class TitleWidget(QWidget):
    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 16, 16)
        path.addRect(self.rect().x(), self.rect().height() - 16, 16, 16)
        path.addRect(self.rect().width() - 16, self.rect().height() - 16, 16, 16)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(60, 60, 60))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

class Frame(QFrame):
    def __init__(self, parent=None):
        super(Frame, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QWidget.mouseMoveEvent(self, event)
        event.ignore()

class Splitter(QSplitter):
    def __init__(self, parent=None):
        super(Splitter, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QSplitter.mouseMoveEvent(self, event)
        event.ignore()

class RegionEnum(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    LEFTTOP = 4
    RIGHTTOP = 5
    LEFTBOTTOM = 6
    RIGHTBOTTOM = 7
    TITLE = 8
    BUTTON = 9
    MIDDLE = 10

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setMinimumSize(624, 416)
        self.resize(1220, 820)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.setMouseTracking(True)
        #mouseLeftButtonIsPress
        self.mouseLeftButtonIsPress = False
        #RegionEnum
        self.regionDir = RegionEnum.MIDDLE
        #padding
        self.padding = 2
        #title QWidget init
        self.titleWidgetInit()
        #FunWidget
        self.chatFun = FunWidget()
        self.chatFun.connectChatRecordsButtonClick(self.showChatRecords)
        self.chatFun.connectNewChatButtonClick(self.newChat)
        #ListWidget
        self.chatShow = ListWidget()
        self.chatShow.itemClicked.connect(self.itemShowColorful)
        #chatShowWidget QWidget
        self.chatShowWidget = Widget()
        self.chatShowWidget.setMinimumHeight(244)
        self.chatShowWidget.resize(1200, 520)
        self.chatShowWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #chatShowVLayout QVBoxLayout
        self.chatShowVLayout = QVBoxLayout()
        self.chatShowWidget.setLayout(self.chatShowVLayout)
        self.chatShowVLayout.addWidget(self.chatShow)
        self.chatShowVLayout.setContentsMargins(27, 12, 2, 16)
        #TextEditFull
        self.chatInput = TextEditFull()
        self.chatInput.connectSendButtonClick(self.sendMessage)
        #chatInputWidget QWidget
        self.chatInputWidget = Widget()
        self.chatInputWidget.setMinimumHeight(100)
        self.chatInputWidget.resize(1200, 208)
        self.chatInputWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #chatInputVLayout QVBoxLayout
        self.chatInputVLayout = QVBoxLayout()
        self.chatInputWidget.setLayout(self.chatInputVLayout)
        self.chatInputVLayout.addWidget(self.chatInput)
        self.chatInputVLayout.setContentsMargins(20, 0, 20, 20)
        #QSplitter
        self.splitter = Splitter(Qt.Vertical)
        self.splitter.resize(1200, 728)
        self.splitter.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.chatShowWidget)
        self.splitter.addWidget(self.chatInputWidget)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setHandleWidth(0)
        #contentWidget QWidget
        self.contentWidget = Widget()
        self.contentWidget.resize(1200, 764)
        self.contentWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #contentVLayout QVBoxLayout
        self.contentVLayout = QVBoxLayout()
        self.contentWidget.setLayout(self.contentVLayout)
        self.contentVLayout.addWidget(self.chatFun)
        self.contentVLayout.addWidget(self.splitter)
        self.contentVLayout.setContentsMargins(0, 0, 0, 0)
        self.contentVLayout.setSpacing(0)
        self.contentVLayout.setStretch(0, 0)
        self.contentVLayout.setStretch(1, 1)
        #mainWidget Frame
        self.mainWidget = Frame(self)
        self.mainWidget.setFixedSize(self.width() - 20, self.height() - 20)
        self.mainWidget.move(10, 10)
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.mainWidget.setObjectName("mainWidget")
        self.mainWidget.setStyleSheet('''
        #mainWidget {
            border-radius: 16px;
            background-color: #F0F0F0;
        }
        ''')
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.titleWidget)
        self.mainVLayout.addWidget(self.contentWidget)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        self.mainVLayout.setStretch(0, 0)
        self.mainVLayout.setStretch(1, 1)
        #QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)
        """ #MainWindow
        self.setCentralWidget(self.mainWidget) """
        #messageWidget list
        self.messageWidgetList = []
        #setting QWidget init
        self.settingWidgetInit()
        #ChatRecordsWidget
        self.chatRecordsWidget = ChatRecordsWidget(self.mainWidget)
        self.chatRecordsWidget.connectSettingButtonClick(self.settingButtonClicked)
        self.chatRecordsWidget.connectLineEditTextChanged(self.showSearchRecords)
        self.chatRecordsWidget.connectSearchButtonClick(self.showSearchRecords)
        self.chatRecordsWidget.connectClearAllButtonClick(self.clearAllChatRecords)
        self.chatRecordsWidget.connectListItemClick(self.generateChatRecord)
        self.chatRecordsWidget.move(-self.chatRecordsWidget.width(), self.titleWidget.height())
        #init curChatFile
        self.curChatFile = ''
        #chatRecordsAnimationMove QPropertyAnimation
        self.chatRecordsAnimationMove = QPropertyAnimation(self.chatRecordsWidget, b'geometry')
        self.chatRecordsAnimationMove.setDuration(1000)
        self.chatRecordsAnimationMove.setEasingCurve(QEasingCurve.OutQuad)
        self.chatRecordsAnimationMove.valueChanged.connect(self.chatRecordsUiAnimationMove)
        self.chatRecordsAnimationMove.finished.connect(self.chatRecordsUiMoveFinished)
        #chatRecordsAnimationMove2 QPropertyAnimation
        self.chatRecordsAnimationMove2 = QPropertyAnimation(self.chatRecordsWidget, b'geometry')
        self.chatRecordsAnimationMove2.setDuration(1000)
        self.chatRecordsAnimationMove2.setEasingCurve(QEasingCurve.OutQuad)
        self.chatRecordsAnimationMove2.valueChanged.connect(self.chatRecordsUiAnimationMove2)
        self.chatRecordsAnimationMove2.finished.connect(self.chatRecordsUiMoveFinished)
        #chatRecordsWidgetIsOpen
        self.chatRecordsWidgetIsOpen = False
        #chatRecordsFoldButton PushButton
        self.chatRecordsFoldButton = PushButton(tipText='折叠', tipOffsetX=10, tipOffsetY=40, parent=self.mainWidget)
        self.chatRecordsFoldButton.setFixedSize(30, 50)
        self.chatRecordsFoldButton.setIconSize(QSize(30, 50))
        self.chatRecordsFoldButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.fold_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.fold_hover_images_path}");
        }}
        ''')
        self.chatRecordsFoldButton.move(0, (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)
        self.chatRecordsFoldButton.hide()
        self.chatRecordsFoldButton.clicked.connect(self.chatRecordsFoldButtonClicked)
        #emptyTextLabel PrintLabel
        self.emptyTextLabel = PrintLabel('文本不能为空', self)
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.emptyTextLabel.height() - 10)
        self.emptyTextLabel.raise_()
        self.emptyTextLabel.hide()
        #textCopyLabel PrintLabel
        self.textCopyLabel = PrintLabel('文本复制成功', self)
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.textCopyLabel.height() - 10)
        self.textCopyLabel.raise_()
        self.textCopyLabel.hide()
        #resizeTimer
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.onResizeTimeout)
        #isSetTexting
        self.isSetTexting = False
        #pushButtonIsPress
        self.pushButtonIsPress = False
        #messageWidgetIsSelect
        self.messageWidgetIsSelect = False
        #selectMessageWidgetNumber
        self.selectMessageWidgetNumber = -1
        #settingIsTop
        self.settingIsTop = False
        #chatRecordsIsTop
        self.chatRecordsIsTop = False
        #
        print('init', self.settingWidget.geometry())
        print('init', self.chatRecordsWidget.geometry())
        print('init', self.mainWidget.geometry())
        print('init', self.geometry())

    """ def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPen
        painter.setPen(Qt.NoPen)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(240, 240, 240))
        painter.setBrush(brush)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 16, 16)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end() """

    def mouseMoveEvent(self, event):
        #If the mouse hovers over the list item, it has a pop-up effect
        self.isItemShowFull(self.childAt(event.pos()))
        #Stretch and drag the UI by dragging the mouse
        self.cursorGlobalPos = event.globalPos()
        self.cursorGlobalX = self.cursorGlobalPos.x()
        self.cursorGlobalY = self.cursorGlobalPos.y()
        self.uiGlobalTL = self.mainWidget.mapToGlobal(QPoint(0, 0))
        self.uiGlobalBR = self.mainWidget.mapToGlobal(QPoint(self.mainWidget.width(), self.mainWidget.height()))
        """ self.uiGlobalTL = self.geometry().topLeft()
        self.uiGlobalBR = self.geometry().bottomRight() """
        if not self.mouseLeftButtonIsPress:
            self.regionDivision()
        else:
            if self.regionDir != RegionEnum.TITLE and self.regionDir != RegionEnum.BUTTON and self.regionDir != RegionEnum.MIDDLE:
                self.UiStretch()
            else:
                if self.regionDir == RegionEnum.TITLE:
                    self.UiDrag(event.globalPos())
        QMainWindow.mouseMoveEvent(self, event)

    def isItemShowFull(self, widget):
        for i in range(0, len(self.messageWidgetList)):
            messageWidget = self.messageWidgetList[i]
            messageWidget.hideFunWidget()
            #chatShow itemWidget adjust size
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            if messageWidget.getIsUser():
                itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
            else:
                itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))
        if isinstance(widget, TextWidget):
            for i in range(0, len(self.messageWidgetList)):
                messageWidget = self.messageWidgetList[i]
                if widget == messageWidget.getTextWidget():
                    messageWidget.showFunWidget()
                    #chatShow itemWidget adjust size
                    itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
                    itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
                    if messageWidget.getIsUser():
                        itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
                    else:
                        itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
                    #chatShow item adjust size
                    self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))
        elif isinstance(widget, MessageWidget):
            for i in range(0, len(self.messageWidgetList)):
                messageWidget = self.messageWidgetList[i]
                if widget == messageWidget:
                    messageWidget.showFunWidget()
                    #chatShow itemWidget adjust size
                    itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
                    itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
                    if messageWidget.getIsUser():
                        itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
                    else:
                        itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
                    #chatShow item adjust size
                    self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))
        elif isinstance(widget, ItemWidget):
            childWidget = widget.layout().itemAt(0).widget()
            if isinstance(childWidget, MessageWidget):
                for i in range(0, len(self.messageWidgetList)):
                    messageWidget = self.messageWidgetList[i]
                    if childWidget == messageWidget:
                        messageWidget.showFunWidget()
                        #chatShow itemWidget adjust size
                        itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
                        itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
                        if messageWidget.getIsUser():
                            itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
                        else:
                            itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
                        #chatShow item adjust size
                        self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))

    def regionDivision(self):
        if self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + self.padding and self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + self.padding:
            self.regionDir = RegionEnum.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - self.padding and self.cursorGlobalX <= self.uiGlobalBR.x() and self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + self.padding:
            self.regionDir = RegionEnum.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + self.padding and self.cursorGlobalY >= self.uiGlobalBR.y() - self.padding and self.cursorGlobalY <= self.uiGlobalBR.y():
            self.regionDir = RegionEnum.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - self.padding and self.cursorGlobalX <= self.uiGlobalBR.x() and self.cursorGlobalY >= self.uiGlobalBR.y() - self.padding and self.cursorGlobalY <= self.uiGlobalBR.y():
            self.regionDir = RegionEnum.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + self.padding:
            self.regionDir = RegionEnum.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - self.padding and self.cursorGlobalX <= self.uiGlobalBR.x():
            self.regionDir = RegionEnum.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + self.padding:
            self.regionDir = RegionEnum.TOP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif self.cursorGlobalY >= self.uiGlobalBR.y() - self.padding and self.cursorGlobalY <= self.uiGlobalBR.y():
            self.regionDir = RegionEnum.BOTTOM
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif self.cursorGlobalX >= self.uiGlobalTL.x() + self.padding + 1 and self.cursorGlobalX <= self.uiGlobalBR.x() - self.padding - 1 and self.cursorGlobalY >= self.uiGlobalTL.y() + self.padding + 1 and self.cursorGlobalY <= self.uiGlobalTL.y() + self.titleWidget.height():
            if self.cursorGlobalX <= self.uiGlobalBR.x() - self.minButton.width() - self.maxButton.width() - self.closeButton.width() - 1:
                self.regionDir = RegionEnum.TITLE
            else:
                self.regionDir = RegionEnum.BUTTON
            self.setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.regionDir = RegionEnum.MIDDLE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def UiStretch(self):
        uiGlobalRect = QRect(self.uiGlobalTL, self.uiGlobalBR)
        match self.regionDir:
            case RegionEnum.LEFT:
                if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                    uiGlobalRect.setX(self.cursorGlobalX)
            case RegionEnum.RIGHT:
                if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                    uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
            case RegionEnum.TOP:
                if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                    uiGlobalRect.setY(self.cursorGlobalY)
            case RegionEnum.BOTTOM:
                if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                    uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
            case RegionEnum.LEFTTOP:
                if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                    uiGlobalRect.setX(self.cursorGlobalX)
                if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                    uiGlobalRect.setY(self.cursorGlobalY)
            case RegionEnum.RIGHTTOP:
                if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                    uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
                if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                    uiGlobalRect.setY(self.cursorGlobalY)
            case RegionEnum.LEFTBOTTOM:
                if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                    uiGlobalRect.setX(self.cursorGlobalX)
                if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                    uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
            case RegionEnum.RIGHTBOTTOM:
                if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                    uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
                if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                    uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
        windowGlobalRect = QRect(uiGlobalRect.x() - 10, uiGlobalRect.y() - 10, uiGlobalRect.width() + 20, uiGlobalRect.height() + 20)
        self.setGeometry(windowGlobalRect)
        #self.setGeometry(uiGlobalRect)

    def UiDrag(self, globalPos):
        self.move(self.pressPosDistanceUiGlobalTL + globalPos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonIsPress = True
            #title region calculate the distance to move
            if self.regionDir == RegionEnum.TITLE:
                self.pressPosDistanceUiGlobalTL = self.geometry().topLeft() - event.globalPos()
        QMainWindow.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonIsPress = False
            #judge mouse press position
            if self.pushButtonIsPress:
                self.pushButtonIsPress = False
            else:
                if self.settingWidgetIsOpen:
                    chatShowRect = QRect(self.chatShow.geometry().x() + self.settingWidget.width(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                elif self.chatRecordsWidgetIsOpen:
                    chatShowRect = QRect(self.chatShow.geometry().x() + self.chatRecordsWidget.width(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                else:
                    chatShowRect = QRect(self.chatShow.geometry().x(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                if not chatShowRect.contains(event.pos()):
                    self.messageWidgetIsSelect = False
                    self.selectMessageWidgetNumber = -1
                    for i in range(0, len(self.messageWidgetList)):
                        self.messageWidgetList[i].showDefaultColor()
                else:
                    widget = self.childAt(event.pos())
                    if isinstance(widget, CopyButton):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            messageWidget.showDefaultColor()
                            if widget == messageWidget.getCopyButton():
                                self.messageWidgetIsSelect = True
                                self.selectMessageWidgetNumber = i
                                messageWidget.showColorful()
                    elif isinstance(widget.parent(), WebEngineView):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            messageWidget.showDefaultColor()
                            if widget.parent() == messageWidget.getTextShow().getWebEngineView():
                                self.messageWidgetIsSelect = True
                                self.selectMessageWidgetNumber = i
                                messageWidget.showColorful()
                if self.settingWidgetIsOpen:
                    chatInputRect = QRect(self.chatInput.geometry().x() + self.settingWidget.width(), self.chatInput.geometry().y() + self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height(), self.chatInput.geometry().width(), self.chatInput.geometry().height())
                elif self.chatRecordsWidgetIsOpen:
                    chatInputRect = QRect(self.chatInput.geometry().x() + self.chatRecordsWidget.width(), self.chatInput.geometry().y() + self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height(), self.chatInput.geometry().width(), self.chatInput.geometry().height())
                else:
                    chatInputRect = QRect(self.chatInput.geometry().x(), self.chatInput.geometry().y() + self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height(), self.chatInput.geometry().width(), self.chatInput.geometry().height())
                if chatInputRect.contains(event.pos()):
                    self.chatInput.backgroundColorShowLight()
                else:
                    self.chatInput.backgroundColorShowDark()
                    self.chatInput.clearFocus()
        QMainWindow.mouseReleaseEvent(self, event)

    def itemShowColorful(self, item):
        for i in range(0, len(self.messageWidgetList)):
            self.messageWidgetList[i].showDefaultColor()
        self.messageWidgetList[self.chatShow.row(item)].showColorful()
        self.messageWidgetIsSelect = True
        self.selectMessageWidgetNumber = self.chatShow.row(item)

    def resizeEvent(self, event):
        #mainWidget Frame
        self.mainWidget.setFixedSize(self.width() - 20, self.height() - 20)
        self.mainWidget.move(10, 10)
        #setting widget set geometry
        self.settingWidget.resize(self.mainWidget.width() // 3, self.mainWidget.height() - self.titleWidget.height())
        if self.settingWidgetIsOpen:
            self.chatShow.resize(self.mainWidget.width() * 2 // 3 - 29, self.chatShow.height())
            self.chatShowWidget.resize(self.mainWidget.width() * 2 // 3, self.chatShowWidget.height())
            self.chatInput.resize(self.mainWidget.width() * 2 // 3 - 40, self.chatInput.height())
            self.chatInput.resetWidgetSize()
            self.chatInputWidget.resize(self.mainWidget.width() * 2 // 3, self.chatInputWidget.height())
            self.splitter.resize(self.mainWidget.width() * 2 // 3, self.splitter.height())
            self.contentVLayout.setContentsMargins(self.mainWidget.width() // 3, 0, 0, 0)
        else:
            self.settingWidget.move(-self.settingWidget.width(), self.titleWidget.height())
        #chatRecords widget set geometry
        self.chatRecordsWidget.resetWidgetSize(self.mainWidget.width() // 3, self.mainWidget.height() - self.titleWidget.height())
        if self.chatRecordsWidgetIsOpen:
            self.chatShow.resize(self.mainWidget.width() * 2 // 3 - 29, self.chatShow.height())
            self.chatShowWidget.resize(self.mainWidget.width() * 2 // 3, self.chatShowWidget.height())
            self.chatInput.resize(self.mainWidget.width() * 2 // 3 - 40, self.chatInput.height())
            self.chatInput.resetWidgetSize()
            self.chatInputWidget.resize(self.mainWidget.width() * 2 // 3, self.chatInputWidget.height())
            self.splitter.resize(self.mainWidget.width() * 2 // 3, self.splitter.height())
            self.contentVLayout.setContentsMargins(self.mainWidget.width() // 3, 0, 0, 0)
        else:
            self.chatRecordsWidget.move(-self.chatRecordsWidget.width(), self.titleWidget.height())
        #resizeTimer
        self.resizeTimer.start(150)
        #TextEditFull adjust size
        self.chatInput.resetWidgetSize()
        #move emptyTextLabel
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.emptyTextLabel.height() - 10)
        #move textCopyLabel
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.textCopyLabel.height() - 10)
        #
        print('resize', self.settingWidget.geometry())
        print('resize', self.chatRecordsWidget.geometry())
        print('resize', self.mainWidget.geometry())
        print('resize', self.geometry())

    def titleWidgetInit(self):
        #titleIconLabel QLabel
        self.titleIconLabel = QLabel()
        self.titleIconLabel.setFixedSize(30, 30)
        self.titleIconLabel.setScaledContents(True)
        self.ai_assistant_images_path = os.path.join(images_dir, 'ai_assistant.png').replace('\\', '/')
        self.titleIconLabel.setPixmap(QPixmap(f'{self.ai_assistant_images_path}'))
        #titleTextLabel QLabel
        self.titleTextLabel = QLabel()
        self.titleTextLabel.setFixedHeight(30)
        self.titleTextFont = QFont()
        self.titleTextFont.setPixelSize(windowFontSize)
        self.titleTextLabel.setFont(self.titleTextFont)
        self.titleTextPalette = self.titleTextLabel.palette()
        self.titleTextPalette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.titleTextLabel.setPalette(self.titleTextPalette)
        self.titleTextLabel.setText('AI助理')
        self.titleTextLabel.adjustSize()
        #titleLeftSubWidget QWidget
        self.titleLeftSubWidget = Widget()
        self.titleLeftSubWidget.resize(self.titleIconLabel.width() + self.titleTextLabel.width() + 20, 36)
        self.titleLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleLeftSubHLayout QHBoxLayout
        self.titleLeftSubHLayout = QHBoxLayout()
        self.titleLeftSubWidget.setLayout(self.titleLeftSubHLayout)
        self.titleLeftSubHLayout.addWidget(self.titleIconLabel)
        self.titleLeftSubHLayout.addWidget(self.titleTextLabel)
        self.titleLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.titleLeftSubHLayout.setContentsMargins(10, 3, 5, 3)
        self.titleLeftSubHLayout.setSpacing(5)
        #minButton PushButton
        self.minButton = PushButton(tipText='', tipOffsetX=20, tipOffsetY=40)
        self.minButton.setFixedSize(50, 36)
        self.min_images_path = os.path.join(images_dir, 'min.png').replace('\\', '/')
        self.minButton.setIcon(QIcon(f"{self.min_images_path}"))
        self.minButton.setIconSize(QSize(20, 20))
        self.minButton.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QPushButton:hover{
            background: #808080;
        }
        ''')
        self.minButton.clicked.connect(self.UiMinimize)
        #maxButton PushButton
        self.maxButton = PushButton(tipText='', tipOffsetX=20, tipOffsetY=40)
        self.maxButton.setFixedSize(50, 36)
        self.max_images_path = os.path.join(images_dir, 'max.png').replace('\\', '/')
        self.normal_images_path = os.path.join(images_dir, 'normal.png').replace('\\', '/')
        self.maxButton.setIcon(QIcon(f"{self.max_images_path}"))
        self.maxButton.setIconSize(QSize(20, 20))
        self.maxButton.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QPushButton:hover{
            background: #808080;
        }
        ''')
        self.maxButton.clicked.connect(self.UiMaximize)
        #closeButton PushButton
        self.closeButton = PushButton(tipText='', tipOffsetX=10, tipOffsetY=40)
        self.closeButton.setFixedSize(50, 36)
        self.close_images_path = os.path.join(images_dir, 'close.png').replace('\\', '/')
        self.closeButton.setIcon(QIcon(f"{self.close_images_path}"))
        self.closeButton.setIconSize(QSize(20, 20))
        self.closeButton.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QPushButton:hover{
            border-top-right-radius: 16px;
            background: #c80000;
        }
        ''')
        self.closeButton.clicked.connect(self.UiClose)
        #titleRightSubWidget QWidget
        self.titleRightSubWidget = Widget()
        self.titleRightSubWidget.resize(150, 36)
        self.titleRightSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleRightSubHLayout QHBoxLayout
        self.titleRightSubHLayout = QHBoxLayout()
        self.titleRightSubWidget.setLayout(self.titleRightSubHLayout)
        self.titleRightSubHLayout.addWidget(self.minButton)
        self.titleRightSubHLayout.addWidget(self.maxButton)
        self.titleRightSubHLayout.addWidget(self.closeButton)
        self.titleRightSubHLayout.setAlignment(Qt.AlignRight)
        self.titleRightSubHLayout.setContentsMargins(0, 0, 0, 0)
        self.titleRightSubHLayout.setSpacing(0)
        #titleWidget QWidget
        self.titleWidget = TitleWidget()
        self.titleWidget.resize(1200, 36)
        self.titleWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleHLayout QHBoxLayout
        self.titleHLayout = QHBoxLayout()
        self.titleWidget.setLayout(self.titleHLayout)
        self.titleHLayout.addWidget(self.titleLeftSubWidget)
        self.titleHLayout.addWidget(self.titleRightSubWidget)
        self.titleHLayout.setContentsMargins(0, 0, 0, 0)

    def UiMinimize(self):
        self.showMinimized()

    def UiMaximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maxButton.setIcon(QIcon(f"{self.max_images_path}"))
        else:
            self.showMaximized()
            self.maxButton.setIcon(QIcon(f"{self.normal_images_path}"))

    def UiClose(self):
        self.saveCurChatRecord(withholdCurChatFile=True)
        self.close()

    def settingWidgetInit(self):
        #setting config file
        if not os.path.exists(config_file_path):
            with open(config_file_path, "w") as f:
                global init_base_url, init_api_key, init_model, init_maxTokens_currentVal, init_topP_currentVal, init_temperature_currentVal
                f.write(init_base_url + '\n' + init_api_key + '\n' + init_model + '\n' + str(init_maxTokens_currentVal) + '\n' + str(init_topP_currentVal) + '\n' + str(init_temperature_currentVal) + '\n')
        with open(config_file_path, "r") as f:
            content = f.readlines()
        base_url = content[0].strip('\n')
        api_key = content[1].strip('\n')
        model = content[2].strip('\n')
        maxTokens_currentVal = int(content[3].strip('\n'))
        topP_currentVal = float(content[4].strip('\n'))
        temperature_currentVal = float(content[5].strip('\n'))
        #setting QLabel
        self.baseUrlLabel = Label()
        self.apiKeyLabel = Label()
        self.modelNameLabel = Label()
        self.maxTokensLabel = Label()
        self.topPLabel = Label()
        self.temperatureLabel = Label()
        self.baseUrlLabel.setText('Base Url')
        self.apiKeyLabel.setText('Api Key')
        self.modelNameLabel.setText('Model')
        self.maxTokensLabel.setText("Max Tokens")
        self.topPLabel.setText("Top P")
        self.temperatureLabel.setText("Temperature")
        #setting QLineEdit
        self.baseUrlEdit = SettingEdit()
        self.apiKeyEdit = SettingEdit()
        self.modelNameEdit = SettingEdit()
        self.baseUrlEdit.setText(base_url)
        self.apiKeyEdit.setText(api_key)
        self.modelNameEdit.setText(model)
        self.baseUrlEdit.textChanged.connect(self.baseUrlTextChanged)
        self.apiKeyEdit.textChanged.connect(self.apiKeyTextChanged)
        self.modelNameEdit.textChanged.connect(self.modelNameTextChanged)
        #setting QSpinBox
        self.maxTokensBox = SpinBox()
        self.topPBox = DoubleSpinBox()
        self.temperatureBox = DoubleSpinBox()
        self.maxTokensBox.setRange(maxTokens_minimum, maxTokens_maximum)
        self.maxTokensBox.setValue(maxTokens_currentVal)
        self.topPBox.setRange(topP_minimum, topP_maximum)
        self.topPBox.setValue(topP_currentVal)
        self.topPBox.setSingleStep(topP_singleStep)
        self.temperatureBox.setRange(temperature_minimum, temperature_maximum)
        self.temperatureBox.setValue(temperature_currentVal)
        self.temperatureBox.setSingleStep(temperature_singleStep)
        self.maxTokensBox.valueChanged.connect(self.maxTokensBoxValueChanged)
        self.topPBox.valueChanged.connect(self.topPBoxValueChanged)
        self.temperatureBox.valueChanged.connect(self.temperatureBoxValueChanged)
        #setting QSlider
        self.maxTokensSlider = Slider()
        self.topPSlider = Slider()
        self.temperatureSlider = Slider()
        self.maxTokensSlider.setMinimum(maxTokens_minimum)
        self.maxTokensSlider.setMaximum(maxTokens_maximum)
        self.maxTokensSlider.setValue(maxTokens_currentVal)
        self.topPSlider.setMinimum(int(topP_minimum * 100))
        self.topPSlider.setMaximum(int(topP_maximum * 100))
        self.topPSlider.setValue(int(topP_currentVal * 100))
        self.temperatureSlider.setMinimum(int((temperature_minimum - 0.01) * 100))
        self.temperatureSlider.setMaximum(int((temperature_maximum - 0.01) * 100))
        self.temperatureSlider.setValue(int((temperature_currentVal - 0.01) * 100))
        self.maxTokensSlider.valueChanged.connect(self.maxTokensSliderValueChanged)
        self.topPSlider.valueChanged.connect(self.topPSliderValueChanged)
        self.temperatureSlider.valueChanged.connect(self.temperatureSliderValueChanged)
        #setting ModelSelect QWidget
        self.modelSelectWidget = QWidget()
        self.modelSelectWidget.resize(370, 190)
        self.modelSelectWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.modelSelectWidget.setObjectName("modelSelectWidget")
        self.modelSelectWidget.setStyleSheet('''
        QWidget#modelSelectWidget{
            border-radius: 15px;
            background: white;
        }
        ''')
        #setting base url QWidget
        self.baseUrlWidget = QWidget()
        self.baseUrlWidget.resize(340, 32)
        self.baseUrlWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.baseUrlWidget.setObjectName("baseUrlWidget")
        self.baseUrlWidget.setStyleSheet('''
        QWidget#baseUrlWidget{
            background: transparent;
        }
        ''')
        #setting base url QHBoxLayout
        self.baseUrlHLayout = QHBoxLayout()
        self.baseUrlWidget.setLayout(self.baseUrlHLayout)
        self.baseUrlHLayout.addWidget(self.baseUrlLabel)
        self.baseUrlHLayout.addWidget(self.baseUrlEdit)
        self.baseUrlHLayout.setContentsMargins(0, 0, 0, 0)
        #setting api key QWidget
        self.apiKeyWidget = QWidget()
        self.apiKeyWidget.resize(340, 32)
        self.apiKeyWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.apiKeyWidget.setObjectName("apiKeyWidget")
        self.apiKeyWidget.setStyleSheet('''
        QWidget#apiKeyWidget{
            background: transparent;
        }
        ''')
        #setting api key QHBoxLayout
        self.apiKeyHLayout = QHBoxLayout()
        self.apiKeyWidget.setLayout(self.apiKeyHLayout)
        self.apiKeyHLayout.addWidget(self.apiKeyLabel)
        self.apiKeyHLayout.addWidget(self.apiKeyEdit)
        self.apiKeyHLayout.setContentsMargins(0, 0, 0, 0)
        #setting model name QWidget
        self.modelNameWidget = QWidget()
        self.modelNameWidget.resize(340, 32)
        self.modelNameWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.modelNameWidget.setObjectName("modelNameWidget")
        self.modelNameWidget.setStyleSheet('''
        QWidget#modelNameWidget{
            background: transparent;
        }
        ''')
        #setting model name QHBoxLayout
        self.modelNameHLayout = QHBoxLayout()
        self.modelNameWidget.setLayout(self.modelNameHLayout)
        self.modelNameHLayout.addWidget(self.modelNameLabel)
        self.modelNameHLayout.addWidget(self.modelNameEdit)
        self.modelNameHLayout.setContentsMargins(0, 0, 0, 0)
        #setting model select QVBoxLayout
        self.modelSelectVLayout = QVBoxLayout()
        self.modelSelectWidget.setLayout(self.modelSelectVLayout)
        self.modelSelectVLayout.addWidget(self.baseUrlWidget)
        self.modelSelectVLayout.addWidget(self.apiKeyWidget)
        self.modelSelectVLayout.addWidget(self.modelNameWidget)
        self.modelSelectVLayout.setContentsMargins(15, 27, 15, 27)
        self.modelSelectVLayout.setSpacing(20)
        #setting maxTokens QWidget
        self.maxTokensWidget = QWidget()
        self.maxTokensWidget.resize(370, 130)
        self.maxTokensWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.maxTokensWidget.setObjectName("maxTokensWidget")
        self.maxTokensWidget.setStyleSheet('''
        QWidget#maxTokensWidget{
            border-radius: 15px;
            background: white;
        }
        ''')
        #setting maxTokens top sub QWidget
        self.maxTokensTopSubWidget = QWidget()
        self.maxTokensTopSubWidget.resize(340, 40)
        self.maxTokensTopSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.maxTokensTopSubWidget.setObjectName("maxTokensTopSubWidget")
        self.maxTokensTopSubWidget.setStyleSheet('''
        QWidget#maxTokensTopSubWidget{
            background: transparent;
        }
        ''')
        #setting maxTokens top sub QHBoxLayout
        self.maxTokensTopSubHLayout = QHBoxLayout()
        self.maxTokensTopSubWidget.setLayout(self.maxTokensTopSubHLayout)
        self.maxTokensTopSubHLayout.addWidget(self.maxTokensLabel)
        self.maxTokensTopSubHLayout.addWidget(self.maxTokensBox)
        self.maxTokensTopSubHLayout.setContentsMargins(0, 5, 0, 3)
        #setting maxTokens bottom sub QWidget
        self.maxTokensBottomSubWidget = QWidget()
        self.maxTokensBottomSubWidget.resize(340, 40)
        self.maxTokensBottomSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.maxTokensBottomSubWidget.setObjectName("maxTokensBottomSubWidget")
        self.maxTokensBottomSubWidget.setStyleSheet('''
        QWidget#maxTokensBottomSubWidget{
            background: transparent;
        }
        ''')
        #setting maxTokens bottom sub QHBoxLayout
        self.maxTokensBottomSubHLayout = QHBoxLayout()
        self.maxTokensBottomSubWidget.setLayout(self.maxTokensBottomSubHLayout)
        self.maxTokensBottomSubHLayout.addWidget(self.maxTokensSlider)
        self.maxTokensBottomSubHLayout.setContentsMargins(0, 9, 0, 5)
        #setting maxTokens QVBoxLayout
        self.maxTokensVLayout = QVBoxLayout()
        self.maxTokensWidget.setLayout(self.maxTokensVLayout)
        self.maxTokensVLayout.addWidget(self.maxTokensTopSubWidget)
        self.maxTokensVLayout.addWidget(self.maxTokensBottomSubWidget)
        self.maxTokensVLayout.setContentsMargins(15, 25, 15, 25)
        self.maxTokensVLayout.setSpacing(0)
        #setting topP QWidget
        self.topPWidget = QWidget()
        self.topPWidget.resize(370, 130)
        self.topPWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.topPWidget.setObjectName("topPWidget")
        self.topPWidget.setStyleSheet('''
        QWidget#topPWidget{
            border-radius: 15px;
            background: white;
        }
        ''')
        #setting topP top sub QWidget
        self.topPTopSubWidget = QWidget()
        self.topPTopSubWidget.resize(340, 40)
        self.topPTopSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.topPTopSubWidget.setObjectName("topPTopSubWidget")
        self.topPTopSubWidget.setStyleSheet('''
        QWidget#topPTopSubWidget{
            background: transparent;
        }
        ''')
        #setting topP top sub QHBoxLayout
        self.topPTopSubHLayout = QHBoxLayout()
        self.topPTopSubWidget.setLayout(self.topPTopSubHLayout)
        self.topPTopSubHLayout.addWidget(self.topPLabel)
        self.topPTopSubHLayout.addWidget(self.topPBox)
        self.topPTopSubHLayout.setContentsMargins(0, 5, 0, 3)
        #setting topP bottom sub QWidget
        self.topPBottomSubWidget = QWidget()
        self.topPBottomSubWidget.resize(340, 40)
        self.topPBottomSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.topPBottomSubWidget.setObjectName("topPBottomSubWidget")
        self.topPBottomSubWidget.setStyleSheet('''
        QWidget#topPBottomSubWidget{
            background: transparent;
        }
        ''')
        #setting topP bottom sub QHBoxLayout
        self.topPBottomSubHLayout = QHBoxLayout()
        self.topPBottomSubWidget.setLayout(self.topPBottomSubHLayout)
        self.topPBottomSubHLayout.addWidget(self.topPSlider)
        self.topPBottomSubHLayout.setContentsMargins(0, 9, 0, 5)
        #setting topP QVBoxLayout
        self.topPVLayout = QVBoxLayout()
        self.topPWidget.setLayout(self.topPVLayout)
        self.topPVLayout.addWidget(self.topPTopSubWidget)
        self.topPVLayout.addWidget(self.topPBottomSubWidget)
        self.topPVLayout.setContentsMargins(15, 25, 15, 25)
        self.topPVLayout.setSpacing(0)
        #setting temperature QWidget
        self.temperatureWidget = QWidget()
        self.temperatureWidget.resize(370, 130)
        self.temperatureWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.temperatureWidget.setObjectName("temperatureWidget")
        self.temperatureWidget.setStyleSheet('''
        QWidget#temperatureWidget{
            border-radius: 15px;
            background: white;
        }
        ''')
        #setting temperature top sub QWidget
        self.temperatureTopSubWidget = QWidget()
        self.temperatureTopSubWidget.resize(340, 40)
        self.temperatureTopSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.temperatureTopSubWidget.setObjectName("temperatureTopSubWidget")
        self.temperatureTopSubWidget.setStyleSheet('''
        QWidget#temperatureTopSubWidget{
            background: transparent;
        }
        ''')
        #setting temperature top sub QHBoxLayout
        self.temperatureTopSubHLayout = QHBoxLayout()
        self.temperatureTopSubWidget.setLayout(self.temperatureTopSubHLayout)
        self.temperatureTopSubHLayout.addWidget(self.temperatureLabel)
        self.temperatureTopSubHLayout.addWidget(self.temperatureBox)
        self.temperatureTopSubHLayout.setContentsMargins(0, 5, 0, 3)
        #setting temperature bottom sub QWidget
        self.temperatureBottomSubWidget = QWidget()
        self.temperatureBottomSubWidget.resize(340, 40)
        self.temperatureBottomSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.temperatureBottomSubWidget.setObjectName("temperatureBottomSubWidget")
        self.temperatureBottomSubWidget.setStyleSheet('''
        QWidget#temperatureBottomSubWidget{
            background: transparent;
        }
        ''')
        #setting temperature bottom sub QHBoxLayout
        self.temperatureBottomSubHLayout = QHBoxLayout()
        self.temperatureBottomSubWidget.setLayout(self.temperatureBottomSubHLayout)
        self.temperatureBottomSubHLayout.addWidget(self.temperatureSlider)
        self.temperatureBottomSubHLayout.setContentsMargins(0, 9, 0, 5)
        #setting temperature QVBoxLayout
        self.temperatureVLayout = QVBoxLayout()
        self.temperatureWidget.setLayout(self.temperatureVLayout)
        self.temperatureVLayout.addWidget(self.temperatureTopSubWidget)
        self.temperatureVLayout.addWidget(self.temperatureBottomSubWidget)
        self.temperatureVLayout.setContentsMargins(15, 25, 15, 25)
        self.temperatureVLayout.setSpacing(0)
        #setting QWidget
        self.settingWidget = SettingWidget(self.mainWidget)
        self.settingWidget.setGeometry(-self.mainWidget.width() // 3, self.titleWidget.height(), self.mainWidget.width() // 3, self.mainWidget.height() - self.titleWidget.height())
        self.settingWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #setting QVBoxLayout
        self.settingVLayout = QVBoxLayout()
        self.settingWidget.setLayout(self.settingVLayout)
        self.settingVLayout.addWidget(self.modelSelectWidget)
        self.settingVLayout.addWidget(self.maxTokensWidget)
        self.settingVLayout.addWidget(self.topPWidget)
        self.settingVLayout.addWidget(self.temperatureWidget)
        self.settingVLayout.setContentsMargins(15, 47, 15, 47)
        self.settingVLayout.setSpacing(30)
        #settingAnimationMove QPropertyAnimation
        self.settingAnimationMove = QPropertyAnimation(self.settingWidget, b'geometry')
        self.settingAnimationMove.setDuration(1000)
        self.settingAnimationMove.setEasingCurve(QEasingCurve.OutQuad)
        self.settingAnimationMove.valueChanged.connect(self.settingUiAnimationMove)
        self.settingAnimationMove.finished.connect(self.settingUiMoveFinished)
        #settingAnimationMove2 QPropertyAnimation
        self.settingAnimationMove2 = QPropertyAnimation(self.settingWidget, b'geometry')
        self.settingAnimationMove2.setDuration(1000)
        self.settingAnimationMove2.setEasingCurve(QEasingCurve.OutQuad)
        self.settingAnimationMove2.valueChanged.connect(self.settingUiAnimationMove2)
        self.settingAnimationMove2.finished.connect(self.settingUiMoveFinished)
        #settingWidgetIsOpen
        self.settingWidgetIsOpen = False
        #settingFoldButton PushButton
        self.settingFoldButton = PushButton(tipText='折叠', tipOffsetX=10, tipOffsetY=40, parent=self.mainWidget)
        self.settingFoldButton.setFixedSize(30, 50)
        self.settingFoldButton.setIconSize(QSize(30, 50))
        self.fold_images_path = os.path.join(images_dir, 'fold.png').replace('\\', '/')
        self.fold_hover_images_path = os.path.join(images_dir, 'fold_hover.png').replace('\\', '/')
        self.settingFoldButton.setStyleSheet(f'''
        QPushButton{{
            border-image: url("{self.fold_images_path}");
        }}
        QPushButton:hover{{
            border-image: url("{self.fold_hover_images_path}");
        }}
        ''')
        self.settingFoldButton.move(0, (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)
        self.settingFoldButton.hide()
        self.settingFoldButton.clicked.connect(self.settingFoldButtonClicked)

    def settingButtonClicked(self):
        if not self.settingWidgetIsOpen:
            if not self.chatRecordsWidgetIsOpen:
                self.settingWidget.raise_()
                self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
                self.settingAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                self.settingAnimationMove.start()
                self.settingWidgetIsOpen = True
                self.settingIsTop = True
            else:
                self.settingWidget.raise_()
                self.settingAnimationMove2.setStartValue(self.settingWidget.geometry())
                self.settingAnimationMove2.setEndValue(QRect(0, self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                self.settingAnimationMove2.start()
                self.settingWidgetIsOpen = True
                self.settingIsTop = True
                self.chatRecordsIsTop = False
            self.settingFoldButton.raise_()
            self.settingFoldButton.show()
        else:
            if self.settingIsTop:
                if not self.chatRecordsWidgetIsOpen:
                    self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
                    self.settingAnimationMove.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                    self.settingAnimationMove.start()
                    self.settingWidgetIsOpen = False
                    self.settingIsTop = False
                else:
                    self.settingAnimationMove2.setStartValue(self.settingWidget.geometry())
                    self.settingAnimationMove2.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                    self.settingAnimationMove2.start()
                    self.settingWidgetIsOpen = False
                    self.settingIsTop = False
                    self.chatRecordsIsTop = True
            else:
                self.settingWidget.raise_()
                self.settingIsTop = True
                self.chatRecordsIsTop = False
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def settingUiAnimationMove(self, rect):
        self.settingFoldButton.move(rect.x() + self.settingWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)
        self.chatShow.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.settingWidget.width(), 0, 0, 0)
        #resizeTimer
        self.resizeTimer.start(150)
        #
        print('setting move', self.settingWidget.geometry())
        print('setting move', self.chatRecordsWidget.geometry())
        print('setting move', self.mainWidget.geometry())
        print('setting move', self.geometry())

    def settingUiMoveFinished(self):
        if not self.settingWidgetIsOpen:
            self.settingFoldButton.hide()

    def settingUiAnimationMove2(self, rect):
        self.settingFoldButton.move(rect.x() + self.settingWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)

    def settingFoldButtonClicked(self):
        if not self.chatRecordsWidgetIsOpen:
            self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
            self.settingAnimationMove.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
            self.settingAnimationMove.start()
            self.settingWidgetIsOpen = False
            self.settingIsTop = False
        else:
            self.settingAnimationMove2.setStartValue(self.settingWidget.geometry())
            self.settingAnimationMove2.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
            self.settingAnimationMove2.start()
            self.settingWidgetIsOpen = False
            self.settingIsTop = False
            self.chatRecordsIsTop = True

    def chatRecordsUiAnimationMove(self, rect):
        self.chatRecordsFoldButton.move(rect.x() + self.chatRecordsWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)
        self.chatShow.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.chatRecordsWidget.width(), 0, 0, 0)
        #resizeTimer
        self.resizeTimer.start(150)
        #
        print('record move', self.settingWidget.geometry())
        print('record move', self.chatRecordsWidget.geometry())
        print('record move', self.mainWidget.geometry())
        print('record move', self.geometry())

    def chatRecordsUiMoveFinished(self):
        if not self.chatRecordsWidgetIsOpen:
            self.chatRecordsFoldButton.hide()
            #delete all item
            self.chatRecordsWidget.delAllListItems()

    def chatRecordsUiAnimationMove2(self, rect):
        self.chatRecordsFoldButton.move(rect.x() + self.settingWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)

    def chatRecordsFoldButtonClicked(self):
        if not self.settingWidgetIsOpen:
            self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
            self.chatRecordsAnimationMove.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
            self.chatRecordsAnimationMove.start()
            self.chatRecordsWidgetIsOpen = False
            self.chatRecordsIsTop = False
        else:
            self.chatRecordsAnimationMove2.setStartValue(self.chatRecordsWidget.geometry())
            self.chatRecordsAnimationMove2.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
            self.chatRecordsAnimationMove2.start()
            self.chatRecordsWidgetIsOpen = False
            self.chatRecordsIsTop = False
            self.settingIsTop = True

    def baseUrlTextChanged(self, text):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[0] = text + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)

    def apiKeyTextChanged(self, text):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[1] = text + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)

    def modelNameTextChanged(self, text):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[2] = text + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)

    def maxTokensBoxValueChanged(self, i):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[3] = str(i) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.maxTokensSlider.setValue(i)

    def topPBoxValueChanged(self, d):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[4] = str(d) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.topPSlider.setValue(int(d * 100))

    def temperatureBoxValueChanged(self, d):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[5] = str(d) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.temperatureSlider.setValue(int((d - 0.01) * 100))

    def maxTokensSliderValueChanged(self, i):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[3] = str(i) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.maxTokensBox.setValue(i)

    def topPSliderValueChanged(self, i):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[4] = str(i / 100) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.topPBox.setValue(i / 100)

    def temperatureSliderValueChanged(self, i):
        with open(config_file_path, "r") as f:
            lines = f.readlines()
        lines[5] = str(i / 100 + 0.01) + '\n'
        with open(config_file_path, "w") as f:
            f.writelines(lines)
        self.temperatureBox.setValue(i / 100 + 0.01)

    def messageWidgetResize(self):
        for i in range(0, self.chatShow.count()):
            messageWidget = self.messageWidgetList[i]
            messageWidget.setSize()
            #chatShow itemWidget adjust size
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            if messageWidget.getIsUser():
                itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
            else:
                itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))

    def sendMessage(self):
        #judge status of sendButton
        if not self.chatInput.sendButtonIsEnable():
            return
        context = []
        #get text from TextEditFull
        text = self.chatInput.toPlainText()
        if not text == '':
            for i in range(0, len(self.messageWidgetList)):
                messageWidget = self.messageWidgetList[i]
                if messageWidget.getIsUser():
                    context += [
                        {
                            "role": "user",
                            "content": messageWidget.getText()
                        }
                    ]
                else:
                    context += [
                        {
                            "role": "assistant",
                            "content": messageWidget.getText()
                        }
                    ]
            #MessageWidget
            self.messageSendWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=True, textMaxWidth=int(self.chatShow.width() * 2 / 3))
            self.messageSendWidget.connectSetSizeFinished(self.messageWidgetResize)
            self.messageSendWidget.connectSetTexting(self.getSetTexting)
            self.messageWidgetList.append(self.messageSendWidget)
            #itemSendWidget QWidget
            self.itemSendWidget = ItemWidget(self)
            self.itemSendHLayout = QHBoxLayout()
            self.itemSendHLayout.addWidget(self.messageSendWidget)
            self.itemSendWidget.setLayout(self.itemSendHLayout)
            self.itemSendWidget.setFixedSize(self.chatShow.width(), self.messageSendWidget.height() + 10)
            self.itemSendHLayout.setContentsMargins(self.itemSendWidget.width() - self.messageSendWidget.width() - 25, 5, 25, 5)
            #sendItem QListWidgetItem
            self.sendItem = QListWidgetItem(self.chatShow)
            self.sendItem.setSizeHint(QSize(self.chatShow.width(), self.messageSendWidget.height() + 10))
            self.chatShow.setItemWidget(self.sendItem, self.itemSendWidget)
            #MessageWidget
            self.messageSendWidget.toggleWidget()
            #create thread
            self.thread = messageThread(text, context=context)
            self.thread.started.connect(self.messageStart)
            self.thread.newMessage.connect(self.recvMessage)
            self.thread.finished.connect(self.messageFinish)
            self.thread.start()
            #disable sendButton
            self.chatInput.disableSendButton()
            #clear text of TextEditFull
            self.chatInput.clearText()
        else:
            #print emptyTextLabel
            self.emptyTextLabel.printStart()

    def messageStart(self):
        #message
        self.Message = ""
        #messageWidget remove renewResponseButton
        i = len(self.messageWidgetList) - 1
        if i != 0:
            if self.messageWidgetList[i].getIsUser():
                self.messageWidgetList[i - 1].removeRenewResponseButton()
            else:
                self.messageWidgetList[i].removeRenewResponseButton()
        #MessageWidget
        self.messageRecvWidget = MessageWidget(self.Message, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=False, textMaxWidth=int(self.chatShow.width() * 2 / 3))
        self.messageRecvWidget.connectSetSizeFinished(self.messageWidgetResize)
        self.messageRecvWidget.connectSetTexting(self.getSetTexting)
        self.messageWidgetList.append(self.messageRecvWidget)
        #itemRecvWidget QWidget
        self.itemRecvWidget = ItemWidget(self)
        self.itemRecvHLayout = QHBoxLayout()
        self.itemRecvHLayout.addWidget(self.messageRecvWidget)
        self.itemRecvWidget.setLayout(self.itemRecvHLayout)
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(0, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width(), 5)
        #recvItem QListWidgetItem
        self.recvItem = QListWidgetItem(self.chatShow)
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))
        self.chatShow.setItemWidget(self.recvItem, self.itemRecvWidget)
        #first
        self.first = True

    def recvMessage(self, text):
        if self.first:
            self.first = False
            text = text.strip("\n ")
        self.Message += text
        #messageWidget set text
        self.messageRecvWidget.setText(self.Message)
        #chatShow itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(0, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width(), 5)
        #chatShow item adjust size
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))

    def messageFinish(self):
        #messageRecvWidget
        self.messageRecvWidget.removeLoadingWidget()
        self.messageRecvWidget.toggleWidget()
        #chatShow itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(0, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width(), 5)
        #chatShow item adjust size
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))
        #enable sendButton
        self.chatInput.enableSendButton()
        #message renew response if message is empty
        if self.Message == '':
            del self.messageWidgetList[-1]
            last = self.chatShow.count() - 1
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(last))
            itemWidget.deleteLater()
            lastItem = self.chatShow.takeItem(last)
            del lastItem
            self.messageRenewResponse()

    def textCopy(self):
        #print textCopyLabel
        self.textCopyLabel.printStart()
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def messageRenewResponse(self):
        i = len(self.messageWidgetList) - 1
        j = 0
        while i >= j:
            if self.messageWidgetList[i - j].getIsUser():
                #create thread
                self.thread = messageThread(self.messageWidgetList[i - j].getText())
                self.thread.started.connect(self.messageStart)
                self.thread.newMessage.connect(self.recvMessage)
                self.thread.finished.connect(self.messageFinish)
                self.thread.start()
                #disable sendButton
                self.chatInput.disableSendButton()
                break
            else:
                j += 1
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def saveCurChatRecord(self, withholdCurChatFile=False):
        #init
        chatRecordStr = ''
        chatStrCount = 0
        #judge whether messageWidgetList is empty
        if len(self.messageWidgetList) != 0:
            #judge whether curChatFile is empty
            if self.curChatFile == '':
                #chatRecordFileName QString
                self.chatRecordFileName = "chat_"
                self.chatRecordFileName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
                self.chatRecordFileName += ".txt"
                #write to chatRecord file
                with open(os.path.join(chat_records_dir, self.chatRecordFileName), 'a') as f:
                    for i in range(0, self.chatShow.count()):
                        chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                        f.write(chatRecordStr)
                if not withholdCurChatFile:
                    #assign chatRecord fileName to curChatFile
                    self.curChatFile = self.chatRecordFileName
            else:
                for i in range(0, len(self.messageWidgetList)):
                    chatStrCount += self.messageWidgetList[i].getText().count('\n') + 2
                #read curChat file
                with open(os.path.join(chat_records_dir, self.curChatFile), 'r') as f:
                    lines = f.readlines()
                if chatStrCount > len(lines):
                    #clear curChat file
                    with open(os.path.join(chat_records_dir, self.curChatFile), 'w') as f:
                        f.truncate()
                    #write to curChat file
                    with open(os.path.join(chat_records_dir, self.curChatFile), 'a') as f:
                        for i in range(0, self.chatShow.count()):
                            chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                            f.write(chatRecordStr)

    def chatRecordsGenerateItem(self, searchText=''):
        #generate item
        for fileName in os.listdir(os.path.join(os.getcwd(), chat_records_dir)):
            if fileName.endswith(".txt"):
                if searchText == '':
                    with open(os.path.join(chat_records_dir, fileName), 'r') as f:
                        lines = f.readlines()
                    #create item
                    chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                    item = self.chatRecordsWidget.addListItem(chatRecordStr)
                    #item set data
                    self.chatRecordsWidget.listItemSetData(item, fileName)
                else:
                    with open(os.path.join(chat_records_dir, fileName), 'r') as f:
                        content = f.read()
                    if searchText in content:
                        with open(os.path.join(chat_records_dir, fileName), 'r') as f:
                            lines = f.readlines()
                        #create item
                        chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                        item = self.chatRecordsWidget.addListItem(chatRecordStr)
                        #item set data
                        self.chatRecordsWidget.listItemSetData(item, fileName)

    def generateCurChatRecord(self, lastIsToggle=True):
        #init
        text = ''
        isUser = True
        #read curChat file
        with open(os.path.join(chat_records_dir, self.curChatFile), 'r') as f:
            lines = f.readlines()
        #generate QListWidgetItem
        for i in range(0, len(lines)):
            if lines[i] == 'True\n' or lines[i] == 'False\n':
                if lines[i] == 'True\n':
                    isUser = True
                else:
                    isUser = False
                #messageWidget remove renewResponseButton
                j = len(self.messageWidgetList) - 1
                if j != -1 and j != 0:
                    if not self.messageWidgetList[j].getIsUser():
                        self.messageWidgetList[j].removeRenewResponseButton()
                text = text.strip('\n')
                #MessageWidget
                self.messageWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=isUser, textMaxWidth=self.chatShow.width() * 2 // 3)
                self.messageWidget.connectSetSizeFinished(self.messageWidgetResize)
                self.messageWidget.connectSetTexting(self.getSetTexting)
                if not isUser:
                    self.messageWidget.removeLoadingWidget()
                self.messageWidgetList.append(self.messageWidget)
                #itemWidget QWidget
                self.itemWidget = ItemWidget(self)
                self.itemHLayout = QHBoxLayout()
                self.itemHLayout.addWidget(self.messageWidget)
                self.itemWidget.setLayout(self.itemHLayout)
                self.itemWidget.setFixedSize(self.chatShow.width(), self.messageWidget.height() + 10)
                if isUser:
                    self.itemHLayout.setContentsMargins(self.itemWidget.width() - self.messageWidget.width() - 25, 5, 25, 5)
                else:
                    self.itemHLayout.setContentsMargins(0, 5, self.itemWidget.width() - self.messageWidget.width(), 5)
                #QListWidgetItem
                self.item = QListWidgetItem(self.chatShow)
                self.item.setSizeHint(QSize(self.chatShow.width(), self.messageWidget.height() + 10))
                self.chatShow.setItemWidget(self.item, self.itemWidget)
                #MessageWidget
                if i == len(lines) - 1:
                    if lastIsToggle:
                        self.messageWidget.toggleWidget()
                else:
                    self.messageWidget.toggleWidget()
                #clear text
                text = ''
            else:
                text += lines[i]

    def getSetTexting(self, state):
        self.isSetTexting = state
        return self.isSetTexting

    def onResizeTimeout(self):
        if len(self.messageWidgetList) != 0:
            if not self.isSetTexting:
                self.current_scroll_value = self.chatShow.verticalScrollBar().value()
                self.max_scroll_value = self.chatShow.verticalScrollBar().maximum()
            self.saveCurChatRecord()
            self.messageWidgetList.clear()
            for i in range(0, self.chatShow.count()):
                itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
                itemWidget.deleteLater()
            self.chatShow.clear()
            if not self.isSetTexting:
                self.generateCurChatRecord()
                QTimer.singleShot(5, self.setScrollValue)
            else:
                self.generateCurChatRecord(lastIsToggle=False)
                self.messageRecvWidget = self.messageWidget
                self.itemRecvHLayout = self.itemHLayout
                self.itemRecvWidget = self.itemWidget
                self.recvItem = self.item
            if self.messageWidgetIsSelect:
                self.messageWidgetList[self.selectMessageWidgetNumber].showColorful()

    def setScrollValue(self):
        new_max_scroll_value = self.chatShow.verticalScrollBar().maximum()
        self.chatShow.verticalScrollBar().setValue(int(self.current_scroll_value / self.max_scroll_value * new_max_scroll_value))

    def showChatRecords(self):
        if not self.chatRecordsWidgetIsOpen:
            if not self.settingWidgetIsOpen:
                self.saveCurChatRecord()
                self.chatRecordsGenerateItem()
                #show chatRecordsWidget
                self.chatRecordsWidget.raise_()
                self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
                self.chatRecordsAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                self.chatRecordsAnimationMove.start()
                self.chatRecordsWidgetIsOpen = True
                self.chatRecordsIsTop = True
            else:
                self.saveCurChatRecord()
                self.chatRecordsGenerateItem()
                #show chatRecordsWidget
                self.chatRecordsWidget.raise_()
                self.chatRecordsAnimationMove2.setStartValue(self.chatRecordsWidget.geometry())
                self.chatRecordsAnimationMove2.setEndValue(QRect(0, self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                self.chatRecordsAnimationMove2.start()
                self.chatRecordsWidgetIsOpen = True
                self.chatRecordsIsTop = True
                self.settingIsTop = False
            self.chatRecordsFoldButton.raise_()
            self.chatRecordsFoldButton.show()
        else:
            if self.chatRecordsIsTop:
                if not self.settingWidgetIsOpen:
                    self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
                    self.chatRecordsAnimationMove.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                    self.chatRecordsAnimationMove.start()
                    self.chatRecordsWidgetIsOpen = False
                    self.chatRecordsIsTop = False
                else:
                    self.chatRecordsAnimationMove2.setStartValue(self.chatRecordsWidget.geometry())
                    self.chatRecordsAnimationMove2.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                    self.chatRecordsAnimationMove2.start()
                    self.chatRecordsWidgetIsOpen = False
                    self.chatRecordsIsTop = False
                    self.settingIsTop = True
            else:
                self.chatRecordsWidget.raise_()
                self.chatRecordsIsTop = True
                self.settingIsTop = False
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def showSearchRecords(self):
        text = self.chatRecordsWidget.getLineEditText()
        self.chatRecordsWidget.delAllListItems()
        self.chatRecordsGenerateItem(searchText=text)

    def clearAllChatRecords(self):
        self.chatRecordsWidget.delAllListItems()
        for fileName in os.listdir(os.path.join(os.getcwd(), chat_records_dir)):
            if fileName.endswith(".txt"):
                filePath = os.path.join(os.path.join(os.getcwd(), chat_records_dir), fileName)
                os.remove(filePath)

    def generateChatRecord(self, item):
        #clear
        self.messageWidgetList.clear()
        for i in range(0, self.chatShow.count()):
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.deleteLater()
        self.chatShow.clear()
        #assign chatRecord fileName to curChatFile
        self.curChatFile = self.chatRecordsWidget.listItemToString(item)
        self.generateCurChatRecord()

    def newChat(self):
        self.saveCurChatRecord()
        #clear
        self.messageWidgetList.clear()
        for i in range(0, self.chatShow.count()):
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.deleteLater()
        self.chatShow.clear()
        self.curChatFile = ''
        #pushButtonIsPress
        self.pushButtonIsPress = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont(font_file_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
            font = QFont(font_family, windowFontSize)
            QApplication.setFont(font)
    app.setStyleSheet('''
    QToolTip{
        border: none;
        border-radius: 10px;
        color: white;
        background: #404040;
    }
    ''')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
