# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:31:44 2024

@author: YXD
"""

import sys, os
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QAbstractSpinBox, QGridLayout, QLineEdit, QSplitter, QToolTip, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve, QEvent, QPoint, pyqtProperty, QTimer, QCoreApplication, QUrl
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen, QCursor, QFontDatabase, QMouseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from openai import OpenAI
import math
import mistune
import time

base_url = "http://7613907zg6.vicp.fun:45861/v1"
client = OpenAI(api_key="EMPTY", base_url=base_url)

maxTokens_minimum = 0
maxTokens_maximum = 32768
maxTokens_currentVal = 256
topP_minimum = 0
topP_maximum = 1
topP_currentVal = 0.8
topP_singleStep = 0.01
temperature_minimum = 0.01
temperature_maximum = 1
temperature_currentVal = 0.8
temperature_singleStep = 0.01

# 定义 Markdown 内容
markdown_content = """
一级标题
========
二级标题
--------
------------------
# 一级标题
## 二级标题
### 三级标题
这是一个段落，包含一些 *Markdown* 语法。  
*斜体文本*  
_斜体文本_  
**粗体文本**  
__粗体文本__  
***粗斜体文本***  
___粗斜体文本___  
~~删除线文本~~  
<u>带下划线文本</u>  
苹果10$，梨子20$，香蕉30$，橘子40$。  
苹果10\$，梨子20\$，香蕉30\$，橘子40\$。  

创建脚注格式类似这样 [^RUNOOB]。  
[^RUNOOB]: 菜鸟教程 -- 学的不仅是技术，更是梦想！！！  

******************
$\alpha$ $\beta$ $\gamma$ $\delta$ $\epsilon$ $\zeta$ $\eta$ $\theta$ $\iota$ $\kappa$ $\lambda$  
$\mu$ $\nu$ $\omicron$ $\pi$ $\rho$ $\sigma$ $\tau$ $\phi$ $\chi$ $\psi$ $\omega$ $\Gamma$ $\Delta$  
$\Theta$ $\Lambda$ $\Xi$ $\Pi$ $\Sigma$ $\Phi$ $\Psi$ $\Omega$  
******************
### 无序列表
* 第一项
* 第二项
* 第三项

+ 第一项
+ 第二项
+ 第三项

- 第一项
- 第二项
- 第三项

### 有序列表
1. 第一项
2. 第二项
3. 第三项

### 列表嵌套
1. 第一项
    - 第一项嵌套的第一个元素
    - 第一项嵌套的第二个元素
2. 第二项
    1. 第二项嵌套的第一个元素
    2. 第二项嵌套的第二个元素
******************
### 区块
> 菜鸟教程
> 学的不仅是技术更是梦想

> 最外层
> > 第一层嵌套
> > > 第二层嵌套

> 区块中使用列表
> 1. 第一项
> 2. 第二项
> + 第一项
> + 第二项
> + 第三项

列表中使用区块
* 第一项
    > 菜鸟教程
    > 学的不仅是技术更是梦想
* 第二项
******************
### 代码
`printf()`函数

    def printHelloWorld():
        print('hello world')

```python:
def printHelloWorld():
    print('hello world')
```
******************
### 链接
这是一个链接 [菜鸟教程](https://www.runoob.com)  
这个链接用 1 作为网址变量 [Baidu][1]  
这个链接用 runoob 作为网址变量 [Runoob][runoob]  
然后在文档的结尾为变量赋值（网址）  

[1]: http://www.baidu.com/  
[runoob]: http://www.runoob.com/  
******************
### 图片
![RUNOOB 图标](https://static.jyshare.com/images/runoob-logo.png "RUNOOB")

这个链接用 2 作为网址变量 [RUNOOB][2]  
然后在文档的结尾为变量赋值（网址）  

[2]: https://static.jyshare.com/images/runoob-logo.png

<img src="https://static.jyshare.com/images/runoob-logo.png" width="25%">

******************
### 表格
| 表头 | 表头 | 表头 |  
| :--- | ---: | :---: |  
| 单元格 | 单元格 | 单元格 |  
| 单元格 | 单元格 | 单元格 |  
******************
### LaTeX公式：
这是一个行内公式 $E=mc^2$ 的示例。  
行间公式：
$$\sum_{i=1}^n a_i$$
$$\frac{a}{b} = c$$
积分公式：
$$\int_{a}^{b} {f(x)} \, \mathrm{d}x = F(b) - F(a)$$
微分公式：
$$\frac{d}{dx} e^x = e^x$$
"""

'''class messageThread(QThread):
    newMessage = pyqtSignal(str)

    def __init__(self, contentInput, use_stream=True, parent=None):
        super(messageThread, self).__init__(parent)
        self.text = [
            {
                "role": "user",
                "content": contentInput
            }
        ]
        self.use_stream = use_stream

    def run(self):
        response = client.chat.completions.create(
            model="qwen2.5:14b",
            messages=self.text,
            stream=self.use_stream,
            max_tokens=maxTokens_currentVal,
            temperature=temperature_currentVal,
            presence_penalty=1.1,
            top_p=topP_currentVal
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
        return'''
class messageThread(QThread):
    newMessage = pyqtSignal(str)

    def __init__(self, contentInput, use_stream=True, parent=None):
        super(messageThread, self).__init__(parent)
        self.text = [
            {
                "role": "user",
                "content": contentInput
            }
        ]
        self.use_stream = use_stream

    def run(self):
        self.contentOutput = markdown_content
        if self.use_stream:
            """ for _ in range(0, 100):
                self.newMessage.emit(self.contentOutput)
                time.sleep(0.1) """
            """ for i in range(0, len(self.contentOutput), 10):
                self.newMessage.emit(self.contentOutput[i:i+10])
                time.sleep(0.1) """
            self.newMessage.emit('# 一级标题## 二级标题### 三级标题')
        else:
            self.newMessage.emit(self.contentOutput)
        return

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
        #settingButton PushButton
        self.settingButton = PushButton(tipText='设置', tipOffsetX=10, tipOffsetY=40)
        self.settingButton.setFixedSize(30, 30)
        self.settingButton.setIconSize(QSize(30, 30))
        self.settingButton.setStyleSheet('''
        QPushButton{
            border-image: url("setting.png");
        }
        QPushButton:hover{
            border-image: url("setting_hover.png");
        }
        ''')
        #cutButton PushButton
        self.cutButton = PushButton(tipText='界面截图', tipOffsetX=30, tipOffsetY=40)
        self.cutButton.setFixedSize(30, 30)
        self.cutButton.setIconSize(QSize(30, 30))
        self.cutButton.setStyleSheet('''
        QPushButton{
            border-image: url("cut.png");
        }
        QPushButton:hover{
            border-image: url("cut_hover.png");
        }
        ''')
        #chatRecordsButton PushButton
        self.chatRecordsButton = PushButton(tipText='聊天历史', tipOffsetX=30, tipOffsetY=40)
        self.chatRecordsButton.setFixedSize(30, 30)
        self.chatRecordsButton.setIconSize(QSize(30, 30))
        self.chatRecordsButton.setStyleSheet('''
        QPushButton{
            border-image: url("chat_records.png");
        }
        QPushButton:hover{
            border-image: url("chat_records_hover.png");
        }
        ''')
        #newChatButton PushButton
        self.newChatButton = PushButton(tipText='新聊天', tipOffsetX=20, tipOffsetY=40)
        self.newChatButton.setFixedSize(30, 30)
        self.newChatButton.setIconSize(QSize(30, 30))
        self.newChatButton.setStyleSheet('''
        QPushButton{
            border-image: url("new_chat.png");
        }
        QPushButton:hover{
            border-image: url("new_chat_hover.png");
        }
        ''')
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.mainHLayout.addWidget(self.settingButton)
        self.mainHLayout.addWidget(self.cutButton)
        self.mainHLayout.addWidget(self.chatRecordsButton)
        self.mainHLayout.addWidget(self.newChatButton)
        self.mainHLayout.setAlignment(Qt.AlignLeft)
        self.mainHLayout.setContentsMargins(3, 3, 3, 3)
        self.mainHLayout.setSpacing(2)
        #FunWidget adjust size
        self.resize(1200, 36)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(200, 200, 200))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def connectSettingButtonClick(self, fun):
        self.settingButton.clicked.connect(fun)

    def connectCutButtonClick(self, fun):
        self.cutButton.clicked.connect(fun)

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

    def mouseMoveEvent(self, event):
        QListWidget.mouseMoveEvent(self, event)
        event.ignore()

    def mousePressEvent(self, event):
        QListWidget.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QListWidget.mouseReleaseEvent(self, event)
        event.ignore()

    def resizeEvent(self, event):
        return

    def toList(self, sourceList):
        self.messageWidgetList = sourceList

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
        self.sendButton.setStyleSheet('''
        QPushButton{
            border: none;
            image: url("send.png");
        }
        QPushButton:disabled{
            border: none;
            image: url("send_disable.png");
        }
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
            self.sendButton.setStyleSheet('''
            QPushButton{
                border: none;
                image: url("send.png");
            }
            QPushButton:disabled{
                border: none;
                image: url("send_disable.png");
            }
            ''')
        else:
            self.sendButton.setStyleSheet('''
            QPushButton{
                border: none;
                image: url("send_hover.png");
            }
            QPushButton:disabled{
                border: none;
                image: url("send_disable.png");
            }
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
        self.BGColor = QColor(224, 224, 224)
        #AnimationBackgroundColor QPropertyAnimation
        self.AnimationBackgroundColor = QPropertyAnimation(self, b'backgroundColor')
        self.AnimationBackgroundColor.setDuration(400)
        self.AnimationBackgroundColor.setEasingCurve(QEasingCurve.OutQuad)
        #border color
        self.BColor = QColor(100, 100, 100, 0)
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
            self.AnimationBackgroundColor.setStartValue(QColor(224, 224, 224))
            self.AnimationBackgroundColor.setEndValue(QColor(224, 224, 224, 0))
            self.AnimationBackgroundColor.start()
            self.AnimationBorderColor.setStartValue(QColor(100, 100, 100, 0))
            self.AnimationBorderColor.setEndValue(QColor(100, 100, 100))
            self.AnimationBorderColor.start()

    def backgroundColorShowDark(self):
        if self.backgroundColorIsLight:
            self.backgroundColorIsLight = False
            self.AnimationBackgroundColor.setStartValue(QColor(224, 224, 224, 0))
            self.AnimationBackgroundColor.setEndValue(QColor(224, 224, 224))
            self.AnimationBackgroundColor.start()
            self.AnimationBorderColor.setStartValue(QColor(100, 100, 100))
            self.AnimationBorderColor.setEndValue(QColor(100, 100, 100, 0))
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
        if isUser:
            self.setPixmap(QPixmap("user.png"))
        else:
            self.setPixmap(QPixmap("ai.png"))

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
        if obj == self.focusProxy() and  event.type() == QEvent.MouseButtonPress:
            newMouseEvent = QMouseEvent(event.type(), event.pos(), event.button(), event.buttons(), event.modifiers())
            QCoreApplication.postEvent(obj.parent(), newMouseEvent)
        return QWebEngineView.eventFilter(self, obj, event)

    def connectPageLoadFinished(self, fun):
        self.page().loadFinished.connect(fun)

class CustomLabel(QLabel):
    textSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        QLabel.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.hasSelectedText():
                self.textSelected.emit(self.selectedText())
        QLabel.mouseReleaseEvent(self, event)
        event.ignore()

class TextShow(QWidget):
    setSizeFinished = pyqtSignal()

    def __init__(self, text, isUser=True, maxWidth=650, parent=None):
        super(TextShow, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = CustomLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        self.font.setPixelSize(22)
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)

        self.webEngineView = WebEngineView()
        self.webEngineView.connectPageLoadFinished(self.onPageLoadFinished)
        self.mainHLayout = QHBoxLayout()
        self.webEngineView.setMaximumWidth(self.maxWidth)

        self.isLabel = True
        if not self.text == '':
            print('textShow:', self.text)
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
            self.label.setFixedSize(22, 22)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(32, 32)
        self.isUser = isUser
        self.isColorful = False

    def onPageLoadFinished(self, success):
        js = """
        function getPageHeight() {
            var body = document.body;
            var html = document.documentElement;
            var height = Math.max(body.scrollHeight, body.offsetHeight,
                                html.clientHeight, html.scrollHeight, html.offsetHeight);
            return height;
        }
        getPageHeight();
        """
        if success:
            """ self.webEngineView.show() """
            self.webEngineView.page().runJavaScript("document.body.style.overflow = 'hidden';")
            self.webEngineView.page().runJavaScript(js, self.adjustSize)
            """ QTimer.singleShot(1, self.setSize) """
            """ self.setSize() """

    def adjustSize(self, height):
        print('height:', height)
        if height != 0:
            self.webEngineView.setFixedHeight(height)
            print(self.label.parent())
            if self.label:
                self.mainHLayout.removeWidget(self.label)
                self.label.deleteLater()
                self.mainHLayout.addWidget(self.webEngineView)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            self.setSizeFinished.emit()
            print('view_size:', self.webEngineView.width(), self.webEngineView.height())
        for i in range(self.mainHLayout.count()):
            item = self.mainHLayout.itemAt(i)
            print(item.widget())

    """ def setSize(self):
        width = self.webEngineView.page().contentsSize().toSize().width()
        height = self.webEngineView.page().contentsSize().toSize().height()
        print('width:', width, 'height:', height)
        if  width != 0 and  height != 0:
            self.webEngineView.setFixedSize(width, height)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10)
            self.setSizeFinished.emit()
        else:
            QTimer.singleShot(1, self.setSize) """

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
            brush.setColor(QColor(119, 221, 255))
        else:
            if self.isUser:
                brush.setColor(QColor(255, 238, 153))
            else:
                brush.setColor(QColor(209, 187, 255))
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

    def toggleWidget(self):
        self.isLabel = False

        markdown_content = ''
        self.html_text = ''
        self.full_html_text = ''
        initWidth = self.font_metrics.width(self.text) + 16
        if initWidth > self.maxWidth:
            self.webEngineView.setFixedSize(self.maxWidth, math.ceil(self.font_metrics.width(self.text) / (self.maxWidth - 16)) * 29 + 44)
            """ self.webEngineView.setFixedWidth(self.maxWidth) """
        else:
            if self.text == '':
                self.webEngineView.setFixedSize(38, 73)
            else:
                self.webEngineView.setFixedSize(int(initWidth), 73)
                """ self.webEngineView.setFixedWidth(int(initWidth)) """
        # 添加 MathJax CDN 链接到 HTML 头部
        self.mathjax_cdn = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                <script type="text/javascript" async
                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.1.2/es5/tex-mml-chtml.js">
                </script>
                <style>
                    table {
                        width: 50%;
                        border-collapse: collapse;
                        margin: 10px 0;
                    }  
                    th, td {
                        border: 1px solid #000;
                        padding: 8px;
                    }
                    th {
                        background-color: #b0b0b0;
                    }
                    .left-align { text-align: left; }
                    .center-align { text-align: center; }
                    .right-align { text-align: right; }
                </style>
                <style>  
                    body { font-size: 22px; }
                </style>
            </head>
        """
        self.markdown = mistune.create_markdown(escape=False, renderer='html')

        if not self.text == '':
            tableText, tableItemList, tableAlignList, row, column, tableIsComplete= self.getTable(self.text)
            if tableIsComplete:
                textList = self.text.split(tableText, 1)
                markdown_content = textList[0].replace('\$', '\\\$')
                markdown_content = markdown_content.replace('\frac', '\\frac')
                markdown_content = markdown_content.replace('\,', '\\\,')
                markdown_content = markdown_content.replace('\alpha', '\\alpha')
                markdown_content = markdown_content.replace('\beta', '\\beta')
                markdown_content = markdown_content.replace('\theta', '\\theta')
                markdown_content = markdown_content.replace('\nu', '\\nu')
                markdown_content = markdown_content.replace('\rho', '\\rho')
                markdown_content = markdown_content.replace('\tau', '\\tau')
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
                markdown_content = textList[1].replace('\$', '\\\$')
                markdown_content = markdown_content.replace('\frac', '\\frac')
                markdown_content = markdown_content.replace('\,', '\\\,')
                markdown_content = markdown_content.replace('\alpha', '\\alpha')
                markdown_content = markdown_content.replace('\beta', '\\beta')
                markdown_content = markdown_content.replace('\theta', '\\theta')
                markdown_content = markdown_content.replace('\nu', '\\nu')
                markdown_content = markdown_content.replace('\rho', '\\rho')
                markdown_content = markdown_content.replace('\tau', '\\tau')
                # 使用 mistune 将 Markdown 转换为 HTML
                self.html_text += self.markdown(markdown_content)
            else:
                markdown_content = self.text.replace('\$', '\\\$')
                markdown_content = markdown_content.replace('\frac', '\\frac')
                markdown_content = markdown_content.replace('\,', '\\\,')
                markdown_content = markdown_content.replace('\alpha', '\\alpha')
                markdown_content = markdown_content.replace('\beta', '\\beta')
                markdown_content = markdown_content.replace('\theta', '\\theta')
                markdown_content = markdown_content.replace('\nu', '\\nu')
                markdown_content = markdown_content.replace('\rho', '\\rho')
                markdown_content = markdown_content.replace('\tau', '\\tau')
                # 使用 mistune 将 Markdown 转换为 HTML
                self.html_text = self.markdown(markdown_content)
            # 将转换后的 HTML 内容添加到 body 中
            self.full_html_text = f"{self.mathjax_cdn}<body>\n{self.html_text}\n</body>\n</html>\n"

            print(self.text)
            print('subWidget count:', self.mainHLayout.count())

            self.webEngineView.setHtml(str(self.full_html_text))

    def setText(self, text):
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
            self.label.setFixedSize(22, 22)
            self.setFixedSize(32, 32)

    def setMaxWidth(self, maxWidth):
        if self.isLabel:
            self.maxWidth = maxWidth
            self.label.setMaximumWidth(self.maxWidth)
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
                self.label.setFixedSize(22, 22)
                self.setFixedSize(32, 32)
        else:
            self.maxWidth = maxWidth
            self.webEngineView.setMaximumWidth(self.maxWidth)
            """ initWidth = self.font_metrics.width(self.text) + 16 """
            """ if initWidth > self.maxWidth:
                self.webEngineView.setFixedWidth(self.maxWidth) """
            """ self.webEngineView.resize(self.maxWidth, math.ceil(self.font_metrics.width(self.text) / (self.maxWidth - 16)) * 29 + 44) """
            """ else:
                self.webEngineView.setFixedWidth(int(initWidth)) """
            """ self.webEngineView.resize(int(initWidth), 73) """
            if not self.text == '':
                self.webEngineView.setHtml(str(self.full_html_text))
            """ self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height() + 10) """

    def getWebEngineView(self):
        return self.webEngineView

    def hasSelectedText(self):
        return self.webEngineView.hasSelection()

    def getSelectedText(self):
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
    def __init__(self, text, copyFun, renewResponseFun, isUser=True, textMaxWidth=780, parent=None):
        super(MessageWidget, self).__init__(parent)
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
        self.copyButton.setStyleSheet('''
        QPushButton{
            border-image: url("copy.png");
        }
        QPushButton:hover{
            border-image: url("copy_hover.png");
        }
        ''')
        self.copyButton.clicked.connect(copyFun)
        #renewResponseButton PushButton
        self.renewResponseButton = PushButton(tipText='重新生成响应', tipOffsetX=50, tipOffsetY=40)
        self.renewResponseButton.setFixedSize(16, 16)
        self.renewResponseButton.setStyleSheet('''
        QPushButton{
            border-image: url("renewResponse.png");
        }
        QPushButton:hover{
            border-image: url("renewResponse_hover.png");
        }
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

        """ self.textShow.setSizeFinished.connect(self.toggleWidget) """
        """ self.sizeFinishedFlag = False """

    def toggleWidget(self):
        self.textShow.toggleWidget()

    def connectSetSizeFinished(self, fun):
        self.textShow.setSizeFinished.connect(fun)

    """ def setSizeFinishedFlag(self):
        self.sizeFinishedFlag = True """

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
        """ if self.sizeFinishedFlag:
            self.textLayout.removeWidget(self.textShow)
            self.textShow.deleteLater()
            self.textShow = TextShow(self.text, isUser=self.isUser, maxWidth=self.textMaxWidth)
            if self.isUser:
                self.textLayout.removeWidget(self.funWidget)
                self.textLayout.addWidget(self.textShow)
                self.textLayout.addWidget(self.funWidget)
                self.textLayout.setSpacing(0)
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            else:
                if self.loadingWidgetIsRemove:
                    self.textLayout.removeWidget(self.funWidget)
                    self.textLayout.addWidget(self.textShow)
                    self.textLayout.addWidget(self.funWidget)
                    self.textLayout.setSpacing(0)
                    self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
                else:
                    self.textLayout.removeWidget(self.loadingWidget)
                    self.textLayout.addWidget(self.textShow)
                    self.textLayout.addWidget(self.loadingWidget)
                    self.textLayout.setSpacing(0)
                    self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height()) """

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

    def setTextMaxWidth(self, textMaxWidth):
        self.textMaxWidth = textMaxWidth
        self.textShow.setMaxWidth(textMaxWidth)
        """ if self.sizeFinishedFlag:
            self.textLayout.removeWidget(self.textShow)
            self.textShow.deleteLater()
            self.textShow = TextShow(self.text, isUser=self.isUser, maxWidth=self.textMaxWidth)
            if self.isUser:
                self.textLayout.removeWidget(self.funWidget)
                self.textLayout.addWidget(self.textShow)
                self.textLayout.addWidget(self.funWidget)
                self.textLayout.setSpacing(0)
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            else:
                if self.loadingWidgetIsRemove:
                    self.textLayout.removeWidget(self.funWidget)
                    self.textLayout.addWidget(self.textShow)
                    self.textLayout.addWidget(self.funWidget)
                    self.textLayout.setSpacing(0)
                    self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
                else:
                    self.textLayout.removeWidget(self.loadingWidget)
                    self.textLayout.addWidget(self.textShow)
                    self.textLayout.addWidget(self.loadingWidget)
                    self.textLayout.setSpacing(0)
                    self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height()) """

        if self.isUser:
            self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
        else:
            if self.loadingWidgetIsRemove:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.funWidget.width() else self.funWidget.width(), self.textShow.height() + self.funWidget.height())
            else:
                self.textWidget.setFixedSize(self.textShow.width() if self.textShow.width() > self.loadingWidget.width() else self.loadingWidget.width(), self.textShow.height() + self.loadingWidget.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

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
        self.font.setPixelSize(22)
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
            self.label.resize(22, 22)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(32, 32)
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
            self.label.resize(22, 22)
            self.setFixedSize(32, 32)

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
        self.font.setPixelSize(22)
        self.font.setBold(True)
        self.setFont(self.font)
        self.palette = self.palette()
        self.palette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.setPalette(self.palette)

class SpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(SpinBox, self).__init__(parent)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setStyleSheet('''
        QSpinBox{
            border: 2px solid rgb(23, 171, 227);
            border-radius: 8px;
            background: transparent;
            font: 22px, bold;
            color: rgb(23, 171, 227);
            selection-background-color: rgb(23, 171, 227);
        }
        QSpinBox::up-button{
            width: 16px;
            height: 16px;
            border-image: url("up_arrow.png");
        }
        QSpinBox::up-button:pressed{
            margin-top: 1px;
        }
        QSpinBox::down-button{
            width: 16px;
            height: 16px;
            border-image: url("down_arrow.png");
        }
        QSpinBox::down-button:pressed{
            margin-bottom: 1px;
        }
        ''')

    def mousePressEvent(self, event):
        QSpinBox.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QSpinBox.mouseReleaseEvent(self, event)
        event.ignore()

    def enterEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def leaveEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setStyleSheet('''
        QDoubleSpinBox{
            border: 2px solid rgb(23, 171, 227);
            border-radius: 8px;
            background: transparent;
            font: 22px, bold;
            color: rgb(23, 171, 227);
            selection-background-color: rgb(23, 171, 227);
        }
        QDoubleSpinBox::up-button{
            width: 16px;
            height: 16px;
            border-image: url("up_arrow.png");
        }
        QDoubleSpinBox::up-button:pressed{
            margin-top: 1px;
        }
        QDoubleSpinBox::down-button{
            width: 16px;
            height: 16px;
            border-image: url("down_arrow.png");
        }
        QDoubleSpinBox::down-button:pressed{
            margin-bottom: 1px;
        }
        ''')

    def mousePressEvent(self, event):
        QDoubleSpinBox.mousePressEvent(self, event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        QDoubleSpinBox.mouseReleaseEvent(self, event)
        event.ignore()

    def enterEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def leaveEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

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
        font_file_path = 'msyhl.ttc'
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
        self.searchButton.setIcon(QIcon("search.png"))
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
        font_file_path = 'msyhl.ttc'
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, 10)
        #LineEdit
        self.lineEdit = LineEdit()
        #clearAllButton QPushButton
        self.clearAllButton = PushButton(tipText='删除所有记录', tipOffsetX=50, tipOffsetY=40)
        self.clearAllButton.setFixedSize(30, 30)
        self.clearAllButton.setIconSize(QSize(30, 30))
        self.clearAllButton.setStyleSheet('''
        QPushButton{
            border: none;
            border-radius: 5px;
            background: #e0e0e0;
            image: url("clearAll.png");
        }
        QPushButton:hover{
            background: #b8b8b8;
            image: url("clearAll_hover.png");
        }
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
        #QLabel
        self.label = QLabel()
        self.label.resize(self.width() - 40, 50)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        font = QFont()
        font.setPixelSize(30)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setText("聊天历史")
        self.label.setAlignment(Qt.AlignLeft)
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
        self.mainVLayout.addWidget(self.label)
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
        path.addRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
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
        self.resize(1200, 800)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        #mouseLeftButtonIsPress
        self.mouseLeftButtonIsPress = False
        #RegionEnum
        self.regionDir = RegionEnum.MIDDLE
        #padding
        self.padding = 2
        #mask
        self.mask = QWidget(self)
        self.mask.setFixedSize(self.width(), self.height())
        self.mask.setStyleSheet('''
        QWidget{
            background: rgba(220, 220, 220, 50%);
        }
        ''')
        self.mask.raise_()
        self.mask.hide()
        #title QWidget init
        self.titleWidgetInit()
        #FunWidget
        self.chatFun = FunWidget()
        self.chatFun.connectSettingButtonClick(self.settingButtonClicked)
        self.chatFun.connectCutButtonClick(self.saveImage)
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
        #mainWidget QWidget
        self.mainWidget = Widget()
        self.mainWidget.resize(1200, 800)
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.titleWidget)
        self.mainVLayout.addWidget(self.contentWidget)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        self.mainVLayout.setStretch(0, 0)
        self.mainVLayout.setStretch(1, 1)
        #MainWindow
        self.setCentralWidget(self.mainWidget)
        #messageWidget list
        self.messageWidgetList = []
        self.chatShow.toList(self.messageWidgetList)
        #setting QWidget init
        self.settingWidgetInit()
        #ChatRecordsWidget
        self.chatRecordsWidget = ChatRecordsWidget(self)
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
        self.chatRecordsAnimationMove.finished.connect(self.chatRecordsMoveFinished)
        #settingWidgetIsOpen
        self.chatRecordsWidgetIsOpen = False
        #emptyTextLabel PrintLabel
        self.emptyTextLabel = PrintLabel('文本不能为空', self)
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.emptyTextLabel.height() - 10)
        self.emptyTextLabel.raise_()
        self.emptyTextLabel.hide()
        #saveImageLabel PrintLabel
        self.saveImageLabel = PrintLabel('', self)
        self.saveImageLabel.move((self.width() - self.saveImageLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.saveImageLabel.height() - 10)
        self.saveImageLabel.raise_()
        self.saveImageLabel.hide()
        #textCopyLabel PrintLabel
        self.textCopyLabel = PrintLabel('文本复制成功', self)
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.textCopyLabel.height() - 10)
        self.textCopyLabel.raise_()
        self.textCopyLabel.hide()

    def mouseMoveEvent(self, event):
        #If the mouse hovers over the list item, it has a pop-up effect
        self.isItemShowFull(self.childAt(event.pos()))
        #Stretch and drag the UI by dragging the mouse
        self.cursorGlobalPos = event.globalPos()
        self.cursorGlobalX = self.cursorGlobalPos.x()
        self.cursorGlobalY = self.cursorGlobalPos.y()
        self.uiGlobalTL = self.geometry().topLeft()
        self.uiGlobalBR = self.geometry().bottomRight()
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
        self.setGeometry(uiGlobalRect)

    def UiDrag(self, globalPos):
        self.move(self.pressPosDistanceUiGlobalTL + globalPos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonIsPress = True
            #title region calculate the distance to move
            if self.regionDir == RegionEnum.TITLE:
                self.pressPosDistanceUiGlobalTL = self.geometry().topLeft() - event.globalPos()
            #judge mouse press position
            if self.settingWidgetIsOpen:
                notSettingRect = QRect(self.settingWidget.width(), self.titleWidget.height(), self.width() - self.settingWidget.width() - self.padding - 1, self.height() - self.titleWidget.height() - self.padding - 1)
                if notSettingRect.contains(event.pos()):
                    self.mask.hide()
                    self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
                    self.settingAnimationMove.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                    self.settingAnimationMove.start()
                    self.settingWidgetIsOpen = False
            elif self.chatRecordsWidgetIsOpen:
                notChatRecordsRect = QRect(self.chatRecordsWidget.width(), self.titleWidget.height(), self.width() - self.chatRecordsWidget.width() - self.padding - 1, self.height() - self.titleWidget.height() - self.padding - 1)
                if notChatRecordsRect.contains(event.pos()):
                    self.mask.hide()
                    self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
                    self.chatRecordsAnimationMove.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                    self.chatRecordsAnimationMove.start()
                    self.chatRecordsWidgetIsOpen = False
            else:
                chatShowRect = QRect(self.chatShow.geometry().x(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                if not chatShowRect.contains(event.pos()):
                    for i in range(0, len(self.messageWidgetList)):
                        self.messageWidgetList[i].showDefaultColor()
                else:
                    widget = self.childAt(event.pos())
                    if isinstance(widget, CopyButton):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            messageWidget.showDefaultColor()
                            if widget == messageWidget.getCopyButton():
                                messageWidget.showColorful()
                    elif isinstance(widget.parent(), WebEngineView):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            messageWidget.showDefaultColor()
                            if widget.parent() == messageWidget.getTextShow().getWebEngineView():
                                messageWidget.showColorful()
                chatInputRect = QRect(self.chatInput.geometry().x(), self.chatInput.geometry().y() + self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height(), self.chatInput.geometry().width(), self.chatInput.geometry().height())
                if chatInputRect.contains(event.pos()):
                    self.chatInput.backgroundColorShowLight()
                else:
                    self.chatInput.backgroundColorShowDark()
                    self.chatInput.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonIsPress = False
        QMainWindow.mouseReleaseEvent(self, event)

    def resizeEvent(self, event):
        #mask adjust size
        self.mask.setFixedSize(self.width(), self.height())
        #setting widget set geometry
        self.settingWidget.resize(self.width() // 3, self.height() - self.titleWidget.height())
        if self.settingWidgetIsOpen:
            self.chatShow.resize(self.width() * 2 // 3 - 29, self.chatShow.height())
            self.chatShowWidget.resize(self.width() * 2 // 3, self.chatShowWidget.height())
            self.chatInput.resize(self.width() * 2 // 3 - 40, self.chatInput.height())
            self.chatInput.resetWidgetSize()
            self.chatInputWidget.resize(self.width() * 2 // 3, self.chatInputWidget.height())
            self.splitter.resize(self.width() * 2 // 3, self.splitter.height())
            self.contentVLayout.setContentsMargins(self.width() // 3, 0, 0, 0)
        else:
            self.settingWidget.move(-self.settingWidget.width(), self.titleWidget.height())
        #chatRecords widget set geometry
        self.chatRecordsWidget.resetWidgetSize(self.width() // 3, self.height() - self.titleWidget.height())
        if self.chatRecordsWidgetIsOpen:
            self.chatShow.resize(self.width() * 2 // 3 - 29, self.chatShow.height())
            self.chatShowWidget.resize(self.width() * 2 // 3, self.chatShowWidget.height())
            self.chatInput.resize(self.width() * 2 // 3 - 40, self.chatInput.height())
            self.chatInput.resetWidgetSize()
            self.chatInputWidget.resize(self.width() * 2 // 3, self.chatInputWidget.height())
            self.splitter.resize(self.width() * 2 // 3, self.splitter.height())
            self.contentVLayout.setContentsMargins(self.width() // 3, 0, 0, 0)
        else:
            self.chatRecordsWidget.move(-self.chatRecordsWidget.width(), self.titleWidget.height())
        #TextShow max width
        textMaxWidth = self.chatShow.width() * 2 // 3
        for i in range(0, self.chatShow.count()):
            #messageWidget set max width of text
            messageWidget = self.messageWidgetList[i]
            messageWidget.setTextMaxWidth(textMaxWidth)
            #chatShow itemWidget adjust size
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            if messageWidget.getIsUser():
                itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
            else:
                itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))
        #TextEditFull adjust size
        self.chatInput.resetWidgetSize()
        #move emptyTextLabel
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.emptyTextLabel.height() - 10)
        #move saveImageLabel
        self.saveImageLabel.move((self.width() - self.saveImageLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.saveImageLabel.height() - 10)
        #move textCopyLabel
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.textCopyLabel.height() - 10)

    def itemShowColorful(self, item):
        for i in range(0, len(self.messageWidgetList)):
            self.messageWidgetList[i].showDefaultColor()
        self.messageWidgetList[self.chatShow.row(item)].showColorful()

    def titleWidgetInit(self):
        #titleIconLabel QLabel
        self.titleIconLabel = QLabel()
        self.titleIconLabel.setFixedSize(30, 30)
        self.titleIconLabel.setScaledContents(True)
        self.titleIconLabel.setPixmap(QPixmap('AI助理.png'))
        #titleTextLabel QLabel
        self.titleTextLabel = QLabel()
        self.titleTextLabel.setFixedHeight(30)
        self.titleTextFont = QFont()
        self.titleTextFont.setPixelSize(22)
        self.titleTextLabel.setFont(self.titleTextFont)
        self.titleTextPalette = self.titleTextLabel.palette()
        self.titleTextPalette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.titleTextLabel.setPalette(self.titleTextPalette)
        self.titleTextLabel.setText('AI助理')
        self.titleTextLabel.adjustSize()
        #titleLeftSubWidget QWidget
        self.titleLeftSubWidget = Widget()
        self.titleLeftSubWidget.resize(self.titleIconLabel.width() + self.titleTextLabel.width() + 11, 36)
        self.titleLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleLeftSubHLayout QHBoxLayout
        self.titleLeftSubHLayout = QHBoxLayout()
        self.titleLeftSubWidget.setLayout(self.titleLeftSubHLayout)
        self.titleLeftSubHLayout.addWidget(self.titleIconLabel)
        self.titleLeftSubHLayout.addWidget(self.titleTextLabel)
        self.titleLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.titleLeftSubHLayout.setContentsMargins(3, 3, 3, 3)
        self.titleLeftSubHLayout.setSpacing(5)
        #minButton PushButton
        self.minButton = PushButton(tipText='', tipOffsetX=20, tipOffsetY=40)
        self.minButton.setFixedSize(50, 36)
        self.minButton.setIcon(QIcon("min.png"))
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
        self.maxButton.setIcon(QIcon("max.png"))
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
        self.closeButton.setIcon(QIcon("close.png"))
        self.closeButton.setIconSize(QSize(20, 20))
        self.closeButton.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QPushButton:hover{
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
            self.maxButton.setIcon(QIcon("max.png"))
        else:
            self.showMaximized()
            self.maxButton.setIcon(QIcon("normal.png"))

    def UiClose(self):
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
                with open(self.chatRecordFileName, 'a') as f:
                    for i in range(0, self.chatShow.count()):
                        chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                        f.write(chatRecordStr)
            else:
                for i in range(0, len(self.messageWidgetList)):
                    chatStrCount += self.messageWidgetList[i].getText().count('\n') + 2
                #read curChat file
                with open(self.curChatFile, 'r') as f:
                    lines = f.readlines()
                if chatStrCount > len(lines):
                    #clear curChat file
                    with open(self.curChatFile, 'w') as f:
                        f.truncate()
                    #write to curChat file
                    with open(self.curChatFile, 'a') as f:
                        for i in range(0, self.chatShow.count()):
                            chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                            f.write(chatRecordStr)
        self.close()

    def settingWidgetInit(self):
        #setting QLabel
        self.maxTokensLabel = Label()
        self.topPLabel = Label()
        self.temperatureLabel = Label()
        self.maxTokensLabel.setText("Max Tokens")
        self.topPLabel.setText("Top P")
        self.temperatureLabel.setText("Temperature")
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
        #setting maxTokens QWidget
        self.maxTokensWidget = QWidget()
        self.maxTokensWidget.resize(370, 160)
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
        self.maxTokensVLayout.setContentsMargins(15, 40, 15, 40)
        self.maxTokensVLayout.setSpacing(0)
        #setting topP QWidget
        self.topPWidget = QWidget()
        self.topPWidget.resize(370, 160)
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
        self.topPVLayout.setContentsMargins(15, 40, 15, 40)
        self.topPVLayout.setSpacing(0)
        #setting temperature QWidget
        self.temperatureWidget = QWidget()
        self.temperatureWidget.resize(370, 160)
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
        self.temperatureVLayout.setContentsMargins(15, 40, 15, 40)
        self.temperatureVLayout.setSpacing(0)
        #setting QWidget
        self.settingWidget = SettingWidget(self)
        self.settingWidget.setGeometry(-self.width() // 3, self.titleWidget.height(), self.width() // 3, self.height() - self.titleWidget.height())
        self.settingWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #setting QVBoxLayout
        self.settingVLayout = QVBoxLayout()
        self.settingWidget.setLayout(self.settingVLayout)
        self.settingVLayout.addWidget(self.maxTokensWidget)
        self.settingVLayout.addWidget(self.topPWidget)
        self.settingVLayout.addWidget(self.temperatureWidget)
        self.settingVLayout.setContentsMargins(15, 97, 15, 97)
        self.settingVLayout.setSpacing(45)
        #settingAnimationMove QPropertyAnimation
        self.settingAnimationMove = QPropertyAnimation(self.settingWidget, b'geometry')
        self.settingAnimationMove.setDuration(1000)
        self.settingAnimationMove.setEasingCurve(QEasingCurve.OutQuad)
        self.settingAnimationMove.valueChanged.connect(self.settingUiAnimationMove)
        #settingWidgetIsOpen
        self.settingWidgetIsOpen = False

    def settingButtonClicked(self):
        self.mask.show()
        self.settingWidget.raise_()
        self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
        self.settingAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
        self.settingAnimationMove.start()
        self.settingWidgetIsOpen = True

    def settingUiAnimationMove(self, rect):
        self.chatShow.resize(self.width() - rect.x() - self.settingWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.width() - rect.x() - self.settingWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.width() - rect.x() - self.settingWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.width() - rect.x() - self.settingWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.width() - rect.x() - self.settingWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.settingWidget.width(), 0, 0, 0)
        #TextShow max width
        textMaxWidth = self.chatShow.width() * 2 // 3
        for i in range(0, self.chatShow.count()):
            #messageWidget set max width of text
            messageWidget = self.messageWidgetList[i]
            messageWidget.setTextMaxWidth(textMaxWidth)
            #chatShow itemWidget adjust size
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            if messageWidget.getIsUser():
                itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
            else:
                itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))

    def chatRecordsUiAnimationMove(self, rect):
        self.chatShow.resize(self.width() - rect.x() - self.chatRecordsWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.width() - rect.x() - self.chatRecordsWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.width() - rect.x() - self.chatRecordsWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.width() - rect.x() - self.chatRecordsWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.width() - rect.x() - self.chatRecordsWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.chatRecordsWidget.width(), 0, 0, 0)
        #TextShow max width
        textMaxWidth = self.chatShow.width() * 2 // 3
        for i in range(0, self.chatShow.count()):
            #messageWidget set max width of text
            messageWidget = self.messageWidgetList[i]
            messageWidget.setTextMaxWidth(textMaxWidth)
            #chatShow itemWidget adjust size
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            itemWidget.setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            if messageWidget.getIsUser():
                itemWidget.layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 25, 5, 25, 5)
            else:
                itemWidget.layout().setContentsMargins(0, 5, itemWidget.width() - messageWidget.width(), 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))

    def chatRecordsMoveFinished(self):
        if not self.chatRecordsWidgetIsOpen:
            #delete all item
            self.chatRecordsWidget.delAllListItems()

    def maxTokensBoxValueChanged(self, i):
        global maxTokens_currentVal
        maxTokens_currentVal = i
        self.maxTokensSlider.setValue(i)

    def topPBoxValueChanged(self, d):
        global topP_currentVal
        topP_currentVal = d
        self.topPSlider.setValue(int(d * 100))

    def temperatureBoxValueChanged(self, d):
        global temperature_currentVal
        temperature_currentVal = d
        self.temperatureSlider.setValue(int((d - 0.01) * 100))

    def maxTokensSliderValueChanged(self, i):
        global maxTokens_currentVal
        maxTokens_currentVal = i
        self.maxTokensBox.setValue(maxTokens_currentVal)

    def topPSliderValueChanged(self, i):
        global topP_currentVal
        topP_currentVal = i / 100
        self.topPBox.setValue(topP_currentVal)

    def temperatureSliderValueChanged(self, i):
        global temperature_currentVal
        temperature_currentVal = i / 100 + 0.01
        self.temperatureBox.setValue(temperature_currentVal)

    def messageWidgetResize(self):
        for i in range(0, len(self.messageWidgetList)):
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
        #get text from TextEditFull
        text = self.chatInput.toPlainText()
        if not text == '':
            #MessageWidget
            self.messageSendWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, isUser=True, textMaxWidth=int(self.chatShow.width() * 2 / 3))
            self.messageSendWidget.connectSetSizeFinished(self.messageWidgetResize)
            self.messageSendWidget.toggleWidget()
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
            self.chatShow.setCurrentItem(self.sendItem)
            #create thread
            self.thread = messageThread(text)
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
        self.messageRecvWidget = MessageWidget(self.Message, self.textCopy, self.messageRenewResponse, isUser=False, textMaxWidth=int(self.chatShow.width() * 2 / 3))
        self.messageRecvWidget.connectSetSizeFinished(self.messageWidgetResize)
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
        self.chatShow.setCurrentItem(self.recvItem)
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

    def textCopy(self):
        #print textCopyLabel
        self.textCopyLabel.printStart()

    def messageRenewResponse(self):
        i = len(self.messageWidgetList) - 1
        j = 1
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

    def saveImage(self):
        #chatPixmap QPixmap
        self.chatPixmap = self.grab(self.rect())
        #chatPixmapName QString
        self.chatPixmapName = "chat_"
        self.chatPixmapName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
        self.chatPixmapName += ".png"
        #save image
        if self.chatPixmap.save(self.chatPixmapName, "png"):
            self.saveImageLabel.setText("图像保存成功")
            self.saveImageLabel.move((self.width() - self.saveImageLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.saveImageLabel.height() - 10)
            self.saveImageLabel.printStart()
        else:
            self.saveImageLabel.setText("图像保存失败")
            self.saveImageLabel.move((self.width() - self.saveImageLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() - self.saveImageLabel.height() - 10)
            self.saveImageLabel.printStart()

    def showChatRecords(self):
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
                with open(self.chatRecordFileName, 'a') as f:
                    for i in range(0, self.chatShow.count()):
                        chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                        f.write(chatRecordStr)
                #assign chatRecord fileName to curChatFile
                self.curChatFile = self.chatRecordFileName
            else:
                for i in range(0, len(self.messageWidgetList)):
                    chatStrCount += self.messageWidgetList[i].getText().count('\n') + 2
                #read curChat file
                with open(self.curChatFile, 'r') as f:
                    lines = f.readlines()
                if chatStrCount > len(lines):
                    #clear curChat file
                    with open(self.curChatFile, 'w') as f:
                        f.truncate()
                    #write to curChat file
                    with open(self.curChatFile, 'a') as f:
                        for i in range(0, self.chatShow.count()):
                            chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                            f.write(chatRecordStr)
        #generate item
        for fileName in os.listdir(os.curdir):
            if fileName.endswith(".txt"):
                with open(fileName, 'r') as f:
                    lines = f.readlines()
                #create item
                chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                item = self.chatRecordsWidget.addListItem(chatRecordStr)
                #item set data
                self.chatRecordsWidget.listItemSetData(item, fileName)
        #show chatRecordsWidget
        self.mask.show()
        self.chatRecordsWidget.raise_()
        self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
        self.chatRecordsAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
        self.chatRecordsAnimationMove.start()
        self.chatRecordsWidgetIsOpen = True

    def showSearchRecords(self):
        text = self.chatRecordsWidget.getLineEditText()
        self.chatRecordsWidget.delAllListItems()
        if not text == '':
            #generate item
            for fileName in os.listdir(os.curdir):
                if fileName.endswith(".txt"):
                    with open(fileName, 'r') as f:
                        content = f.read()
                    if text in content:
                        with open(fileName, 'r') as f:
                            lines = f.readlines()
                        #create item
                        chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                        item = self.chatRecordsWidget.addListItem(chatRecordStr)
                        #item set data
                        self.chatRecordsWidget.listItemSetData(item, fileName)
        else:
            #generate item
            for fileName in os.listdir(os.curdir):
                if fileName.endswith(".txt"):
                    with open(fileName, 'r') as f:
                        lines = f.readlines()
                    #create item
                    chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                    item = self.chatRecordsWidget.addListItem(chatRecordStr)
                    #item set data
                    self.chatRecordsWidget.listItemSetData(item, fileName)

    def clearAllChatRecords(self):
        self.chatRecordsWidget.delAllListItems()
        for fileName in os.listdir(os.curdir):
            if fileName.endswith(".txt"):
                filePath = os.path.join(os.curdir, fileName)
                os.remove(filePath)

    def generateChatRecord(self, item):
        #clear
        self.messageWidgetList.clear()
        self.chatShow.clear()
        #init
        text = ''
        isUser = True
        #assign chatRecord fileName to curChatFile
        self.curChatFile = self.chatRecordsWidget.listItemToString(item)
        #read curChat file
        with open(self.curChatFile, 'r') as f:
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
                self.messageWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, isUser=isUser, textMaxWidth=self.chatShow.width() * 2 // 3)
                self.messageWidget.connectSetSizeFinished(self.messageWidgetResize)
                self.messageWidget.toggleWidget()
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
                self.chatShow.setCurrentItem(self.item)
                #clear text
                text = ''
            else:
                text += lines[i]

    def newChat(self):
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
                with open(self.chatRecordFileName, 'a') as f:
                    for i in range(0, self.chatShow.count()):
                        chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                        f.write(chatRecordStr)
                #assign chatRecord fileName to curChatFile
                self.curChatFile = self.chatRecordFileName
            else:
                for i in range(0, len(self.messageWidgetList)):
                    chatStrCount += self.messageWidgetList[i].getText().count('\n') + 2
                #read curChat file
                with open(self.curChatFile, 'r') as f:
                    lines = f.readlines()
                if chatStrCount > len(lines):
                    #clear curChat file
                    with open(self.curChatFile, 'w') as f:
                        f.truncate()
                    #write to curChat file
                    with open(self.curChatFile, 'a') as f:
                        for i in range(0, self.chatShow.count()):
                            chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                            f.write(chatRecordStr)
        #clear
        self.messageWidgetList.clear()
        self.chatShow.clear()
        self.curChatFile = ''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font_file_path = 'msyhl.ttc'
    font_id = QFontDatabase.addApplicationFont(font_file_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
            font = QFont(font_family, 22)
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
