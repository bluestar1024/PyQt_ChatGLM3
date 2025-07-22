# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:31:44 2024

@author: YXD
"""

import sys, os
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QAbstractItemView, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QGridLayout, QLineEdit, QSplitter, QToolTip, QMenu, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QPropertyAnimation, QEasingCurve, QEvent, QPoint, pyqtProperty, QTimer, QCoreApplication, QUrl, QTime, QObject, QXmlStreamReader, QFile, QIODevice, QRegularExpression, QDir
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen, QCursor, QFontDatabase, QMouseEvent, QLinearGradient, QTextCursor, QTextCharFormat, QTextDocument, QSyntaxHighlighter, QTextOption
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
""" from pygments import highlight, token
from pygments.lexers import CLexer, CppLexer, PythonLexer, JavaLexer, JavascriptLexer
from pygments.formatters import HtmlFormatter
from pygments.style import Style """
from openai import OpenAI
import math
import re
import mistune

#test
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
font_file_path = os.path.normpath(os.path.join(current_dir, '..', 'font', 'msyhl.ttc')).replace('\\', '/')
images_dir = os.path.normpath(os.path.join(current_dir, '..', 'images')).replace('\\', '/')
config_file_path = os.path.normpath(os.path.join(current_dir, '..', 'config', 'config.txt'))
mathjax_script_path = os.path.normpath(os.path.join(current_dir, '..', 'mathjax/es5/tex-mml-chtml.js')).replace('\\', '/')
chat_records_dir = os.path.normpath(os.path.join(current_dir, '..', 'chatrecords'))
code_theme_file_path = os.path.normpath(os.path.join(current_dir, '..', 'config', 'dark_theme.xml'))

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

windowFontPointSize = 10
bubbleFontPointSize = 10
bubbleFontPixelSize = 20
buttonFontPointSize = 9
titleFontPointSize = 14
textEditFullBGColor = QColor(224, 224, 224)
textEditFullBGTColor = QColor(224, 224, 224, 0)
textEditFullBColor = QColor(100, 100, 100)
textEditFullBTColor = QColor(100, 100, 100, 0)
""" fulBubbleColor = QColor(119, 221, 255)
userBubbleColor = QColor(16, 149, 222)
aiBubbleColor = QColor(17, 173, 222) """

testText2 = '''<think>
让我想一下两种方法。第一种方法更直观，适合新手理解。第二种方法效率更高，特别是当n很大的时候。那么对于这个问题来说，两种方式都行。我应该两种方法都写吗？可能问题只需要一种实现，但为了全面，我可以两种情况都考虑一下。

那我先写出循环的方法。Java中，for循环从1到100，每次加i。代码结构大概是：

```cpp
int sum = 0;
for (int i = 1; i <= 100; ++i) {
    #path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
    sum += i;
}
std::cout << sum << std::endl;

#include <iostream>
#include <QDebug>

#sdfgs	"fdgdf"
#cfdsf	546

int main()
{
    int n, sum = 0;

    std::cout << "Enter a positive integer: ";
    std::cin >> n;

    for (int i = 1; i <= n; ++i)
    {
        sum += i;
    }

    std::cout << "Sum = " << sum;
    return 0;
}
int fun()
fun()
std:: fun()
int std::fun ()
float std::std::fun()
fun

// sdassadfsa sda

// sada

/* jkhj
jkk
gjh */

int xf;
int ydsf = 1;
int sdy=0
int xv + =1
int xvbd+ =1
int xf+=1
int xfddd - =1
int fvdx * =1
int xfg / =1
int xh % =1
int xnb , y ;
int xdgf = 1,

a.b.fun()
12.3
```

然后是Python的部分。Python的语法更简单，循环的话：
</think>
'''

testText = '''<think>
让我想一下两种方法。第一种方法更直观，适合新手理解。第二种方法效率更高，特别是当n很大的时候。那么对于这个问题来说，两种方式都行。我应该两种方法都写吗？可能问题只需要一种实现，但为了全面，我可以两种情况都考虑一下。

那我先写出循环的方法。Java中，for循环从1到100，每次加i。代码结构大概是：

```cpp
int sum = 0;
for (int i = 1; i <= 100; ++i) {
    #path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
    sum += i;
}
std::cout << sum << std::endl;

#include <iostream>
#include <QDebug>

#sdfgs	"fdgdf"
#cfdsf	546

int main()
{
    int n, sum = 0;

    std::cout << "Enter a positive integer: ";
    std::cin >> n;

    for (int i = 1; i <= n; ++i)
    {
        sum += i;
    }

    std::cout << "Sum = " << sum;
    return 0;
}
int fun()
fun()
std:: fun()
int std::fun ()
float std::std::fun()
fun

// sdassadfsa sda

// sada

/* jkhj
jkk
gjh */

int xf;
int ydsf = 1;
int sdy=0
int xv + =1
int xvbd+ =1
int xf+=1
int xfddd - =1
int fvdx * =1
int xfg / =1
int xh % =1
int xnb , y ;
int xdgf = 1,

a.b.fun()
12.3
```

然后是Python的部分。Python的语法更简单，循环的话：

```python
sum = 0
for i in range(1, 101):
    sum += i
#path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
print(sum)

import sys
from PyQt5.QtWidgets import QTextEdit, QApplication, QWidget
from PyQt5.QtGui import QTextCharFormat, QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QRect
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        xd - = 8
        fy += 6
        ztrh *= 7
        xr /= 7
        yrte % = 9
        self.editor.document().blockCountChanged.connect(self.update_width)
        """ self.editor.updateRequest.connect(self.update) """
        print(self.editor.document())

    def paintEvent(self, event):
        """ painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        block = self.editor.document().begin()
        while block and block.isValid():
            line_number = block.blockNumber() + 1
            painter.drawText(0, block.position() - 
            self.editor.contentOffset().y(), str(line_number))
            block = block.next() """
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        """ for count in range(0, self.editor.document().blockCount()): """
        painter.end()

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setTabStopWidth(4)
        self.lineNumberArea = LineNumberArea(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 更新行号区域位置
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 
        self.lineNumberArea.width(), cr.height()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeEditor()
    window.show()
    sys.exit(app.exec_())
```

总结一下，每个语言可以有两种实现方式，但问题可能只需要一种，所以我可以选择其中一种，比如公式的方法，这样更简洁高效。
</think>

以下是分别计算整数 1 到 100 的和的代码示例：

### C++
```cpp
#include <iostream>

using namespace std;

int main() {
    #path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
    int n = 100;
    int sum = n * (n + 1) / 2;
    cout << sum << endl;
    return 0;
}
```

### Python
```python
n = 100
total = n * (n + 1) // 2
#path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
print(total)
```

这些代码都使用了高斯公式来计算从 1 到 100 的和，结果都是 5050。
'''

'''class messageThread(QThread):
    newMessage = pyqtSignal(str)

    def __init__(self, contentInput, context=None, use_stream=True, parent=None):
        super(messageThread, self).__init__(parent)
        #read setting config file
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                content = f.readlines()
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
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
        return'''
class messageThread(QThread):
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
        self.contentOutput = testText
        if self.use_stream:
            for i in range(0, len(self.contentOutput), 400):
                self.newMessage.emit(self.contentOutput[i:i+400])
                time.sleep(1)
        else:
            self.newMessage.emit(self.contentOutput)
        return

    def stop(self):
        self.terminate()
        self.wait()

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
            font.setPointSize(buttonFontPointSize)
            QToolTip.setFont(font)
            QToolTip.showText(self.mapToGlobal(self.tipStartPos), self.tipText, self)
        return QPushButton.event(self, event)

class FunWidget(QWidget):
    def __init__(self, parent=None):
        super(FunWidget, self).__init__(parent)
        #chatRecordsButton PushButton
        self.chatRecordsButton = PushButton(tipText='聊天历史', tipOffsetX=15, tipOffsetY=35)
        self.chatRecordsButton.setFixedSize(44, 44)
        self.chat_records_images_path = os.path.join(images_dir, 'chat_records.png').replace('\\', '/')
        """ self.chat_records_hover_images_path = os.path.join(images_dir, 'chat_records_hover.png').replace('\\', '/') """
        self.chatRecordsButton.setIcon(QIcon(f"{self.chat_records_images_path}"))
        self.chatRecordsButton.setIconSize(QSize(30, 30))
        self.chatRecordsButton.setStyleSheet('''
        QPushButton{
            border: none;
            border-radius: 22px;
        }
        QPushButton:hover{
            background: #d0d0d0;
        }
        ''')
        #funLeftSubWidget QWidget
        self.funLeftSubWidget = Widget()
        self.funLeftSubWidget.resize(self.chatRecordsButton.width() + 15, self.chatRecordsButton.height() + 16)
        self.funLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #funLeftSubHLayout QHBoxLayout
        self.funLeftSubHLayout = QHBoxLayout()
        self.funLeftSubWidget.setLayout(self.funLeftSubHLayout)
        self.funLeftSubHLayout.addWidget(self.chatRecordsButton)
        self.funLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.funLeftSubHLayout.setContentsMargins(10, 10, 5, 6)
        #titleLabel QLabel
        self.titleLabel = QLabel()
        self.titleLabel.setFixedHeight(60)
        self.titleFont = QFont()
        self.titleFont.setPointSize(titleFontPointSize)
        self.titleFont.setBold(True)
        self.titleLabel.setFont(self.titleFont)
        self.titleLabel.setText('AI助理')
        self.titleLabel.adjustSize()
        #funMidSubWidget QWidget
        self.funMidSubWidget = Widget()
        self.funMidSubWidget.resize(self.titleLabel.width(), self.titleLabel.height())
        self.funMidSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #funMidSubHLayout QHBoxLayout
        self.funMidSubHLayout = QHBoxLayout()
        self.funMidSubWidget.setLayout(self.funMidSubHLayout)
        self.funMidSubHLayout.addWidget(self.titleLabel)
        self.funMidSubHLayout.setAlignment(Qt.AlignCenter)
        self.funMidSubHLayout.setContentsMargins(0, 0, 0, 0)
        #newChatButton PushButton
        self.newChatButton = PushButton(tipText='新聊天', tipOffsetX=10, tipOffsetY=35)
        self.newChatButton.setFixedSize(44, 44)
        self.new_chat_images_path = os.path.join(images_dir, 'new_chat.png').replace('\\', '/')
        """ self.new_chat_hover_images_path = os.path.join(images_dir, 'new_chat_hover.png').replace('\\', '/') """
        self.newChatButton.setIcon(QIcon(f"{self.new_chat_images_path}"))
        self.newChatButton.setIconSize(QSize(30, 30))
        self.newChatButton.setStyleSheet('''
        QPushButton{
            border: none;
            border-radius: 22px;
        }
        QPushButton:hover{
            background: #d0d0d0;
        }
        ''')
        #funRightSubWidget QWidget
        self.funRightSubWidget = Widget()
        self.funRightSubWidget.resize(self.newChatButton.width() + 15, self.newChatButton.height() + 16)
        self.funRightSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #funRightSubHLayout QHBoxLayout
        self.funRightSubHLayout = QHBoxLayout()
        self.funRightSubWidget.setLayout(self.funRightSubHLayout)
        self.funRightSubHLayout.addWidget(self.newChatButton)
        self.funRightSubHLayout.setAlignment(Qt.AlignRight)
        self.funRightSubHLayout.setContentsMargins(5, 10, 10, 6)
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.mainHLayout.addWidget(self.funLeftSubWidget)
        self.mainHLayout.addWidget(self.funMidSubWidget)
        self.mainHLayout.addWidget(self.funRightSubWidget)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        #FunWidget adjust size
        self.resize(1200, 60)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def connectChatRecordsButtonClick(self, fun):
        self.chatRecordsButton.clicked.connect(fun)

    def connectNewChatButtonClick(self, fun):
        self.newChatButton.clicked.connect(fun)

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.resize(1170, 480)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setFocusPolicy(Qt.NoFocus)
        self.verticalScrollBar().setCursor(Qt.PointingHandCursor)
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
        QScrollBar:vertical {
            background: transparent;
            width: 10px;
            padding: 0px 4px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #bcbcbc;
            width: 6px;
            border-radius: 3px; /* 设置滑块为圆角矩形 */
        }
        QScrollBar::handle:vertical:hover {
            background: #808080;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: transparent;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            width: 0px;
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
            font.setPointSize(buttonFontPointSize)
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
        self.resize(1130, 150)
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
        ''')
        self.setStyleSheet(f'''
        QTextEdit{{
            border: none;
            background :transparent;
            font-size: {windowFontPointSize}pt;
        }}
        QScrollBar{{
            width: 25px;
        }}
        ''')
        #setMouseTracking
        self.setMouseTracking(True)
        #isSending
        self.isSending = False

    def contextMenuEvent(self, event):
        menu = CustomMenu(self)
        menu.setStyleSheet('''
        QMenu {
            background-color: white;
            border: none;
            border-radius: 15px;
            padding: 5px;  /* 菜单内边距 */
        }
        QMenu::item:selected {
            color: black;
            background-color: #e0e0e0;
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

    """ def enableSendButton(self):
        self.sendButton.setEnabled(True) """

    """ def disableSendButton(self):
        self.sendButton.setEnabled(False) """

    """ def sendButtonIsEnable(self):
        return self.sendButton.isEnabled() """

    def sendButtonShow(self):
        if self.isSending:
            self.sendButton.setStyleSheet(f'''
            QPushButton{{
                border: none;
                image: url("{self.send_disable_images_path}");
            }}
            ''')
        elif self.toPlainText() == '':
            self.sendButton.setStyleSheet(f'''
            QPushButton{{
                border: none;
                image: url("{self.send_images_path}");
            }}
            ''')
        else:
            self.sendButton.setStyleSheet(f'''
            QPushButton{{
                border: none;
                image: url("{self.send_hover_images_path}");
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

    """ def enableSendButton(self):
        self.textEdit.enableSendButton() """

    """ def disableSendButton(self):
        self.textEdit.disableSendButton() """

    """ def sendButtonIsEnable(self):
        return self.textEdit.sendButtonIsEnable() """

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
        if isinstance(self.parent(), TextShow):
            current_scroll_value = self.parent().parent().parent().parent().listWidget.verticalScrollBar().value()
            min_scroll_value = self.parent().parent().parent().parent().listWidget.verticalScrollBar().minimum()
            max_scroll_value = self.parent().parent().parent().parent().listWidget.verticalScrollBar().maximum()
        else:
            current_scroll_value = self.parent().parent().parent().parent().parent().listWidget.verticalScrollBar().value()
            min_scroll_value = self.parent().parent().parent().parent().parent().listWidget.verticalScrollBar().minimum()
            max_scroll_value = self.parent().parent().parent().parent().parent().listWidget.verticalScrollBar().maximum()
        # 计算新的滚动位置
        new_scroll_value = current_scroll_value - delta_y * 3
        if new_scroll_value < min_scroll_value:
            new_scroll_value = min_scroll_value
        elif new_scroll_value > max_scroll_value:
            new_scroll_value = max_scroll_value
        # 设置新的滚动位置
        if isinstance(self.parent(), TextShow):
            self.parent().parent().parent().parent().listWidget.verticalScrollBar().setValue(new_scroll_value)
        else:
            self.parent().parent().parent().parent().parent().listWidget.verticalScrollBar().setValue(new_scroll_value)
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
    """ setTexting = pyqtSignal(bool) """

    def __init__(self, text, isUser=True, maxWidth=810, parent=None):
        super(TextShow, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = CustomLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth - 10
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        """ self.font.setPointSize(windowFontPointSize) """
        self.font.setPixelSize(bubbleFontPixelSize)
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)
        self.mainHLayout = QHBoxLayout()
        self.webEngineView = WebEngineView()
        self.webEngineView.setMaximumWidth(self.maxWidth)
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
            self.mainHLayout.setContentsMargins(5, 0, 5, 0)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(labelWidth + 10, labelHeight)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 0, 5, 0)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(self.label.width() + 10, self.label.height())
        self.isUser = isUser
        self.isColorful = False

    """ def paintEvent(self, event):
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
        painter.end() """

    def setText(self, text):
        """ self.setTexting.emit(self.isLabel) """
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
            self.setFixedSize(labelWidth + 10, labelHeight)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.setFixedSize(self.label.width() + 10, self.label.height())

    def onPageLoadFinished(self, success):
        js = """
        function getPageSize() {
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
        getPageSize();
        """
        if success:
            self.webEngineView.page().runJavaScript("document.body.style.overflowY = 'hidden';")
            self.webEngineView.page().runJavaScript(js, self.updateSize)

    def updateSize(self, result):
        width, height = result
        """ print('TextShow width, height:', width + 10, height + 10) """
        if width != 0 and height != 0:
            self.webEngineView.setFixedSize(width, height)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height())
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
        """ print('TextShow') """
        markdown_content = ''
        self.html_text = ''
        self.full_html_text = ''
        initWidth = self.font_metrics.width(self.text)
        if initWidth > self.maxWidth:
            self.webEngineView.setFixedWidth(self.maxWidth)
        else:
            if self.text == '':
                self.webEngineView.setFixedSize(20, 66)
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
                        font-size: {bubbleFontPixelSize}px;
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
            """ self.setTexting.emit(self.isLabel) """
        else:
            if self.isLabel:
                self.mainHLayout.removeWidget(self.label)
                self.label.deleteLater()
                self.mainHLayout.addWidget(self.webEngineView)
            self.setFixedSize(self.webEngineView.width() + 10, self.webEngineView.height())
            self.setSizeFinished.emit()
            self.isLabel = False
            """ self.setTexting.emit(self.isLabel) """

    """ def connectSetTexting(self, fun):
        self.setTexting.connect(fun) """

    """ def getWebEngineView(self):
        return self.webEngineView """

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
    def __init__(self, isUser=True, parent=None):
        super(TextWidget, self).__init__(parent)
        self.isUser = isUser
        self.setMouseTracking(True)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        if self.isUser:
            brush.setColor(QColor(235, 243, 251))
        else:
            brush.setColor(Qt.white)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

class TextBoxWidget(QWidget):
    def __init__(self, parent=None):
        super(TextBoxWidget, self).__init__(parent)
        self.setMouseTracking(True)

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super(LoadingWidget, self).__init__(parent)
        self.setFixedSize(35, 35)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(1)

    def update_animation(self):
        self.angle = (self.angle + 9) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        x1 = self.width() / 2 + math.cos(math.radians(self.angle)) * ((self.width() - 10) / 2)
        y1 = self.width() / 2 + math.sin(math.radians(self.angle)) * ((self.width() - 10) / 2)
        x2 = self.width() / 2 - math.cos(math.radians(self.angle)) * ((self.width() - 10) / 2)
        y2 = self.width() / 2 - math.sin(math.radians(self.angle)) * ((self.width() - 10) / 2)
        gradient = QLinearGradient(x1, y1, x2, y2)
        gradient.setColorAt(0, QColor(224, 224, 224))
        gradient.setColorAt(1, QColor(100, 100, 100))
        pen = QPen(gradient, 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        rect = self.rect().adjusted(5, 5, -5, -5)
        painter.drawArc(rect, -self.angle * 16, -180 * 16)

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
            font.setPointSize(buttonFontPointSize)
            QToolTip.setFont(font)
            QToolTip.showText(self.mapToGlobal(self.tipStartPos), self.tipText, self)
        return QPushButton.event(self, event)

class ThinkingButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ThinkingButton, self).__init__(parent)
        self.setFixedHeight(30)
        self.setCursor(Qt.PointingHandCursor)
        self.isShowThinkContent = False
        self.backgroundColor = QColor(248, 248, 248)
        #leftIconLabel QLabel
        self.leftIconLabel = QLabel()
        self.thinking_icon_images_path = os.path.join(images_dir, 'thinking_icon.png').replace('\\', '/')
        self.leftIconLabel.setPixmap(QPixmap(f'{self.thinking_icon_images_path}').scaled(20, 20, Qt.KeepAspectRatio))
        self.leftIconLabel.setFixedSize(20, 20)
        #textLabel QLabel
        self.textLabel = QLabel('思考中...')
        font = QFont()
        font.setPointSize(windowFontPointSize)
        self.textLabel.setFont(font)
        self.textLabel.adjustSize()
        #rightIconLabel QLabel
        self.rightIconLabel = QLabel()
        self.arrow_up_images_path = os.path.join(images_dir, 'arrow_up.png').replace('\\', '/')
        self.arrow_down_images_path = os.path.join(images_dir, 'arrow_down.png').replace('\\', '/')
        self.rightIconLabel.setPixmap(QPixmap(f'{self.arrow_up_images_path}').scaled(20, 20, Qt.KeepAspectRatio))
        self.rightIconLabel.setFixedSize(20, 20)
        #QHBoxLayout
        mainHLayout = QHBoxLayout()
        self.setLayout(mainHLayout)
        mainHLayout.addWidget(self.leftIconLabel)
        mainHLayout.addWidget(self.textLabel)
        mainHLayout.addWidget(self.rightIconLabel)
        mainHLayout.setContentsMargins(5, 5, 5, 5)
        mainHLayout.setSpacing(0)
        self.setFixedWidth(self.leftIconLabel.width() + self.textLabel.width() + self.rightIconLabel.width() + 10)
        #thinkTime
        self.thinkTimeLength = 0
        self.startThinkTime = QTime.currentTime()

    def enterEvent(self, event):
        self.backgroundColor = QColor(232, 232, 232)
        self.repaint()

    def leaveEvent(self, event):
        self.backgroundColor = QColor(248, 248, 248)
        self.repaint()

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 10, 10)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.backgroundColor)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def mousePressEvent(self, event):
        self.isShowThinkContent = not self.isShowThinkContent
        if self.isShowThinkContent:
            self.rightIconLabel.setPixmap(QPixmap(f'{self.arrow_up_images_path}').scaled(20, 20, Qt.KeepAspectRatio))
        else:
            self.rightIconLabel.setPixmap(QPixmap(f'{self.arrow_down_images_path}').scaled(20, 20, Qt.KeepAspectRatio))
        self.clicked.emit()
        QWidget.mousePressEvent(self, event)

    def connectButtonClick(self, fun):
        self.clicked.connect(fun)

    def setThinkEnd(self):
        endThinkTime = QTime.currentTime()
        self.thinkTimeLength = self.startThinkTime.secsTo(endThinkTime)
        self.textLabel.setText(f"已深度思考(用时{self.thinkTimeLength}秒)")
        self.textLabel.adjustSize()
        self.setFixedWidth(self.leftIconLabel.width() + self.textLabel.width() + self.rightIconLabel.width() + 10)

""" class ThinkLabel(QLabel):
    def __init__(self, text, maxWidth=765, parent=None):
        super().__init__(parent)
        self.text = text.strip('\n')
        self.label = CustomLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        self.font.setPointSize(windowFontPointSize)
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)
        self.mainHLayout = QHBoxLayout()
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
            self.mainHLayout.setContentsMargins(10, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(labelWidth + 15, labelHeight + 10)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(10, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(self.label.width() + 15, self.label.height() + 10)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x() + 4, self.rect().y() + 4, 2, self.rect().height() - 8)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.lightGray)
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

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
            self.setFixedSize(labelWidth + 15, labelHeight + 10)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.setFixedSize(self.label.width() + 15, self.label.height() + 10) """

class ThinkWidget(QWidget):
    setSizeFinished = pyqtSignal()

    def __init__(self, text, maxWidth=765, parent=None):
        super(ThinkWidget, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = CustomLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        """ self.font.setPointSize(windowFontPointSize) """
        self.font.setPixelSize(bubbleFontPixelSize)
        """ print('ThinkWidget bubbleFontPixelSize:', bubbleFontPixelSize) """
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)
        self.mainHLayout = QHBoxLayout()
        self.webEngineView = WebEngineView()
        self.webEngineView.setMaximumWidth(self.maxWidth)
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
            self.mainHLayout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(labelWidth, labelHeight)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(self.label.width(), self.label.height())

    """ def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #backgroundPath QPainterPath
        backgroundPath = QPainterPath()
        backgroundPath.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #backgroundBrush QBrush
        backgroundBrush = QBrush(Qt.SolidPattern)
        backgroundBrush.setColor(QColor(Qt.green))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(backgroundBrush)
        painter.drawPath(backgroundPath.simplified())
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x() + 9, self.rect().y() + 8, 2, self.rect().height() - 16)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(200, 200, 200))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end() """

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
            self.setFixedSize(labelWidth, labelHeight)
        else:
            self.label.setFixedSize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.setFixedSize(self.label.width(), self.label.height())

    def onPageLoadFinished(self, success):
        js = """
        function getPageSize() {
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
        getPageSize();
        """
        if success:
            self.webEngineView.page().runJavaScript("document.body.style.overflowY = 'hidden';")
            self.webEngineView.page().runJavaScript(js, self.updateSize)

    def updateSize(self, result):
        width, height = result
        if width != 0 and height != 0:
            self.webEngineView.setFixedSize(width, height)
            self.setFixedSize(self.webEngineView.width(), self.webEngineView.height())
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
        """ print('ThinkWidget toggleWidget') """
        markdown_content = ''
        self.html_text = ''
        self.full_html_text = ''
        initWidth = self.font_metrics.width(self.text)
        if initWidth > self.maxWidth:
            self.webEngineView.setFixedWidth(self.maxWidth)
        else:
            if self.text == '':
                self.webEngineView.setFixedSize(20, 66)
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
                        font-size: {bubbleFontPixelSize}px;
                        color: gray;
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
        else:
            if self.isLabel:
                self.mainHLayout.removeWidget(self.label)
                self.label.deleteLater()
                self.mainHLayout.addWidget(self.webEngineView)
            self.setFixedSize(self.webEngineView.width(), self.webEngineView.height())
            self.setSizeFinished.emit()
            self.isLabel = False

    """ def getWebEngineView(self):
        return self.webEngineView """

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

class ThinkBackWidget(QWidget):
    def __init__(self, parent=None):
        super(ThinkBackWidget, self).__init__(parent)

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #backgroundPath QPainterPath
        backgroundPath = QPainterPath()
        backgroundPath.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 13, 13)
        #backgroundBrush QBrush
        backgroundBrush = QBrush(Qt.SolidPattern)
        backgroundBrush.setColor(QColor(244, 244, 252))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(backgroundBrush)
        painter.drawPath(backgroundPath.simplified())
        #QPainterPath
        path = QPainterPath()
        path.addRect(self.rect().x() + 14, self.rect().y() + 12, 2, self.rect().height() - 24)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(172, 188, 220))
        #QPainter setting
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

class LineNumberArea(QWidget):
    def __init__(self, parent=None):
        super(LineNumberArea, self).__init__(parent)
        self.editor = parent
        self.backgroundColor = QColor(20, 20, 28)
        self.numberColor = QColor(178, 170, 164)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), self.backgroundColor)
        """ painter.fillRect(event.rect(), QColor(Qt.red)) """
        pen = QPen(self.numberColor)
        painter.setPen(pen)
        painter.setFont(self.editor.font())
        hAdvance = self.editor.fontMetrics().horizontalAdvance('9')
        blockNumber = self.editor.getFirstVisibleBlock()
        block       = self.editor.document().findBlockByNumber(blockNumber)
        top         = int(self.editor.document().documentLayout().blockBoundingRect(block).translated(0, -self.editor.verticalScrollBar().value()).top())
        bottom      = top + int(self.editor.document().documentLayout().blockBoundingRect(block).height())
        while(block.isValid() and top <= event.rect().bottom()):
            if (block.isVisible() and bottom >= event.rect().top()):
                """ print('naturalTextRect:', block.layout().lineAt(0).naturalTextRect())
                print('rect:', block.layout().lineAt(0).rect()) """
                painter.drawText(int((2 - len(str(self.editor.document().blockCount()))) * 0.275 * hAdvance), top, self.width() - hAdvance, int(block.layout().lineAt(0).rect().height()), Qt.AlignRight | Qt.AlignVCenter, str(blockNumber + 1))
            block = block.next()
            top = int(self.editor.document().documentLayout().blockBoundingRect(block).translated(0, -self.editor.verticalScrollBar().value()).top())
            bottom = top + int(self.editor.document().documentLayout().blockBoundingRect(block).height())
            blockNumber += 1
        painter.end()

    def setLightBackgroundColor(self):
        self.backgroundColor = QColor(236, 236, 228)
        self.numberColor = QColor(78, 86, 92)

    def setDarkBackgroundColor(self):
        self.backgroundColor = QColor(20, 20, 28)
        self.numberColor = QColor(178, 170, 164)

class CodeEdit(QTextEdit):
    setSizeFinished = pyqtSignal()

    def __init__(self, maxWidth=810, parent=None):
        super(CodeEdit, self).__init__(parent)
        self.text = ''
        self.lexerName = ''
        self.setFixedWidth(maxWidth)
        self.horizontalScrollBar().setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('''
        QTextEdit {
            border: none;
            background-color: #14141c;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
        }
        QScrollBar:horizontal {
            background: transparent;
            height: 10px;
            padding: 0px 0px 4px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #44444c;
            height: 6px;
            border-radius: 3px; /* 设置滑块为圆角矩形 */
        }
        QScrollBar::handle:horizontal:hover {
            background: #747474;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: transparent;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        ''')
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setFixedPitch(True)
        font.setPointSize(windowFontPointSize)
        self.setFont(font)
        """ print('font pitch:', font.fixedPitch(), self.font().fixedPitch()) """
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(178, 170, 164))
        self.setPalette(palette)
        #LineNumberArea
        self.lineNumberArea = LineNumberArea(self)
        self.lineNumberArea.move(0, 0)
        self.updateLineNumberAreaWidth()
        #textChanged
        """ self.textChanged.connect(self.onTextChanged) """
        self.textChanged.connect(self.adjustSize)
        #valueChanged
        self.verticalScrollBar().valueChanged.connect(self.onScroll)
        self.m_highlighters = {
            "None": None,
            "Python": QPythonHighlighter(),
            "C++": QCXXHighlighter(),
            "GLSL": QGLSLHighlighter(),
            "LUA": QLuaHighlighter()
        }
        self.m_highlighter = self.m_highlighters["None"]
        #isAdjustSizeCalled
        self.isAdjustSizeCalled = False

    def setThemeStyle(self, isLightThemeStyle=False):
        global code_theme_file_path
        if isLightThemeStyle:
            self.setStyleSheet('''
            QTextEdit {
                border: none;
                background-color: #ecece4;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
            }
            QScrollBar:horizontal {
                background: transparent;
                height: 10px;
                padding: 0px 0px 4px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #bcbcb4;
                height: 6px;
                border-radius: 3px; /* 设置滑块为圆角矩形 */
            }
            QScrollBar::handle:horizontal:hover {
                background: #8c8c8c;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            ''')
            palette = self.palette()
            palette.setColor(QPalette.Text, QColor(78, 86, 92))
            self.setPalette(palette)
            self.lineNumberArea.setLightBackgroundColor()
            code_theme_file_path = os.path.normpath(os.path.join(current_dir, '..', 'config', 'light_theme.xml'))
        else:
            self.setStyleSheet('''
            QTextEdit {
                border: none;
                background-color: #14141c;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
            }
            QScrollBar:horizontal {
                background: transparent;
                height: 10px;
                padding: 0px 0px 4px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #44444c;
                height: 6px;
                border-radius: 3px; /* 设置滑块为圆角矩形 */
            }
            QScrollBar::handle:horizontal:hover {
                background: #747474;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            ''')
            palette = self.palette()
            palette.setColor(QPalette.Text, QColor(178, 170, 164))
            self.setPalette(palette)
            self.lineNumberArea.setDarkBackgroundColor()
            code_theme_file_path = os.path.normpath(os.path.join(current_dir, '..', 'config', 'dark_theme.xml'))
        self.highlightCode(self.text, self.lexerName)

    def onScroll(self, value):
        self.lineNumberArea.repaint()

    def getFirstVisibleBlock(self):
        curs = QTextCursor(self.document())
        curs.movePosition(QTextCursor.Start)
        r1 = self.viewport().geometry()
        for i in range(self.document().blockCount()):
            block = curs.block()
            r2 = self.document().documentLayout().blockBoundingRect(block).translated(self.viewport().geometry().x(), self.viewport().geometry().y() - self.verticalScrollBar().sliderPosition()).toRect()
            if r1.intersects(r2):
                return i
            curs.movePosition(QTextCursor.NextBlock)
        return 0

    def highlightCode(self, text, lexerName='python'):
        self.text = text
        self.lexerName = lexerName

        match lexerName:
            case 'cpp':
                self.setHighlighter(self.m_highlighters["C++"])
            case 'python':
                self.setHighlighter(self.m_highlighters["Python"])
            case 'glsl':
                self.setHighlighter(self.m_highlighters["GLSL"])
            case 'lua':
                self.setHighlighter(self.m_highlighters["LUA"])
            case _:
                self.setHighlighter(self.m_highlighters["Python"])
        """ text = self.add_line_numbers(text) """
        """ formatter = HtmlFormatter(style=CustomStyle, noclasses=True)
        html = highlight(text, lexer, formatter) """
        """ html = html.replace('<pre style="line-height: 125%;">', '<pre style="line-height: 100%;">') """
        """ self.setHtml(html) """
        self.setText(text)
        """ self.setPlainText(text) """

    def setHighlighter(self, highlighter):
        if self.m_highlighter:
            self.m_highlighter.setDocument(None)
        self.m_highlighter = highlighter
        if self.m_highlighter:
            """ print('m_highlighter:', self.m_highlighter) """
            self.m_highlighter.setSyntaxStyle(QSyntaxStyle.defaultStyle())
            self.m_highlighter.setDocument(self.document())

    """ def add_line_numbers(self, text):
        # 根据 '\n' 分割字符串成多行
        lines = text.split('\n')
        
        # 为每一行添加行号和两个空格
        numbered_lines = []
        for i, line in enumerate(lines, start=1):
            numbered_line = f"{i}  {line}"  # 行号加两个空格
            numbered_lines.append(numbered_line)
        
        # 将处理后的行重新组合成字符串
        result = '\n'.join(numbered_lines)
        return result """

    def updateLineNumberAreaWidth(self):
        self.lineNumberArea.setFixedSize(self.fontMetrics().horizontalAdvance('9') * (len(str(self.document().blockCount())) + 1), self.viewport().height())
        self.setViewportMargins(self.lineNumberArea.width(), 0, 0, 0)

    """ def onTextChanged(self):
        QTimer.singleShot(1, self.adjustSize) """

    def adjustSize(self):
        self.isAdjustSizeCalled = True
        print('CodeEdit adjustSize height:', int(self.document().size().height()), self.horizontalScrollBar().height(), self)
        self.setFixedHeight(int(self.document().size().height()) + 15)
        self.updateLineNumberAreaWidth()
        self.lineNumberArea.repaint()
        self.setSizeFinished.emit()
        self.isAdjustSizeCalled = False

    def resizeEvent(self, event):
        QTextEdit.resizeEvent(self, event)
        print('CodeEdit resizeEvent isAdjustSizeCalled', self.isAdjustSizeCalled, self)
        print('?=', self.height(), int(self.document().size().height()))
        if self.height() != int(self.document().size().height()) + 15:
            print('CodeEdit resizeEvent adjust height')
            self.setFixedHeight(int(self.document().size().height()) + 15)
            self.updateLineNumberAreaWidth()
            self.lineNumberArea.repaint()
            self.setSizeFinished.emit()

""" class CustomStyle(Style):
    default_style = ""
    background_color = '#14141c'
    styles = {
        token.Token: "#b2aaa4",
        token.Keyword: "#a6538c",  # 关键字为紫色   #a45c74, #fc6447
        token.Name.Class: "#6dae59",  # 类型名为绿色
        token.Name.Function: "#6dae59",  # 函数名为绿色
        token.Comment: "#aaa676",  # 注释为灰色
        token.String: "#399cc6",  # 字符串为蓝色
        token.Number: "#d2bd48",  # 数字为黄色
    } """

class QSyntaxStyle(QObject):
    def __init__(self, parent=None):
        super(QSyntaxStyle, self).__init__(parent)
        self.m_name = ""
        self.m_data = {}
        self.m_loaded = False

    def load(self, fl):
        reader = QXmlStreamReader(fl)

        while not reader.atEnd() and not reader.hasError():
            token = reader.readNext()

            if token == QXmlStreamReader.StartElement:
                if reader.name() == "style-scheme":
                    if reader.attributes().hasAttribute("name"):
                        self.m_name = reader.attributes().value("name")
                elif reader.name() == "style":
                    attributes = reader.attributes()
                    name = attributes.value("name")

                    format = QTextCharFormat()

                    if attributes.hasAttribute("background"):
                        format.setBackground(QColor(attributes.value("background")))

                    if attributes.hasAttribute("foreground"):
                        format.setForeground(QColor(attributes.value("foreground")))

                    if attributes.hasAttribute("bold") and attributes.value("bold") == "true":
                        format.setFontWeight(QFont.Bold)

                    if attributes.hasAttribute("italic") and attributes.value("italic") == "true":
                        format.setFontItalic(True)

                    if attributes.hasAttribute("underlineStyle"):
                        underline = attributes.value("underlineStyle")
                        s = QTextCharFormat.NoUnderline

                        if underline == "SingleUnderline":
                            s = QTextCharFormat.SingleUnderline
                        elif underline == "DashUnderline":
                            s = QTextCharFormat.DashUnderline
                        elif underline == "DotLine":
                            s = QTextCharFormat.DotLine
                        elif underline == "DashDotLine":
                            s = QTextCharFormat.DashDotLine
                        elif underline == "DashDotDotLine":
                            s = QTextCharFormat.DashDotDotLine
                        elif underline == "WaveUnderline":
                            s = QTextCharFormat.WaveUnderline
                        elif underline == "SpellCheckUnderline":
                            s = QTextCharFormat.SpellCheckUnderline
                        else:
                            print(f"Unknown underline value {underline}")

                        format.setUnderlineStyle(s)

                    self.m_data[name] = format

        self.m_loaded = not reader.hasError()
        return self.m_loaded

    def name(self):
        return self.m_name

    def getFormat(self, name):
        return self.m_data.get(name, QTextCharFormat())

    def isLoaded(self):
        return self.m_loaded

    @staticmethod
    def defaultStyle():
        if not hasattr(QSyntaxStyle.defaultStyle, "style"):
            QSyntaxStyle.defaultStyle.style = QSyntaxStyle()
            if not QSyntaxStyle.defaultStyle.style.isLoaded():
                # 初始化资源文件
                # Q_INIT_RESOURCE(qcodeeditor_resources)
                fl = QFile(code_theme_file_path)

                if not fl.open(QIODevice.ReadOnly):
                    print("Can't open default style file.")
                    return QSyntaxStyle.defaultStyle.style

                data = fl.readAll().data().decode('utf-8')
                if not QSyntaxStyle.defaultStyle.style.load(data):
                    print("Can't load default style.")
        return QSyntaxStyle.defaultStyle.style

class QStyleSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument = None):
        super(QStyleSyntaxHighlighter, self).__init__(document)
        self.m_syntaxStyle = None

    def setSyntaxStyle(self, style: QSyntaxStyle):
        self.m_syntaxStyle = style

    def syntaxStyle(self) -> QSyntaxStyle:
        return self.m_syntaxStyle

class QCXXHighlighter(QStyleSyntaxHighlighter):
    def __init__(self, document: QTextDocument = None):
        super(QCXXHighlighter, self).__init__(document)
        self.highlight_rules = []  # 存储高亮规则的列表
        self.m_highlightDotRules = []
        
        # 初始化正则表达式模式：
        self.include_pattern = QRegularExpression(r'(^\s*#\s*include\s*([<"][^:?"<>\|]+[">]))')  # #include 语句
        self.function_pattern = QRegularExpression(r'(\b([_a-zA-Z][_a-zA-Z0-9]*\s+)?((?:[_a-zA-Z][_a-zA-Z0-9]*\s*::\s*)*[_a-zA-Z][_a-zA-Z0-9]*)(?=\s*\())')  # 函数声明
        self.m_functionPattern = QRegularExpression(r"(\b([A-Za-z0-9_]+(?:\.))*([A-Za-z0-9_]+)(?=\s*\())")
        """ self.def_type_pattern = QRegularExpression(r'(\b([_a-zA-Z][_a-zA-Z0-9]*)\s+[_a-zA-Z][_a-zA-Z0-9]*\s*[;=])') """  # 类型定义
        self.def_type_pattern = QRegularExpression(r'(\b([_a-zA-Z][_a-zA-Z0-9]*)\s+([_a-zA-Z][_a-zA-Z0-9]*)\s*(?=[;=]))')
        self.m_variPattern = QRegularExpression(r"(\b[A-Za-z_][A-Za-z0-9_]*\b)")
        self.comment_start_pattern = QRegularExpression(r'/\*')  # 多行注释开始 /*
        self.comment_end_pattern = QRegularExpression(r'\*/')    # 多行注释结束 */
        
        # 从 XML 文件加载语法规则
        fl = QFile("config/cpp.xml")
        if not fl.open(QFile.ReadOnly):
            return
        
        language = QLanguage(fl)
        if not language.isLoaded():
            return
        
        # 解析语言规则并添加到高亮规则中
        keys = language.keys()
        for key in keys:
            names = language.names(key)
            for name in names:
                self.highlight_rules.append({
                    'pattern': QRegularExpression(rf'\b{name}\b'),  # 匹配单词边界
                    'format': key  # 对应的格式类型
                })
        
        # 添加数字的高亮规则
        self.highlight_rules.append({
            'pattern': QRegularExpression(r'(?<=\b|\s|^)(?i)(?:(?:(?:(?:(?:\d+(?:\'\d+)*)?\.(?:\d+(?:\'\d+)*)(?:e[+-]?(?:\d+(?:\'\d+)*))?)|(?:(?:\d+(?:\'\d+)*)\.(?:e[+-]?(?:\d+(?:\'\d+)*))?)|(?:(?:\d+(?:\'\d+)*)(?:e[+-]?(?:\d+(?:\'\d+)*)))|(?:0x(?:[0-9a-f]+(?:\'[0-9a-f]+)*)?\.(?:[0-9a-f]+(?:\'[0-9a-f]+)*)(?:p[+-]?(?:\d+(?:\'\d+)*)))|(?:0x(?:[0-9a-f]+(?:\'[0-9a-f]+)*)\.?(?:p[+-]?(?:\d+(?:\'\d+)*))))[lf]?)|(?:(?:(?:[1-9]\d*(?:\'\d+)*)|(?:0[0-7]*(?:\'[0-7]+)*)|(?:0x[0-9a-f]+(?:\'[0-9a-f]+)*)|(?:0b[01]+(?:\'[01]+)*))(?:u?l{0,2}|l{0,2}u?)))(?=\b|\s|$)'),
            'format': 'Number'
        })

        self.m_highlightDotRules.append((
            QRegularExpression(r"((?<!\d)\.(?!\d))"),
            "Dot"
        ))

        # 添加字符串的高亮规则
        self.highlight_rules.append({
            'pattern': QRegularExpression(r'("[^\n"]*")'),  # 匹配双引号内的内容
            'format': 'String'
        })
        
        # 添加预处理指令的高亮规则（如 #define）
        self.highlight_rules.append({
            'pattern': QRegularExpression(r'(#[a-zA-Z_]+)'),
            'format': 'Preprocessor'
        })
        
        # 添加单行注释的高亮规则
        self.highlight_rules.append({
            'pattern': QRegularExpression(r'(//[^\n]*)'),  # 从 // 到行尾
            'format': 'Comment'
        })

    def highlightBlock(self, text):
        match_iterator = self.m_variPattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Vari")
            )

        match_iterator = self.function_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # 高亮返回类型部分
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Type")
            )
            # 高亮函数名部分
            self.setFormat(
                match.capturedStart(3),
                match.capturedLength(3),
                self.syntaxStyle().getFormat("Function")
            )

        match_iterator = self.m_functionPattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Type")
            )
            self.setFormat(
                match.capturedStart(3),
                match.capturedLength(3),
                self.syntaxStyle().getFormat("Function")
            )

        match_iterator = self.def_type_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # 高亮类型名部分
            self.setFormat(
                match.capturedStart(3),
                match.capturedLength(3),
                self.syntaxStyle().getFormat("DefType")
            )

        for rule in self.m_highlightDotRules:
            pattern, format_name = rule
            match_iterator = pattern.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    self.syntaxStyle().getFormat(format_name)
                )

        match_iterator = self.include_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            # 高亮整个 #include 指令
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Preprocessor")
            )
            # 高亮包含的文件名部分
            self.setFormat(
                match.capturedStart(2),
                match.capturedLength(2),
                self.syntaxStyle().getFormat("String")
            )

        for rule in self.highlight_rules:
            match_iterator = rule['pattern'].globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    self.syntaxStyle().getFormat(rule['format'])
                )

        self.setCurrentBlockState(0)  # 初始状态
        
        start_index = 0
        if self.previousBlockState() != 1:  # 如果前一个块不在注释中
            start_match = self.comment_start_pattern.match(text)
            start_index = start_match.capturedStart()
        
        while start_index >= 0:
            end_match = self.comment_end_pattern.match(text, start_index)
            end_index = end_match.capturedStart()
            comment_length = 0
            
            if end_index == -1:  # 没有找到注释结束
                self.setCurrentBlockState(1)  # 设置状态为"在注释中"
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + end_match.capturedLength()
            
            self.setFormat(
                start_index,
                comment_length,
                self.syntaxStyle().getFormat("Comment")
            )
            
            # 查找下一个注释开始
            next_match = self.comment_start_pattern.match(text, start_index + comment_length)
            start_index = next_match.capturedStart()

class QPythonHighlighter(QStyleSyntaxHighlighter):
    def __init__(self, document: QTextDocument = None):
        super(QPythonHighlighter, self).__init__(document)
        self.m_highlightRules = []
        self.m_highlightDotRules = []
        self.m_highlightStringRules = []
        self.m_highlightBlockRules = []
        """ self.m_includePattern = QRegularExpression(r"(import \w+)") """
        self.m_includePattern = QRegularExpression(r"(?:from\s+(\w+(?:\.\w+)*)\s+)?import\s+((?:\w+(?:\s+as\s+\w+)?)(?:\s*,\s*\w+(?:\s+as\s+\w+)?)*|\*)")
        """ self.m_functionPattern = QRegularExpression(r"(\b([A-Za-z0-9_]+(?:\.))*([A-Za-z0-9_]+)(?=\())") """
        self.m_functionPattern = QRegularExpression(r"(\b([A-Za-z0-9_]+(?:\.))*([A-Za-z0-9_]+)(?=\s*\())")
        """ self.m_defTypePattern = QRegularExpression(r"(\b([A-Za-z0-9_]+)\s+[A-Za-z]{1}[A-Za-z0-9_]+\s*[;=])") """
        self.m_defTypePattern = QRegularExpression(r"(\b[A-Za-z_][A-Za-z0-9_]*\s*(?=\+?\s*=))")
        self.m_variPattern = QRegularExpression(r"(\b[A-Za-z_][A-Za-z0-9_]*\b)")

        """ current_dir = QDir.currentPath() """
        """ print("当前工作目录:", current_dir) """
        # Load the language definitions from the XML file
        fl = QFile("config/python.xml")
        if not fl.open(QFile.ReadOnly):
            """ print("Can't open python style file") """
            return

        # Assuming QLanguage is a custom class you've implemented
        language = QLanguage(fl)
        if not language.isLoaded():
            return

        keys = language.keys()
        for key in keys:
            names = language.names(key)
            for name in names:
                self.m_highlightRules.append((
                    QRegularExpression(fr"(\b{name}\b)"),
                    key
                ))

        # Following rules have higher priority to display
        # than language specific keys
        # So they must be applied at last.

        # Numbers
        """ QRegularExpression(r"(\b(0b|0x){0,1}[\d.']+\b)"), """
        self.m_highlightRules.append((
            QRegularExpression(r"(\b(0b|0x)?(\d{1,3}(_?\d{3})*(\.\d+)?)\b)"),
            "Number"
        ))

        self.m_highlightDotRules.append((
            QRegularExpression(r"((?<!\d)\.(?!\d))"),
            "Dot"
        ))
        
        # Strings
        self.m_highlightStringRules.append((
            QRegularExpression(r'("[^\n"]*")'),
            "String"
        ))
        self.m_highlightStringRules.append((
            QRegularExpression(r"('[^\n']*')"),
            "String"
        ))
        
        # Single line comment
        self.m_highlightRules.append((
            QRegularExpression(r"#[^\n]*"),
            "Comment"
        ))
        
        # Multiline string
        self.m_highlightBlockRules.append((
            QRegularExpression(r'(""")'),
            QRegularExpression(r'(""")'),
            "String"
        ))
        self.m_highlightBlockRules.append((
            QRegularExpression(r"(''')"),
            QRegularExpression(r"(''')"),
            "String"
        ))
        #
        """ self.hCount = 0 """

    def highlightBlock(self, text: str) -> None:
        match_iterator = self.m_variPattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Vari")
            )

        # Checking for function
        match_iterator = self.m_functionPattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Type")
            )
            self.setFormat(
                match.capturedStart(3),
                match.capturedLength(3),
                self.syntaxStyle().getFormat("Function")
            )
        
        match_iterator = self.m_defTypePattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("DefType")
            )

        for rule in self.m_highlightDotRules:
            pattern, format_name = rule
            match_iterator = pattern.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    self.syntaxStyle().getFormat(format_name)
                )

        match_iterator = self.m_includePattern.globalMatch(text)
        
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Module")
            )

        # Apply regular highlighting rules
        for rule in self.m_highlightRules:
            pattern, format_name = rule
            match_iterator = pattern.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    self.syntaxStyle().getFormat(format_name)
                )
        
        # Handle multi-line highlighting rules (like triple-quoted strings)
        self.setCurrentBlockState(0)
        start_index = 0
        """ self.hCount += 1 """
        """ print('hCount:', self.hCount) """
        """ print('1 currentBlockState:', self.currentBlock(), self.currentBlockState()) """
        highlight_rule_id = self.previousBlockState()
        """ print('2 previousBlockState:', self.currentBlock(), highlight_rule_id) """
        
        start_index = 0
        block_start_index_list = []

        if highlight_rule_id < 1 or highlight_rule_id > len(self.m_highlightBlockRules):
            for i, block_rule in enumerate(self.m_highlightBlockRules):
                start_pattern_tmp, _, _ = block_rule
                """ start_index_tmp = text.indexOf(start_pattern_tmp) """
                start_match_tmp = start_pattern_tmp.match(text)  # 执行正则匹配
                start_index_tmp = start_match_tmp.capturedStart()
                block_start_index_list.append(start_index_tmp)

                """ highlight_rule_id = i + 1
                while start_index >= 0:

                    # Should be + length of start pattern
                    end_match = end_pattern.match(text, start_index + start_match.capturedLength())
                    end_index = end_match.capturedStart()
                    match_length = 0

                    if end_index == -1:
                        print('3:', self.currentBlock())
                        self.setCurrentBlockState(highlight_rule_id)
                        match_length = len(text) - start_index
                    else:
                        match_length = end_index - start_index + end_match.capturedLength()

                    self.setFormat(
                        start_index,
                        match_length,
                        self.syntaxStyle().getFormat(format_name)
                    )

                    start_match = start_pattern.match(text, start_index + match_length)  # 执行正则匹配
                    start_index = start_match.capturedStart() """
                
                """ if start_index >= 0:
                    highlight_rule_id = i + 1
                    break """

            block_start_min_index = -1
            for start_index_tmp in block_start_index_list:
                if start_index_tmp >= 0:
                    if block_start_min_index == -1:
                        block_start_min_index = start_index_tmp
                    elif start_index_tmp < block_start_min_index:
                        block_start_min_index = start_index_tmp
            if block_start_min_index != -1:
                for i, start_index_tmp in enumerate(block_start_index_list):
                    if start_index_tmp == block_start_min_index:
                        highlight_rule_id = i + 1
                        break
            start_index = block_start_min_index

        """ print('start_index, start list:', start_index, block_start_index_list) """
        if start_index >= 0:
            block_rule = self.m_highlightBlockRules[highlight_rule_id - 1]
            start_pattern, end_pattern, format_name = block_rule
            if self.previousBlockState() < 1:
                start_match = start_pattern.match(text)
            """ print('get block_rule index:', highlight_rule_id - 1) """

        if len(text) != 0 and start_index != 0:
            """ for rule in self.m_highlightStringRules:
                string_pattern, string_format_name = rule
                if start_index == -1:
                    match_iterator = string_pattern.globalMatch(text)
                else:
                    match_iterator = string_pattern.globalMatch(text[:start_index])

                while match_iterator.hasNext():
                    match = match_iterator.next()
                    self.setFormat(
                        match.capturedStart(),
                        match.capturedLength(),
                        self.syntaxStyle().getFormat(string_format_name)
                    )
                print('stringPatternStart0') """

            self.singleLineStrHighlight(text, 0, start_index)

        while start_index >= 0:
            """ print('highlight_rule_id start_index:', highlight_rule_id, start_index)
            if highlight_rule_id == 0:
                print('highlight_rule_id:')
                print(self.m_highlightBlockRules[highlight_rule_id - 1]) """

            # Should be + length of start pattern
            if self.previousBlockState() > 0 and start_index == 0:
                end_match = end_pattern.match(text)
            else:
                end_match = end_pattern.match(text, start_index + start_match.capturedLength())
                """ print('start capturedLength:', start_match.capturedLength()) """
            end_index = end_match.capturedStart()
            """ print('end_index:', end_index) """
            match_length = 0

            if end_index == -1:
                """ print('3:', self.currentBlock()) """
                self.setCurrentBlockState(highlight_rule_id)
                match_length = len(text) - start_index
                """ print('len(text), start_index, match_length:', len(text), start_index, match_length) """
            else:
                match_length = end_index - start_index + end_match.capturedLength()
                """ print('end capturedLength, end_index, match_length:', end_match.capturedLength(), end_index, match_length) """

            self.setFormat(
                start_index,
                match_length,
                self.syntaxStyle().getFormat(format_name)
            )
            """ print('start_index, match_length:', start_index, match_length) """
            stringPatternStart = start_index + match_length

            """ start_index = text.indexOf(start_pattern, start_index + match_length) """
            """ start_match = start_pattern.match(text, start_index + match_length)  # 执行正则匹配
            start_index = start_match.capturedStart()
            print('match_length, start_index:', match_length, start_index) """

            block_start_index_list = []
            for i, block_rule in enumerate(self.m_highlightBlockRules):
                start_pattern_tmp, _, _ = block_rule
                """ start_index_tmp = text.indexOf(start_pattern_tmp) """
                start_match_tmp = start_pattern_tmp.match(text, start_index + match_length)  # 执行正则匹配
                """ print('start_index, match_length, start_match:', start_index, match_length, start_match_tmp) """
                start_index_tmp = start_match_tmp.capturedStart()
                block_start_index_list.append(start_index_tmp)

            block_start_min_index = -1
            for start_index_tmp in block_start_index_list:
                if start_index_tmp >= 0:
                    if block_start_min_index == -1:
                        block_start_min_index = start_index_tmp
                    elif start_index_tmp < block_start_min_index:
                        block_start_min_index = start_index_tmp
            if block_start_min_index != -1:
                for i, start_index_tmp in enumerate(block_start_index_list):
                    if start_index_tmp == block_start_min_index:
                        highlight_rule_id = i + 1
                        break

            """ print('start_index, start list:', start_index, block_start_index_list) """
            if block_start_min_index >= 0:
                block_rule = self.m_highlightBlockRules[highlight_rule_id - 1]
                start_pattern, end_pattern, format_name = block_rule
                start_match = start_pattern.match(text, start_index + match_length)
                """ print('start capturedLength, start_index, match_length:', start_match.capturedLength(), start_index, match_length)
                print('get block_rule index:', highlight_rule_id - 1) """
            start_index = block_start_min_index
            """ print('start_index', start_index) """

            if not (stringPatternStart == len(text) or stringPatternStart == start_index):
                """ for rule in self.m_highlightStringRules:
                    string_pattern, string_format_name = rule
                    if start_index == -1:
                        match_iterator = string_pattern.globalMatch(text[stringPatternStart:])
                    else:
                        match_iterator = string_pattern.globalMatch(text[stringPatternStart:start_index])

                    while match_iterator.hasNext():
                        match = match_iterator.next()
                        self.setFormat(
                            match.capturedStart() + stringPatternStart,
                            match.capturedLength(),
                            self.syntaxStyle().getFormat(string_format_name)
                        )
                    print('stringPatternStart1') """

                self.singleLineStrHighlight(text, stringPatternStart, start_index)

    def singleLineStrHighlight(self, text, stringPatternStart, stringPatternEnd):
        string_index = 0
        string_length = 0
        string_rule_id = 0

        string_index_list = []
        for rule in self.m_highlightStringRules:
            string_pattern_tmp, _ = rule
            if stringPatternEnd == -1:
                string_match_tmp = string_pattern_tmp.match(text[stringPatternStart:])
            else:
                string_match_tmp = string_pattern_tmp.match(text[stringPatternStart:stringPatternEnd])
            string_index_tmp = string_match_tmp.capturedStart()
            string_index_list.append(string_index_tmp)

        string_min_index = -1
        for string_index_tmp in string_index_list:
            if string_index_tmp >= 0:
                if string_min_index == -1:
                    string_min_index = string_index_tmp
                elif string_index_tmp < string_min_index:
                    string_min_index = string_index_tmp
        if string_min_index != -1:
            for i, string_index_tmp in enumerate(string_index_list):
                if string_index_tmp == string_min_index:
                    string_rule_id = i + 1
                    break

        while(string_min_index >= 0):
            rule = self.m_highlightStringRules[string_rule_id - 1]
            string_pattern, string_format_name = rule
            """ if self.previousBlockState() < 1: """
            if stringPatternEnd == -1:
                string_match = string_pattern.match(text[stringPatternStart:], string_index + string_length)
            else:
                string_match = string_pattern.match(text[stringPatternStart:stringPatternEnd], string_index + string_length)
            string_index = string_min_index
            string_length = string_match.capturedLength()
            self.setFormat(
                string_index + stringPatternStart,
                string_length,
                self.syntaxStyle().getFormat(string_format_name)
            )

            string_index_list = []
            for rule in self.m_highlightStringRules:
                string_pattern_tmp, _ = rule
                if stringPatternEnd == -1:
                    string_match_tmp = string_pattern_tmp.match(text[stringPatternStart:], string_index + string_length)
                else:
                    string_match_tmp = string_pattern_tmp.match(text[stringPatternStart:stringPatternEnd], string_index + string_length)
                string_index_tmp = string_match_tmp.capturedStart()
                string_index_list.append(string_index_tmp)

            string_min_index = -1
            for string_index_tmp in string_index_list:
                if string_index_tmp >= 0:
                    if string_min_index == -1:
                        string_min_index = string_index_tmp
                    elif string_index_tmp < string_min_index:
                        string_min_index = string_index_tmp
            if string_min_index != -1:
                for i, string_index_tmp in enumerate(string_index_list):
                    if string_index_tmp == string_min_index:
                        string_rule_id = i + 1
                        break

class QGLSLHighlighter(QStyleSyntaxHighlighter):
    def __init__(self, document: QTextDocument = None):
        super(QGLSLHighlighter, self).__init__(document)
        
        self.m_highlightRules = []
        
        # 初始化正则表达式模式
        self.m_includePattern = QRegularExpression(r'(#include\s+([<"][a-zA-Z0-9*._]+[">]))')
        self.m_functionPattern = QRegularExpression(r'(\b([A-Za-z0-9_]+(?:\s+|::))*([A-Za-z0-9_]+)(?=\())')
        self.m_defTypePattern = QRegularExpression(r'(\b([A-Za-z0-9_]+)\s+[A-Za-z]{1}[A-Za-z0-9_]+\s*[;=])')
        self.m_commentStartPattern = QRegularExpression(r'(/\*)')
        self.m_commentEndPattern = QRegularExpression(r'(\*/)')
        
        # 加载语法高亮规则
        self.loadHighlightRules()
        
    def loadHighlightRules(self):
        # Load the language definitions from the XML file
        fl = QFile("config/glsl.xml")
        if not fl.open(QFile.ReadOnly):
            """ print("Can't open glsl style file") """
            return

        # Assuming QLanguage is a custom class you've implemented
        language = QLanguage(fl)
        if not language.isLoaded():
            return

        keys = language.keys()
        for key in keys:
            names = language.names(key)
            for name in names:
                self.m_highlightRules.append((
                    QRegularExpression(fr"(\b{name}\b)"),
                    key
                ))

        # 数字
        self.m_highlightRules.append((
            QRegularExpression(r'\b(0b|0x){0,1}[\d\']+\b'),
            "Number"
        ))
        
        # 预处理指令
        self.m_highlightRules.append((
            QRegularExpression(r'#[a-zA-Z_]+'),
            "Preprocessor"
        ))
        
        # 单行注释
        self.m_highlightRules.append((
            QRegularExpression('//[^\n]*'),
            "Comment"
        ))
        
        # 这里可以添加更多GLSL特定的关键字规则
        
    def highlightBlock(self, text: str) -> None:
        # 处理#include指令
        matchIterator = self.m_includePattern.globalMatch(text)
        while matchIterator.hasNext():
            match = matchIterator.next()
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Preprocessor")
            )
            self.setFormat(
                match.capturedStart(2),
                match.capturedLength(2),
                self.syntaxStyle().getFormat("String")
            )
        
        # 处理函数
        matchIterator = self.m_functionPattern.globalMatch(text)
        while matchIterator.hasNext():
            match = matchIterator.next()
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.syntaxStyle().getFormat("Type")
            )
            self.setFormat(
                match.capturedStart(3),
                match.capturedLength(3),
                self.syntaxStyle().getFormat("Function")
            )
        
        # 应用常规高亮规则
        for rule in self.m_highlightRules:
            pattern, formatName = rule
            matchIterator = pattern.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    self.syntaxStyle().getFormat(formatName)
                )
        
        # 处理多行注释
        self.setCurrentBlockState(0)
        startIndex = 0
        if self.previousBlockState() != 1:
            match = self.m_commentStartPattern.match(text)
            startIndex = match.capturedStart()
        
        while startIndex >= 0:
            match = self.m_commentEndPattern.match(text, startIndex)
            endIndex = match.capturedStart()
            commentLength = 0
            
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + match.capturedLength()
            
            self.setFormat(
                startIndex,
                commentLength,
                self.syntaxStyle().getFormat("Comment")
            )
            match = self.m_commentStartPattern.match(text, startIndex + commentLength)
            startIndex = match.capturedStart()

class QLuaHighlighter(QStyleSyntaxHighlighter):
    def __init__(self, document: QTextDocument = None):
        super(QLuaHighlighter, self).__init__(document)
        # 初始化高亮规则
        self.highlight_rules = []
        self.highlight_block_rules = []
        
        # 正则表达式模式
        self.require_pattern = QRegularExpression(r"(require\s*([(\"'][a-zA-Z0-9*._]+['\")]))")
        self.function_pattern = QRegularExpression(r"(\b([A-Za-z0-9_]+(?:\s+|::))*([A-Za-z0-9_]+)(?=\())")
        self.def_type_pattern = QRegularExpression(r"(\b([A-Za-z0-9_]+)\s+([A-Za-z]{1}[A-Za-z0-9_]+)\s*[=])")
        
        # Load the language definitions from the XML file
        fl = QFile("config/lua.xml")
        if not fl.open(QFile.ReadOnly):
            """ print("Can't open lua style file") """
            return

        # Assuming QLanguage is a custom class you've implemented
        language = QLanguage(fl)
        if not language.isLoaded():
            return

        keys = language.keys()
        for key in keys:
            names = language.names(key)
            for name in names:
                self.highlight_rules.append((
                    QRegularExpression(fr"(\b\s{0,1}{name}\s{0,1}\b)"),
                    key
                ))

        # 数字
        self.highlight_rules.append((
            QRegularExpression(r"\b(0b|0x){0,1}[\d.']+\b"),
            "Number"
        ))
        
        # 字符串
        self.highlight_rules.append((
            QRegularExpression(r"[\"][^\n\"]*[\"]|['][^\n']*[']"),
            "String"
        ))
        
        # 预处理器
        self.highlight_rules.append((
            QRegularExpression(r"#\![a-zA-Z_]+"),
            "Preprocessor"
        ))
        
        # 单行注释
        self.highlight_rules.append((
            QRegularExpression(r"--[^\n]*"),
            "Comment"
        ))
        
        # 多行规则
        # 多行注释
        self.highlight_block_rules.append({
            "start": QRegularExpression(r"--\[\["),
            "end": QRegularExpression(r"--\]\]"),
            "format": "Comment"
        })
        
        # 多行字符串
        self.highlight_block_rules.append({
            "start": QRegularExpression(r"\[\["),
            "end": QRegularExpression(r"\]\]"),
            "format": "String"
        })

    def highlightBlock(self, text):
        """高亮文本块"""
        # 检查require语句
        it = self.require_pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), 
                          self.syntaxStyle().getFormat("Preprocessor"))
            self.setFormat(match.capturedStart(2), match.capturedLength(2),
                          self.syntaxStyle().getFormat("String"))
        
        # 检查函数定义
        it = self.function_pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(),
                          self.syntaxStyle().getFormat("Type"))
            self.setFormat(match.capturedStart(3), match.capturedLength(3),
                          self.syntaxStyle().getFormat("Function"))
        
        # 检查类型定义
        it = self.def_type_pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(3), match.capturedLength(3),
                          self.syntaxStyle().getFormat("Type"))
        
        # 应用基础高亮规则
        for pattern, format_name in self.highlight_rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(),
                              self.syntaxStyle().getFormat(format_name))
        
        # 处理多行规则
        current_state = self.previousBlockState()
        start_index = 0
        
        if current_state < 1 or current_state > len(self.highlight_block_rules):
            for i, rule in enumerate(self.highlight_block_rules):
                match = rule["start"].match(text)
                start_index = match.capturedStart()
                if start_index >= 0:
                    current_state = i + 1
                    break
        
        while start_index >= 0:
            rule = self.highlight_block_rules[current_state - 1]
            match = rule["end"].match(text, start_index)
            end_index = match.capturedStart()
            match_length = 0
            
            if end_index == -1:
                self.setCurrentBlockState(current_state)
                match_length = len(text) - start_index
            else:
                match_length = end_index - start_index + match.capturedLength()
            
            self.setFormat(start_index, match_length, self.syntaxStyle().getFormat(rule["format"]))
            match = rule["start"].match(text, start_index + match_length)
            start_index = match.capturedStart()

class QLanguage(QObject):
    def __init__(self, device, parent=None):
        super(QLanguage, self).__init__(parent)
        self._loaded = False
        self._list = {}
        self.load(device)

    def load(self, device):
        if device is None:
            return False

        reader = QXmlStreamReader(device)

        name = ""
        string_list = []
        read_text = False

        while not reader.atEnd() and not reader.hasError():
            token_type = reader.readNext()

            if token_type == QXmlStreamReader.StartElement:
                if reader.name() == "section":
                    if string_list:
                        self._list[name] = string_list
                        string_list = []

                    name = reader.attributes().value("name")
                elif reader.name() == "name":
                    read_text = True

            elif token_type == QXmlStreamReader.Characters and read_text:
                string_list.append(reader.text())
                read_text = False

        if string_list:
            self._list[name] = string_list

        self._loaded = not reader.hasError()
        return self._loaded

    def keys(self):
        return list(self._list.keys())

    def names(self, key):
        return self._list.get(key, [])

    def isLoaded(self):
        return self._loaded

class CodeShow(QWidget):
    def __init__(self, codeText, lexerName='python', maxWidth=810, parent=None):
        super(CodeShow, self).__init__(parent)
        self.codeText = codeText
        self.maxWidth = maxWidth
        self.setObjectName('CodeShow')
        self.setStyleSheet('''
        #CodeShow {
            border-radius: 7px;
        }
        ''')
        #topWidget QWidget
        self.topWidget = QWidget()
        """ self.topWidget.setFixedHeight(20) """
        self.topWidget.setStyleSheet('''
        QWidget {
            background-color: #34343c;
            border-top-left-radius: 7px;
            border-top-right-radius: 7px;
        }
        ''')
        #label QLabel
        self.label = QLabel(lexerName)
        font = QFont()
        font.setPointSize(windowFontPointSize)
        self.label.setFont(font)
        self.palette = self.label.palette()
        """ self.palette.setColor(QPalette.Text, QColor(178, 170, 164)) """
        self.palette.setColor(QPalette.Text, QColor(Qt.white))
        self.label.setPalette(self.palette)
        self.label.adjustSize()
        #toggleThemeButton PushButton
        self.toggleThemeButton = PushButton(tipText='日间主题', tipOffsetX=15, tipOffsetY=35)
        self.toggleThemeButton.setFixedSize(self.label.height(), self.label.height())
        self.light_theme_images_path = os.path.join(images_dir, 'light_theme.png').replace('\\', '/')
        self.dark_theme_images_path = os.path.join(images_dir, 'dark_theme.png').replace('\\', '/')
        self.toggleThemeButton.setIcon(QIcon(f"{self.light_theme_images_path}"))
        self.toggleThemeButton.setIconSize(QSize(20, 20))
        self.toggleThemeButton.setStyleSheet('''
        QPushButton{
            border: none;
            background: transparent;
        }
        ''')
        self.toggleThemeButton.clicked.connect(self.toggleThemeStyle)
        self.isLightThemeStyle = False
        #wordWrapButton PushButton
        self.wordWrapButton = PushButton(tipText='折叠成单行', tipOffsetX=15, tipOffsetY=35)
        self.wordWrapButton.setFixedSize(self.label.height(), self.label.height())
        self.light_word_wrap_images_path = os.path.join(images_dir, 'light_word_wrap.png').replace('\\', '/')
        self.light_single_line_images_path = os.path.join(images_dir, 'light_single_line.png').replace('\\', '/')
        self.dark_word_wrap_images_path = os.path.join(images_dir, 'dark_word_wrap.png').replace('\\', '/')
        self.dark_single_line_images_path = os.path.join(images_dir, 'dark_single_line.png').replace('\\', '/')
        self.wordWrapButton.setIcon(QIcon(f"{self.light_single_line_images_path}"))
        self.wordWrapButton.setIconSize(QSize(20, 20))
        self.wordWrapButton.setStyleSheet('''
        QPushButton{
            border: none;
            background: transparent;
        }
        ''')
        self.wordWrapButton.clicked.connect(self.setLineWordWrapMode)
        self.isWordWrap = True
        #codeCopyButton PushButton
        self.codeCopyButton = PushButton(tipText='复制代码', tipOffsetX=15, tipOffsetY=35)
        self.codeCopyButton.setFixedSize(self.label.height(), self.label.height())
        self.light_code_copy_images_path = os.path.join(images_dir, 'light_code_copy.png').replace('\\', '/')
        self.dark_code_copy_images_path = os.path.join(images_dir, 'dark_code_copy.png').replace('\\', '/')
        self.codeCopyButton.setIcon(QIcon(f"{self.light_code_copy_images_path}"))
        self.codeCopyButton.setIconSize(QSize(20, 20))
        self.codeCopyButton.setStyleSheet('''
        QPushButton{
            border: none;
            background: transparent;
        }
        ''')
        self.codeCopyButton.clicked.connect(self.copyCode)
        #QClipboard
        self.clip = QApplication.clipboard()
        #topSubLeftWidget QWidget
        self.topSubLeftWidget = QWidget()
        self.topSubLeftWidget.setFixedHeight(self.label.height())
        self.topSubLeftHLayout = QHBoxLayout()
        self.topSubLeftWidget.setLayout(self.topSubLeftHLayout)
        self.topSubLeftHLayout.setAlignment(Qt.AlignLeft)
        self.topSubLeftHLayout.setContentsMargins(0, 0, 0, 0)
        self.topSubLeftHLayout.addWidget(self.label)
        #topSubRightWidget QWidget
        self.topSubRightWidget = QWidget()
        self.topSubRightWidget.setFixedHeight(self.label.height())
        self.topSubRightHLayout = QHBoxLayout()
        self.topSubRightWidget.setLayout(self.topSubRightHLayout)
        self.topSubRightHLayout.setAlignment(Qt.AlignRight)
        self.topSubRightHLayout.setContentsMargins(0, 0, 0, 0)
        self.topSubRightHLayout.setSpacing(0)
        self.topSubRightHLayout.addWidget(self.toggleThemeButton)
        self.topSubRightHLayout.addWidget(self.wordWrapButton)
        self.topSubRightHLayout.addWidget(self.codeCopyButton)
        #topHLayout QHBoxLayout
        self.topHLayout = QHBoxLayout()
        self.topWidget.setLayout(self.topHLayout)
        self.topHLayout.addWidget(self.topSubLeftWidget, 0, Qt.AlignLeft)
        self.topHLayout.addWidget(self.topSubRightWidget, 0, Qt.AlignRight)
        self.topHLayout.setContentsMargins(10, 0, 10, 0)
        self.topWidget.setFixedHeight(self.label.height())
        #CodeEdit
        self.codeEdit = CodeEdit(self.maxWidth)
        self.codeEdit.setSizeFinished.connect(self.OnSizeFinished)
        self.codeEdit.highlightCode(codeText, lexerName=lexerName)
        """ self.codeEdit.setWordWrapMode(QTextOption.WordWrap)
        self.codeEdit.setLineWrapMode(QTextEdit.WidgetWidth) """
        """ self.codeEdit.setFixedHeight(int(self.codeEdit.document().size().height()) + 15)
        self.codeEdit.updateLineNumberAreaWidth()
        self.codeEdit.lineNumberArea.repaint()
        self.codeEdit.setSizeFinished.emit() """
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.topWidget)
        self.mainVLayout.addWidget(self.codeEdit)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        #singleShot
        QTimer.singleShot(1, self.onSetText)

    def onSetText(self):
        self.codeEdit.setText(self.codeText)

    def setText(self, codeText, lexerName='python'):
        self.codeEdit.highlightCode(codeText, lexerName=lexerName)
        self.codeEdit.setFixedWidth(self.maxWidth)

    def OnSizeFinished(self):
        self.setFixedSize(self.maxWidth, self.codeEdit.height() + self.topWidget.height())
        print('CodeShow:', self.height(), self.codeEdit.height(), self.topWidget.height())

    def connectCodeCopyButtonClick(self, fun):
        self.codeCopyButton.clicked.connect(fun)

    def hasSelectedText(self):
        return self.codeEdit.textCursor().hasSelection()

    def getSelectedText(self):
        return self.codeEdit.textCursor().selectedText()

    def toggleThemeStyle(self):
        self.isLightThemeStyle = not self.isLightThemeStyle
        if self.isLightThemeStyle:
            self.topWidget.setStyleSheet('''
            QWidget {
                background-color: #ccccc4;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
            }
            ''')
            self.palette = self.label.palette()
            self.palette.setColor(QPalette.Text, QColor(Qt.black))
            self.label.setPalette(self.palette)
            self.toggleThemeButton.setIcon(QIcon(f"{self.dark_theme_images_path}"))
            self.toggleThemeButton.tipText = '夜间主题'
            if self.isWordWrap:
                self.wordWrapButton.setIcon(QIcon(f"{self.dark_single_line_images_path}"))
            else:
                self.wordWrapButton.setIcon(QIcon(f"{self.dark_word_wrap_images_path}"))
            self.codeCopyButton.setIcon(QIcon(f"{self.dark_code_copy_images_path}"))
        else:
            self.topWidget.setStyleSheet('''
            QWidget {
                background-color: #34343c;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
            }
            ''')
            self.palette = self.label.palette()
            self.palette.setColor(QPalette.Text, QColor(Qt.white))
            self.label.setPalette(self.palette)
            self.toggleThemeButton.setIcon(QIcon(f"{self.light_theme_images_path}"))
            self.toggleThemeButton.tipText = '日间主题'
            if self.isWordWrap:
                self.wordWrapButton.setIcon(QIcon(f"{self.light_single_line_images_path}"))
            else:
                self.wordWrapButton.setIcon(QIcon(f"{self.light_word_wrap_images_path}"))
            self.codeCopyButton.setIcon(QIcon(f"{self.light_code_copy_images_path}"))
        self.codeEdit.setThemeStyle(self.isLightThemeStyle)

    def setLineWordWrapMode(self):
        self.isWordWrap = not self.isWordWrap
        if self.isWordWrap:
            self.codeEdit.setWordWrapMode(QTextOption.WordWrap)
            self.codeEdit.setLineWrapMode(QTextEdit.WidgetWidth)
            if self.isLightThemeStyle:
                self.wordWrapButton.setIcon(QIcon(f"{self.dark_single_line_images_path}"))
            else:
                self.wordWrapButton.setIcon(QIcon(f"{self.light_single_line_images_path}"))
            self.wordWrapButton.tipText = '折叠成单行'
        else:
            self.codeEdit.setWordWrapMode(QTextOption.NoWrap)
            self.codeEdit.setLineWrapMode(QTextEdit.NoWrap)
            if self.isLightThemeStyle:
                self.wordWrapButton.setIcon(QIcon(f"{self.dark_word_wrap_images_path}"))
            else:
                self.wordWrapButton.setIcon(QIcon(f"{self.light_word_wrap_images_path}"))
            self.wordWrapButton.tipText = '自动换行'
        self.codeEdit.adjustSize()

    def copyCode(self):
        self.clip.setText(self.codeText)

class MessageWidget(QWidget):
    """ thinkTextRecvEnd = pyqtSignal() """
    resizeFinished = pyqtSignal()
    setTexting = pyqtSignal(bool)

    def __init__(self, text, copyFun, renewResponseFun, listWidget, isUser=True, thinkIsExpand=True, textMaxWidth=877, parent=None):
        super(MessageWidget, self).__init__(parent)
        self.listWidget = listWidget
        self.text = text
        self.textMaxWidth = textMaxWidth
        self.isUser = isUser
        self.copyFun = copyFun
        #ImageLabel
        self.imageLabel = ImageLabel(isUser=self.isUser)
        #textWidget TextWidget
        self.textWidget = TextWidget(isUser=isUser)
        #textLayout QVBoxLayout
        self.textLayout = QVBoxLayout()
        self.textWidget.setLayout(self.textLayout)
        #textBoxWidget TextBoxWidget
        self.textBoxWidget = TextBoxWidget()
        #textBoxLayout QVBoxLayout
        self.textBoxLayout = QVBoxLayout()
        self.textBoxWidget.setLayout(self.textBoxLayout)
        #thinkButtonHaveCreated
        self.thinkButtonHaveCreated = False
        if not self.isUser:
            #
            self.thinkTextShowList = []
            self.thinkCodeShowList = []
            self.resultTextShowList = []
            self.resultCodeShowList = []
            #thinkBackWidget ThinkBackWidget
            self.thinkBackWidget = ThinkBackWidget(self)
            #thinkBackVLayout QVBoxLayout
            self.thinkBackVLayout = QVBoxLayout()
            self.thinkBackWidget.setLayout(self.thinkBackVLayout)
            self.thinkBackVLayout.setContentsMargins(30, 0, 15, 0)
            self.thinkBackVLayout.setSpacing(0)
            #thinkIsExpand
            self.thinkIsExpand = thinkIsExpand
            """ #
            self.thinkTextRecvEnd.connect(self.thinkToggleWidget) """
            #
            self.thinkWidgetSizeFinshedCount = 0
            self.textShowSizeFinshedCount = 0
            #
            self.thinkText = ''
            self.resultText = ''
            #
            self.thinkTextIsRecvEnd = False
            self.isRecvFirst = True
            if '<think>' in self.text:
                textList = self.text.split('<think>')
                tempText = textList[1]
                if '</think>' in tempText:
                    textList2 = tempText.split('</think>')
                    self.thinkText = textList2[0]
                    self.resultText = self.text.split('<think>' + self.thinkText + '</think>')[1]
                    self.thinkTextIsRecvEnd = True
                else:
                    self.thinkText = tempText
            elif not (self.text in '<think>' or self.text == ''):
                self.resultText = self.text
                self.thinkTextIsRecvEnd = True
            #ThinkWidget
            thinkSplitTextList = []
            thinkTempTextList = []
            thinkTempText = self.thinkText
            if self.thinkText != '':
                thinkCodeBlocks = self.extract_code_blocks(self.thinkText)
                """ lexerNameList = ['c', 'cpp', 'python', 'java', 'javascript']
                for index, codeBlock in enumerate(thinkCodeBlocks):
                    if codeBlock != []:
                        for code in codeBlock:
                            self.thinkCodeShowList.append(CodeShow(code, lexerName=lexerNameList[index], maxWidth=textMaxWidth))
                            thinkTempTextList = thinkTempText.split('```' + lexerNameList[index] + '\n' + code + '\n' + '```')
                            thinkSplitTextList.append(thinkTempTextList[0])
                            thinkTempText = thinkTempTextList[1] """
                """ print('thinkCodeBlocks:', thinkCodeBlocks) """
                for CodeBlock in thinkCodeBlocks:
                    language, code = CodeBlock
                    self.thinkCodeShowList.append(CodeShow(code.strip(), lexerName=language, maxWidth=textMaxWidth - self.imageLabel.width() - 80, parent=self))
                    """ self.thinkCodeShowList[-1].hide() """
                    self.thinkCodeShowList[-1].connectCodeCopyButtonClick(copyFun)
                    thinkTempTextList = thinkTempText.split('```' + language + '\n' + code + '```', maxsplit=1)
                    thinkSplitTextList.append(thinkTempTextList[0])
                    thinkTempText = thinkTempTextList[1]
                """ if thinkTempText != '': """
                thinkSplitTextList.append(thinkTempText)
                """ print('thinkSplitTextList:', thinkSplitTextList) """
                #ThinkingButton
                self.thinkButton = ThinkingButton()
                self.thinkButton.connectButtonClick(self.thinkButtonClicked)
                self.thinkButtonHaveCreated = True
                #textLayout
                self.textLayout.addWidget(self.thinkButton)
                #ThinkWidget
                for splitText in thinkSplitTextList:
                    if splitText != '':
                        self.thinkTextShowList.append(ThinkWidget(splitText, maxWidth=textMaxWidth - self.imageLabel.width() - 80, parent=self))
                    """ print('init len:', splitText[-10:], len(self.thinkTextShowList), len(self.thinkCodeShowList), len(self.resultTextShowList), len(self.resultCodeShowList)) """
                j = 0
                for i in range(len(self.thinkCodeShowList)):
                    if thinkSplitTextList[i] != '':
                        self.thinkBackVLayout.addWidget(self.thinkTextShowList[i - j])
                    else:
                        j += 1
                    self.thinkBackVLayout.addWidget(self.thinkCodeShowList[i])
                    """ #set visible
                    self.thinkCodeShowList[i].setVisible(self.thinkIsExpand) """
                """ if 0 < len(self.thinkTextShowList) - 1 - j and thinkSplitTextList[-1] != '': """
                if thinkSplitTextList[-1] != '':
                    self.thinkBackVLayout.addWidget(self.thinkTextShowList[-1])
                self.textLayout.addWidget(self.thinkBackWidget)
                #set visible
                self.thinkBackWidget.setVisible(self.thinkIsExpand)
                """ for thinkWidget in self.thinkTextShowList:
                    thinkWidget.setVisible(self.thinkIsExpand)
                for codeShow in self.thinkCodeShowList:
                    codeShow.setVisible(self.thinkIsExpand) """
                #
                if self.thinkTextIsRecvEnd and self.isRecvFirst:
                    """ self.thinkTextRecvEnd.emit() """
                    self.thinkButton.setThinkEnd()
                    self.isRecvFirst = False
                """ for i in range(self.textLayout.count()):
                    print('init subwidget:', i, self.textLayout.itemAt(i).widget()) """
            #TextShow
            resultSplitTextList = []
            resultTempTextList = []
            resultTempText = self.resultText
            if self.resultText != '':
                resultCodeBlocks = self.extract_code_blocks(self.resultText)
                for CodeBlock in resultCodeBlocks:
                    language, code = CodeBlock
                    self.resultCodeShowList.append(CodeShow(code.strip(), lexerName=language, maxWidth=textMaxWidth - self.imageLabel.width() - 35, parent=self))
                    """ self.resultCodeShowList[-1].hide() """
                    self.resultCodeShowList[-1].connectCodeCopyButtonClick(copyFun)
                    resultTempTextList = resultTempText.split('```' + language + '\n' + code + '```', maxsplit=1)
                    resultSplitTextList.append(resultTempTextList[0])
                    resultTempText = resultTempTextList[1]
                resultSplitTextList.append(resultTempText)
                #TextShow
                for splitText in resultSplitTextList:
                    if splitText != '':
                        self.resultTextShowList.append(TextShow(splitText, isUser=self.isUser, maxWidth=textMaxWidth - self.imageLabel.width() - 35, parent=self))
                #textLayout
                j = 0
                for i in range(len(self.resultCodeShowList)):
                    if resultSplitTextList[i] != '':
                        self.textLayout.addWidget(self.resultTextShowList[i - j])
                    else:
                        j += 1
                    self.textLayout.addWidget(self.resultCodeShowList[i])
                    """ self.resultCodeShowList[i].show() """
                """ if 0 < len(self.resultTextShowList) - 1 - j and resultSplitTextList[-1] != '': """
                if resultSplitTextList[-1] != '':
                    self.textLayout.addWidget(self.resultTextShowList[-1])
                """ for i in range(self.textLayout.count()):
                    print('init subwidget1:', i, self.textLayout.itemAt(i).widget()) """
            self.textLayout.setContentsMargins(15, 5, 15, 5)
            """ #TextShow
            for splitText in splitTextList:
                if splitText != '':
                    self.textShowList.append(TextShow(splitText, isUser=self.isUser, maxWidth=textMaxWidth))
            self.textShow = TextShow(self.resultText, isUser=self.isUser, maxWidth=textMaxWidth)
            #ThinkingButton
            self.thinkButton = ThinkingButton()
            self.thinkButton.connectButtonClick(self.thinkButtonClicked)
            #ThinkWidget
            self.thinkWidget = ThinkWidget(self.thinkText, maxWidth=textMaxWidth)
            #textLayout
            self.textLayout.addWidget(self.thinkButton)
            self.textLayout.addWidget(self.thinkWidget)
            #set visible
            self.thinkIsExpand = thinkIsExpand
            self.thinkWidget.setVisible(self.thinkIsExpand)
            #
            self.thinkTextRecvEnd.connect(self.thinkToggleWidget)
            if self.thinkTextIsRecvEnd and self.isRecvFirst:
                self.thinkTextRecvEnd.emit()
                self.isRecvFirst = False """
        else:
            #TextShow
            self.textShow = TextShow(text, isUser=self.isUser, maxWidth=textMaxWidth - self.imageLabel.width() - 15)
            self.textLayout.addWidget(self.textShow)
            self.textLayout.setContentsMargins(5, 0, 5, 0)
        """ if self.isUser:
            self.textLayout.addWidget(self.textShow)
            self.textLayout.setContentsMargins(5, 5, 5, 5)
        else:
            for i in range(len(self.codeShowList)):
                if splitTextList[i] != '':
                    self.textLayout.addWidget(self.textShowList[i])
                self.textLayout.addWidget(self.codeShowList[i])
            if splitTextList[-1] != '':
                self.textLayout.addWidget(self.textShowList[-1])
            self.textLayout.setContentsMargins(5, 5, 5, 5) """
        #loadingWidgetIsRemove
        self.loadingWidgetIsRemove = True
        #renewResponseButtonIsRemove
        self.renewResponseButtonIsRemove = True
        #subVLayout QVBoxLayout
        self.subVLayout1 = QVBoxLayout()
        self.subVLayout1.setAlignment(Qt.AlignTop)
        self.subVLayout1.setContentsMargins(0, 0, 0, 0)
        self.subVLayout2 = QVBoxLayout()
        self.subVLayout2.setAlignment(Qt.AlignTop)
        self.subVLayout2.setContentsMargins(0, 0, 0, 0)
        #CopyButton
        self.copyButton = CopyButton(tipText='复制', tipOffsetX=15, tipOffsetY=35, parent=self)
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
        self.renewResponseButton = PushButton(tipText='重新生成响应', tipOffsetX=25, tipOffsetY=35)
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
            """ self.textLayout.addWidget(self.funWidget)
            self.textLayout.setSpacing(0) """
            self.textWidget.setFixedSize(self.textShow.width() + 10, self.textShow.height())
            self.textBoxLayout.addWidget(self.textWidget)
            self.textBoxLayout.addWidget(self.funWidget)
            self.textBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.textBoxLayout.setSpacing(0)
            self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
            self.subVLayout1.addWidget(self.textBoxWidget)
            self.subVLayout2.addWidget(self.imageLabel)
        else:
            self.subVLayout1.addWidget(self.imageLabel)
            thinkBackWidth = max([textShow.width() for textShow in self.thinkTextShowList] + [codeShow.width() for codeShow in self.thinkCodeShowList], default=0) + 45
            thinkBackHeight = sum([textShow.height() for textShow in self.thinkTextShowList] + [codeShow.height() for codeShow in self.thinkCodeShowList])
            self.thinkBackWidget.setFixedSize(thinkBackWidth, thinkBackHeight)
            self.textLayout.setSpacing(0)
            if self.thinkIsExpand:
                if self.thinkText != '':
                    thinkWidth = max([self.thinkButton.width()] + [self.thinkBackWidget.width()])
                    thinkHeight = sum([self.thinkButton.height()] + [self.thinkBackWidget.height()])
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width(), self.thinkWidget.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + self.thinkWidget.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.thinkWidget.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.thinkWidget.height() + self.textShow.height() + 10) """
            else:
                if self.thinkText != '':
                    thinkWidth = self.thinkButton.width()
                    thinkHeight = self.thinkButton.height()
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.textShow.height() + 10) """
            self.textWidget.setFixedSize(max(thinkWidth, resultWidth) + 30, thinkHeight + resultHeight + 10)
            self.loadingWidget = LoadingWidget()
            """ self.textLayout.addWidget(self.loadingWidget)
            self.textLayout.setSpacing(0) """
            self.textBoxLayout.addWidget(self.textWidget)
            self.textBoxLayout.addWidget(self.loadingWidget)
            self.textBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.textBoxLayout.setSpacing(0)
            self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.loadingWidget.width()), self.textWidget.height() + self.loadingWidget.height())
            """ if self.thinkIsExpand:
                self.textWidget.setFixedSize(max(self.thinkButton.width(), self.thinkWidget.width(), self.textShow.width(), self.loadingWidget.width()), self.thinkButton.height() + self.thinkWidget.height() + self.textShow.height() + self.loadingWidget.height())
            else:
                self.textWidget.setFixedSize(max(self.thinkButton.width(), self.textShow.width(), self.loadingWidget.width()), self.thinkButton.height() + self.textShow.height() + self.loadingWidget.height()) """
            self.subVLayout2.addWidget(self.textBoxWidget)
            #loadingWidgetIsRemove
            self.loadingWidgetIsRemove = False
        #mainHLayout QHBoxLayout
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        #mainHLayout add subVLayout
        self.mainHLayout.addLayout(self.subVLayout1)
        self.mainHLayout.addLayout(self.subVLayout2)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.setSpacing(5)
        #main widget set size
        self.setFixedSize(self.imageLabel.width() + self.textBoxWidget.width() + 5, max(self.imageLabel.height(), self.textBoxWidget.height()))

    """ def extract_code_blocks(text):
        code_blocks = []
        # 正则表达式匹配代码块
        cPattern = r"```c\n(.*?)\n```"
        cppPattern = r"```cpp\n(.*?)\n```"
        pythonPattern = r"```python\n(.*?)\n```"
        javaPattern = r"```java\n(.*?)\n```"
        javascriptPattern = r"```javascript\n(.*?)\n```" 
        # re.DOTALL 表示让 . 匹配换行符
        code_blocks.append(re.findall(cPattern, text, re.DOTALL))
        code_blocks.append(re.findall(cppPattern, text, re.DOTALL))
        code_blocks.append(re.findall(pythonPattern, text, re.DOTALL))
        code_blocks.append(re.findall(javaPattern, text, re.DOTALL))
        code_blocks.append(re.findall(javascriptPattern, text, re.DOTALL))
        return code_blocks """
    def extract_code_blocks(self, text):
        # 定义正则表达式模式，匹配代码块
        pattern = r"```(\w+)\n(.*?)```"
        # 使用 re.DOTALL 让 . 匹配换行符
        matches = re.findall(pattern, text, re.DOTALL)
        # 过滤出指定语言的代码块
        supported_languages = {"cpp", "python", "glsl", "lua"}
        code_blocks = []
        for language, code in matches:
            if language.lower() in supported_languages:
                code_blocks.append([language, code])
        return code_blocks

    def getThinkIsExpanded(self):
        if not self.isUser:
            return self.thinkIsExpand
        else:
            return

    def thinkButtonClicked(self):
        self.thinkIsExpand = not self.thinkIsExpand
        #set visible
        """ for thinkWidget in self.thinkTextShowList:
            thinkWidget.setVisible(self.thinkIsExpand)
        for codeShow in self.thinkCodeShowList:
            codeShow.setVisible(self.thinkIsExpand) """
        self.thinkBackWidget.setVisible(self.thinkIsExpand)
        """ #setSize
        self.setSize() """
        self.resizeFinished.emit()

    """ def thinkToggleWidget(self):
        print('thinkToggleWidget') """

    def connectSetTexting(self, fun):
        self.setTexting.connect(fun)

    def toggleWidget(self):
        """ print('toggleWidget') """
        if self.isUser:
            self.textShow.setSizeFinished.connect(self.onSizeFinshed)
            self.textShow.toggleWidget()
        else:
            for thinkWidget in self.thinkTextShowList:
                thinkWidget.setSizeFinished.connect(self.onSizeFinshed)
                thinkWidget.toggleWidget()
            for textShow in self.resultTextShowList:
                textShow.setSizeFinished.connect(self.onSizeFinshed)
                textShow.toggleWidget()

    """ def connectSetSizeFinished(self, fun):
        for textShow in self.resultTextShowList:
            textShow.setSizeFinished.connect(fun) """

    def connectResizeFinished(self, fun):
        self.resizeFinished.connect(fun)

    def onSizeFinshed(self):
        """ print('sizeFinish:', self.thinkWidgetSizeFinshedCount, self.textShowSizeFinshedCount, len(self.thinkTextShowList), len(self.resultTextShowList)) """
        if self.isUser:
            self.resizeFinished.emit()
        else:
            if isinstance(self.sender(), ThinkWidget):
                self.thinkWidgetSizeFinshedCount += 1
                if self.thinkWidgetSizeFinshedCount == len(self.thinkTextShowList):
                    self.thinkWidgetSizeFinshedCount = 0
                    """ self.setSize() """
                    if self.thinkWidgetSizeFinshedCount == 0 and self.textShowSizeFinshedCount == 0:
                        """ print('ThinkWidget sizeFinish:', self.thinkWidgetSizeFinshedCount, self.textShowSizeFinshedCount) """
                        self.resizeFinished.emit()
                        self.setTexting.emit(False)
            else:
                self.textShowSizeFinshedCount += 1
                if self.textShowSizeFinshedCount == len(self.resultTextShowList):
                    self.textShowSizeFinshedCount = 0
                    """ self.setSize() """
                    if self.thinkWidgetSizeFinshedCount == 0 and self.textShowSizeFinshedCount == 0:
                        """ print('TextShow sizeFinish:', self.thinkWidgetSizeFinshedCount, self.textShowSizeFinshedCount) """
                        self.resizeFinished.emit()
                        self.setTexting.emit(False)

    def setSize(self):
        if self.isUser:
            self.textWidget.setFixedSize(self.textShow.width() + 10, self.textShow.height())
            self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
        else:
            thinkBackWidth = max([textShow.width() for textShow in self.thinkTextShowList] + [codeShow.width() for codeShow in self.thinkCodeShowList], default=0) + 45
            thinkBackHeight = sum([textShow.height() for textShow in self.thinkTextShowList] + [codeShow.height() for codeShow in self.thinkCodeShowList])
            self.thinkBackWidget.setFixedSize(thinkBackWidth, thinkBackHeight)
            if self.thinkIsExpand:
                if self.thinkText != '':
                    thinkWidth = max([self.thinkButton.width()] + [self.thinkBackWidget.width()])
                    thinkHeight = sum([self.thinkButton.height()] + [self.thinkBackWidget.height()])
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width(), self.thinkWidget.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + self.thinkWidget.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.thinkWidget.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.thinkWidget.height() + self.textShow.height() + 10) """
            else:
                if self.thinkText != '':
                    thinkWidth = self.thinkButton.width()
                    thinkHeight = self.thinkButton.height()
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.textShow.height() + 10) """
            self.textWidget.setFixedSize(max(thinkWidth, resultWidth) + 30, thinkHeight + resultHeight + 10)
            if self.loadingWidgetIsRemove:
                self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
            else:
                self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.loadingWidget.width()), self.textWidget.height() + self.loadingWidget.height())
        self.setFixedSize(self.imageLabel.width() + self.textBoxWidget.width() + 5, max(self.imageLabel.height(), self.textBoxWidget.height()))

    def setText(self, text):
        self.text = text

        if not self.isUser:
            """ if len(self.resultTextShowList) > 0:
                print('result think[0] size:', self.thinkTextShowList[0].size())
            if len(self.thinkTextShowList) > 0:
                print('think think[0] size:', self.thinkTextShowList[0].size()) """
            """ print('setText len:', self.thinkTextShowList, len(self.thinkTextShowList), len(self.thinkCodeShowList), len(self.resultTextShowList), len(self.resultCodeShowList))
            for i in range(self.textLayout.count()):
                print('subwidget:', i, self.textLayout.itemAt(i).widget()) """
            self.setTexting.emit(True)
            #
            self.thinkText = ''
            self.resultText = ''
            if '<think>' in self.text:
                textList = self.text.split('<think>')
                tempText = textList[1]
                if '</think>' in tempText:
                    textList2 = tempText.split('</think>')
                    self.thinkText = textList2[0]
                    self.resultText = self.text.split('<think>' + self.thinkText + '</think>')[1]
                    self.thinkTextIsRecvEnd = True
                else:
                    self.thinkText = tempText
            elif not (self.text in '<think>' or self.text == ''):
                self.resultText = self.text
                self.thinkTextIsRecvEnd = True
            #ThinkWidget
            thinkSplitTextList = []
            thinkTempTextList = []
            thinkTempText = self.thinkText
            if self.thinkText != '':
                thinkCodeBlocks = self.extract_code_blocks(self.thinkText)
                thinkCodeShowListLastLen = len(self.thinkCodeShowList) - 1
                for index, CodeBlock in enumerate(thinkCodeBlocks):
                    language, code = CodeBlock
                    if thinkCodeShowListLastLen < index:
                        self.thinkCodeShowList.append(CodeShow(code.strip(), lexerName=language, maxWidth=self.textMaxWidth - self.imageLabel.width() - 80, parent=self))
                        #set visible
                        self.thinkCodeShowList[-1].setVisible(self.thinkIsExpand)
                        """ self.thinkCodeShowList[-1].hide() """
                        #connect codeCopyButton Click
                        self.thinkCodeShowList[-1].connectCodeCopyButtonClick(self.copyFun)
                    else:
                        self.thinkCodeShowList[index].setText(code.strip(), lexerName=language)
                    thinkTempTextList = thinkTempText.split('```' + language + '\n' + code + '```', maxsplit=1)
                    thinkSplitTextList.append(thinkTempTextList[0])
                    thinkTempText = thinkTempTextList[1]
                thinkSplitTextList.append(thinkTempText)
                """ print('split:', len(thinkSplitTextList)) """
                if not self.thinkButtonHaveCreated:
                    #ThinkingButton
                    self.thinkButton = ThinkingButton()
                    self.thinkButton.connectButtonClick(self.thinkButtonClicked)
                    self.thinkButtonHaveCreated = True
                    #textLayout
                    self.textLayout.addWidget(self.thinkButton)
                    self.textLayout.addWidget(self.thinkBackWidget)
                    #set visible
                    self.thinkBackWidget.setVisible(self.thinkIsExpand)
                #ThinkWidget
                i = 0
                thinkTextShowListLastLen = len(self.thinkTextShowList) - 1
                for splitText in thinkSplitTextList:
                    if splitText != '':
                        if thinkTextShowListLastLen < i:
                            self.thinkTextShowList.append(ThinkWidget(splitText, maxWidth=self.textMaxWidth - self.imageLabel.width() - 80, parent=self))
                            #set visible
                            self.thinkTextShowList[-1].setVisible(self.thinkIsExpand)
                        else:
                            """ print('i:', i, splitText[-10:]) """
                            """ if self.isRecvFirst:
                                self.thinkTextShowList[i].setText(splitText) """
                            self.thinkTextShowList[i].setText(splitText)
                        i += 1
                #textLayout
                j = 0
                for i in range(len(self.thinkCodeShowList)):
                    if thinkSplitTextList[i] != '':
                        if thinkTextShowListLastLen < i - j:
                            self.thinkBackVLayout.addWidget(self.thinkTextShowList[i - j])
                    else:
                        j += 1
                    if thinkCodeShowListLastLen < i:
                        self.thinkBackVLayout.addWidget(self.thinkCodeShowList[i])
                        """ #set visible
                        self.thinkCodeShowList[i].setVisible(self.thinkIsExpand) """
                if thinkTextShowListLastLen < len(self.thinkTextShowList) - 1 - j and thinkSplitTextList[-1] != '':
                    self.thinkBackVLayout.addWidget(self.thinkTextShowList[-1])
                """ #set text
                if not self.thinkTextIsRecvEnd:
                    self.thinkWidget.setText(self.thinkText) """
                #
                """ print('thinkTextIsRecvEnd:', self.thinkTextIsRecvEnd) """
                if self.thinkTextIsRecvEnd and self.isRecvFirst:
                    """ print('isRecvFirst:', self.isRecvFirst)
                    self.thinkTextRecvEnd.emit() """
                    self.thinkButton.setThinkEnd()
                    self.isRecvFirst = False
            #TextShow
            resultSplitTextList = []
            resultTempTextList = []
            resultTempText = self.resultText
            if self.resultText != '':
                resultCodeBlocks = self.extract_code_blocks(self.resultText)
                resultCodeShowListLastLen = len(self.resultCodeShowList) - 1
                for index, CodeBlock in enumerate(resultCodeBlocks):
                    language, code = CodeBlock
                    if resultCodeShowListLastLen < index:
                        self.resultCodeShowList.append(CodeShow(code.strip(), lexerName=language, maxWidth=self.textMaxWidth - self.imageLabel.width() - 35, parent=self))
                        """ self.resultCodeShowList[-1].hide() """
                        #connect codeCopyButton Click
                        self.resultCodeShowList[-1].connectCodeCopyButtonClick(self.copyFun)
                    else:
                        self.resultCodeShowList[index].setText(code.strip(), lexerName=language)
                    resultTempTextList = resultTempText.split('```' + language + '\n' + code + '```', maxsplit=1)
                    resultSplitTextList.append(resultTempTextList[0])
                    resultTempText = resultTempTextList[1]
                resultSplitTextList.append(resultTempText)
                #TextShow
                i = 0
                resultTextShowListLastLen = len(self.resultTextShowList) - 1
                for splitText in resultSplitTextList:
                    if splitText != '':
                        if resultTextShowListLastLen < i:
                            self.resultTextShowList.append(TextShow(splitText, isUser=self.isUser, maxWidth=self.textMaxWidth - self.imageLabel.width() - 35, parent=self))
                        else:
                            self.resultTextShowList[i].setText(splitText)
                        i += 1
                #textLayout
                j = 0
                for i in range(len(self.resultCodeShowList)):
                    if resultSplitTextList[i] != '':
                        if resultTextShowListLastLen < i - j:
                            self.textLayout.addWidget(self.resultTextShowList[i - j])
                    else:
                        j += 1
                    if resultCodeShowListLastLen < i:
                        self.textLayout.addWidget(self.resultCodeShowList[i])
                        """ self.resultCodeShowList[i].show() """
                if resultTextShowListLastLen < len(self.resultTextShowList) - 1 - j and resultSplitTextList[-1] != '':
                    self.textLayout.addWidget(self.resultTextShowList[-1])
                """ self.textShow.setText(self.resultText) """
        else:
            self.textShow.setText(text)

        if self.isUser:
            self.textWidget.setFixedSize(self.textShow.width() + 10, self.textShow.height())
            self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
        else:
            thinkBackWidth = max([textShow.width() for textShow in self.thinkTextShowList] + [codeShow.width() for codeShow in self.thinkCodeShowList], default=0) + 45
            thinkBackHeight = sum([textShow.height() for textShow in self.thinkTextShowList] + [codeShow.height() for codeShow in self.thinkCodeShowList])
            self.thinkBackWidget.setFixedSize(thinkBackWidth, thinkBackHeight)
            if self.thinkIsExpand:
                if self.thinkText != '':
                    thinkWidth = max([self.thinkButton.width()] + [self.thinkBackWidget.width()])
                    thinkHeight = sum([self.thinkButton.height()] + [self.thinkBackWidget.height()])
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    """ print('width list:', [textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList]) """
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width(), self.thinkWidget.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + self.thinkWidget.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.thinkWidget.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.thinkWidget.height() + self.textShow.height() + 10) """
            else:
                if self.thinkText != '':
                    thinkWidth = self.thinkButton.width()
                    thinkHeight = self.thinkButton.height()
                else:
                    thinkWidth = 0
                    thinkHeight = 0
                if self.resultText != '':
                    resultWidth = max([textShow.width() for textShow in self.resultTextShowList] + [codeShow.width() for codeShow in self.resultCodeShowList])
                    resultHeight = sum([textShow.height() for textShow in self.resultTextShowList] + [codeShow.height() for codeShow in self.resultCodeShowList])
                else:
                    resultWidth = 0
                    resultHeight = 0
                """ textShowWidths = [textShow.width() for textShow in self.textShowList]
                allWidths = [self.thinkButton.width()] + textShowWidths
                textShowHeights = sum([textShow.height() for textShow in self.textShowList])
                codeShowHeights = sum([codeShow.height() for codeShow in self.codeShowList]) """
                """ self.textWidget.setFixedSize(max(allWidths) + 10, self.thinkButton.height() + textShowHeights + codeShowHeights + 10) """
                """ self.textWidget.setFixedSize(max(self.thinkButton.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.textShow.height() + 10) """
            """ print('textWidget:', thinkWidth, thinkHeight, resultWidth, resultHeight) """
            self.textWidget.setFixedSize(max(thinkWidth, resultWidth) + 30, thinkHeight + resultHeight + 10)
            """ print('thinkWidth resultWidth textWidget:', thinkWidth, resultWidth, self.textWidget.width()) """
            """ print(self.textWidget.size()) """
            if self.loadingWidgetIsRemove:
                self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
            else:
                self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.loadingWidget.width()), self.textWidget.height() + self.loadingWidget.height())
        self.setFixedSize(self.imageLabel.width() + self.textBoxWidget.width() + 5, max(self.imageLabel.height(), self.textBoxWidget.height()))

    def getText(self):
        return self.text

    def getIsUser(self):
        return self.isUser

    """ def getTextShow(self):
        return self.textShow """

    def getTextWidget(self):
        return self.textWidget

    def getTextBoxWidget(self):
        return self.textBoxWidget

    """ def getCopyButton(self):
        return self.copyButton """

    def removeLoadingWidget(self):
        if not self.isUser and not self.loadingWidgetIsRemove:
            self.textBoxLayout.removeWidget(self.loadingWidget)
            self.loadingWidget.deleteLater()
            self.loadingWidgetIsRemove = True
            self.textBoxLayout.addWidget(self.funWidget)
            self.textBoxLayout.setSpacing(0)
            """ if self.thinkIsExpand:
                self.textWidget.setFixedSize(max(self.thinkButton.width(), self.thinkWidget.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.thinkWidget.height() + self.textShow.height() + 10)
            else:
                self.textWidget.setFixedSize(max(self.thinkButton.width(), self.textShow.width()) + 10, self.thinkButton.height() + self.textShow.height() + 10) """
            self.textBoxWidget.setFixedSize(max(self.textWidget.width(), self.funWidget.width()), self.textWidget.height() + self.funWidget.height())
            self.setFixedSize(self.imageLabel.width() + self.textBoxWidget.width() + 5, max(self.imageLabel.height(), self.textBoxWidget.height()))

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
        if self.isUser:
            if self.textShow.hasSelectedText():
                return True
            else:
                return False
        else:
            for thinkWidget in self.thinkTextShowList:
                if thinkWidget.hasSelectedText():
                    return True
            for codeShow in self.thinkCodeShowList:
                if codeShow.hasSelectedText():
                    return True
            for textShow in self.resultTextShowList:
                if textShow.hasSelectedText():
                    return True
            for codeShow in self.resultCodeShowList:
                if codeShow.hasSelectedText():
                    return True
            return False

    def getSelectedText(self):
        if self.isUser:
            if self.textShow.hasSelectedText():
                return self.textShow.getSelectedText()
            else:
                return ''
        else:
            for thinkWidget in self.thinkTextShowList:
                if thinkWidget.hasSelectedText():
                    return thinkWidget.getSelectedText()
            for codeShow in self.thinkCodeShowList:
                if codeShow.hasSelectedText():
                    return codeShow.getSelectedText()
            for textShow in self.resultTextShowList:
                if textShow.hasSelectedText():
                    return textShow.getSelectedText()
            for codeShow in self.resultCodeShowList:
                if codeShow.hasSelectedText():
                    return codeShow.getSelectedText()
            return ''

    """ def showColorful(self):
        self.textShow.isColorful = True
        self.textShow.repaint()

    def showDefaultColor(self):
        self.textShow.isColorful = False
        self.textShow.repaint() """

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
        self.font.setPointSize(windowFontPointSize)
        self.font.setBold(True)
        self.label.setFont(self.font)
        self.font_metrics = QFontMetricsF(self.font)
        self.palette = self.label.palette()
        self.palette.setColor(QPalette.WindowText, QColor(76, 106, 246))
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
            self.label.resize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(self.label.width() + 10, self.label.height() + 10)
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
            self.label.resize(int(self.font_metrics.height()), int(self.font_metrics.height()))
            self.setFixedSize(self.label.width() + 10, self.label.height() + 10)

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
        self.font.setPointSize(windowFontPointSize)
        """ self.font.setBold(True) """
        self.setFont(self.font)
        """ self.palette = self.palette()
        self.palette.setColor(QPalette.WindowText, QColor(23, 171, 227))
        self.setPalette(self.palette) """

class SettingEdit(QLineEdit):
    def __init__(self, parent=None):
        super(SettingEdit, self).__init__(parent)
        self.setFixedHeight(32)
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, windowFontPointSize)
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
            border: 2px solid;
            border-radius: 8px;
            background: transparent;
            font: {windowFontPointSize}pt;
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
            border: 2px solid;
            border-radius: 8px;
            background: transparent;
            font: {windowFontPointSize}pt;
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
            background-color: rgb(50, 50, 50);
        }
        QSlider::handle:hover:horizontal{
            background-color: rgb(70, 70, 70);
        }
        QSlider::sub-page:horizontal{
            border-radius: 4px;
            background-color: rgb(90, 90, 90);
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
                self.font = QFont(font_family, windowFontPointSize)
                self.setFont(self.font)
        #searchButton QPushButton
        self.searchButton = PushButton(tipText='搜索', tipOffsetX=5, tipOffsetY=35, parent=self)
        self.searchButton.setFixedSize(30, 30)
        self.search_images_path = os.path.join(images_dir, 'search.png').replace('\\', '/')
        self.searchButton.setIcon(QIcon(f"{self.search_images_path}"))
        self.searchButton.setIconSize(QSize(24, 24))
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
            padding-left: 30px;
        }
        ''')

    def connectSearchButtonClick(self, fun):
        self.searchButton.clicked.connect(fun)

class ChatRecordsWidget(QWidget):
    def __init__(self, parent=None):
        super(ChatRecordsWidget, self).__init__(parent)
        self.resize(1200 // 3, 760)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        font_id = QFontDatabase.addApplicationFont(font_file_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                self.font = QFont(font_family, windowFontPointSize)
        #settingButton PushButton
        self.settingButton = PushButton(tipText='设置', tipOffsetX=5, tipOffsetY=35)
        self.settingButton.setFixedSize(44, 44)
        self.setting_images_path = os.path.join(images_dir, 'setting.png').replace('\\', '/')
        """ self.setting_hover_images_path = os.path.join(images_dir, 'setting_hover.png').replace('\\', '/') """
        self.settingButton.setIcon(QIcon(f"{self.setting_images_path}"))
        self.settingButton.setIconSize(QSize(30, 30))
        self.settingButton.setStyleSheet('''
        QPushButton{
            border: none;
            border-radius: 22px;
        }
        QPushButton:hover{
            background: #b0b0b0;
        }
        ''')
        #buttonWidget QWidget
        self.buttonWidget = Widget()
        self.buttonWidget.resize(44, 50)
        self.buttonWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #buttonVLayout QVBoxLayout
        self.buttonVLayout = QVBoxLayout()
        self.buttonWidget.setLayout(self.buttonVLayout)
        self.buttonVLayout.addWidget(self.settingButton)
        self.buttonVLayout.setAlignment(Qt.AlignTop)
        self.buttonVLayout.setContentsMargins(0, 0, 0, 6)
        #QLabel
        self.label = QLabel()
        self.label.resize(self.width() - self.buttonWidget.width() - 40, 50)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        font = QFont()
        font.setPointSize(titleFontPointSize)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setText("聊天历史")
        self.label.setAlignment(Qt.AlignLeft)
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
        self.clearAllButton = PushButton(tipText='删除所有记录', tipOffsetX=25, tipOffsetY=35)
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
        self.mainWidget.resize(1200 // 3, 760)
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
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 16, 16)
        path.addRect(self.rect().x(), self.rect().y(), 16, 16)
        path.addRect(self.rect().width() - 16, self.rect().y(), 16, 16)
        path.addRect(self.rect().width() - 16, self.rect().height() - 16, 16, 16)
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
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height(), 16, 16)
        path.addRect(self.rect().x(), self.rect().y(), 16, 16)
        path.addRect(self.rect().width() - 16, self.rect().y(), 16, 16)
        path.addRect(self.rect().width() - 16, self.rect().height() - 16, 16, 16)
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
        """ self.chatShow.itemClicked.connect(self.itemShowColorful) """
        #chatShowWidget QWidget
        self.chatShowWidget = Widget()
        self.chatShowWidget.setMinimumHeight(244)
        self.chatShowWidget.resize(1200, 500)
        self.chatShowWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #chatShowVLayout QVBoxLayout
        self.chatShowVLayout = QVBoxLayout()
        self.chatShowWidget.setLayout(self.chatShowVLayout)
        self.chatShowVLayout.addWidget(self.chatShow)
        self.chatShowVLayout.setContentsMargins(20, 4, 10, 16)
        #TextEditFull
        self.chatInput = TextEditFull()
        self.chatInput.connectSendButtonClick(self.sendMessage)
        #chatInputWidget QWidget
        self.chatInputWidget = Widget()
        self.chatInputWidget.setMinimumHeight(100)
        self.chatInputWidget.resize(1200, 200)
        self.chatInputWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #chatInputVLayout QVBoxLayout
        self.chatInputVLayout = QVBoxLayout()
        self.chatInputWidget.setLayout(self.chatInputVLayout)
        self.chatInputVLayout.addWidget(self.chatInput)
        self.chatInputVLayout.setContentsMargins(20, 0, 20, 20)
        #QSplitter
        self.splitter = Splitter(Qt.Vertical)
        self.splitter.resize(1200, 700)
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
        self.chatRecordsFoldButton = PushButton(tipText='折叠', tipOffsetX=5, tipOffsetY=35, parent=self.mainWidget)
        self.chatRecordsFoldButton.setFixedSize(30, 50)
        self.chatRecordsFoldButton.setIconSize(QSize(30, 50))
        self.chatRecordsFoldButton.setStyleSheet(f'''
        QPushButton{{
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            background: #d0d0d0;
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
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() + 10)
        self.emptyTextLabel.raise_()
        self.emptyTextLabel.hide()
        #textCopyLabel PrintLabel
        self.textCopyLabel = PrintLabel('文本复制成功', self)
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() + 10)
        self.textCopyLabel.raise_()
        self.textCopyLabel.hide()
        """ #resizeTimer
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.messageWidgetRegenerate) """
        #isRegenerate
        self.isRegenerate = False
        self.isRegenerateFirst = True
        #isSetTexting
        self.isSetTexting = False
        #pushButtonIsPress
        self.pushButtonIsPress = False
        """ #messageWidgetIsSelect
        self.messageWidgetIsSelect = False
        #selectMessageWidgetNumber
        self.selectMessageWidgetNumber = -1 """
        #settingIsTop
        self.settingIsTop = False
        #chatRecordsIsTop
        self.chatRecordsIsTop = False
        #screen
        self.lastScreen = self.curScreen = self.screen()
        self.dpi = 0.0
        self.screenChanged = False
        #thinkExpandedList
        self.thinkExpandedList = []
        """ #messageIsRenewResponse
        self.messageIsRenewResponse = False """
        #isSending
        self.isSending = False
        #isContinueShow
        self.isContinueShow = True
        """ #isScreenMax
        self.isScreenMax = False
        #lastNormalGeometry
        self.lastNormalGeometry = self.geometry() """

    def moveEvent(self, event):
        #screen
        self.curScreen = self.screen()
        if self.lastScreen != self.curScreen:
            self.lastScreen = self.curScreen
            self.screenChanged = True
        QMainWindow.moveEvent(self, event)

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
        elif isinstance(widget, TextBoxWidget):
            for i in range(0, len(self.messageWidgetList)):
                messageWidget = self.messageWidgetList[i]
                if widget == messageWidget.getTextBoxWidget():
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
                """ if self.settingWidgetIsOpen:
                    chatShowRect = QRect(self.chatShow.geometry().x() + self.settingWidget.width(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                elif self.chatRecordsWidgetIsOpen:
                    chatShowRect = QRect(self.chatShow.geometry().x() + self.chatRecordsWidget.width(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                else:
                    chatShowRect = QRect(self.chatShow.geometry().x(), self.chatShow.geometry().y() + self.titleWidget.height() + self.chatFun.height(), self.chatShow.geometry().width(), self.chatShow.geometry().height())
                if not chatShowRect.contains(event.pos()):
                    self.messageWidgetIsSelect = False
                    self.selectMessageWidgetNumber = -1
                else:
                    widget = self.childAt(event.pos())
                    if isinstance(widget, CopyButton):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            if widget == messageWidget.getCopyButton():
                                self.messageWidgetIsSelect = True
                                self.selectMessageWidgetNumber = i
                                messageWidget.showColorful()
                    elif isinstance(widget.parent(), WebEngineView):
                        for i in range(0, len(self.messageWidgetList)):
                            messageWidget = self.messageWidgetList[i]
                            if widget.parent() == messageWidget.getTextShow().getWebEngineView():
                                self.messageWidgetIsSelect = True
                                self.selectMessageWidgetNumber = i
                                messageWidget.showColorful() """
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
            if self.screenChanged:
                self.dpi = self.curScreen.logicalDotsPerInch()
                global bubbleFontPixelSize
                bubbleFontPixelSize = math.ceil(bubbleFontPointSize * (self.dpi / 72))
                """ print('mouseReleaseEvent bubbleFontPixelSize:', bubbleFontPixelSize) """
                self.screenChanged = False
            if self.isRegenerate:
                self.isRegenerate = False
                self.messageWidgetRegenerate()
        QMainWindow.mouseReleaseEvent(self, event)

    """ def itemShowColorful(self, item):
        self.messageWidgetList[self.chatShow.row(item)].showColorful()
        self.messageWidgetIsSelect = True
        self.selectMessageWidgetNumber = self.chatShow.row(item) """

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
            self.settingFoldButton.move(self.settingWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)
        else:
            self.settingWidget.move(-self.settingWidget.width(), self.titleWidget.height())
            self.settingFoldButton.move(0, (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)
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
            self.chatRecordsFoldButton.move(self.chatRecordsWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)
        else:
            self.chatRecordsWidget.move(-self.chatRecordsWidget.width(), self.titleWidget.height())
            self.chatRecordsFoldButton.move(0, (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)
        #TextEditFull adjust size
        self.chatInput.resetWidgetSize()
        #move emptyTextLabel
        self.emptyTextLabel.move((self.width() - self.emptyTextLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() + 10)
        #move textCopyLabel
        self.textCopyLabel.move((self.width() - self.textCopyLabel.width()) // 2, self.titleWidget.height() + self.chatFun.height() + self.chatShowWidget.height() + 10)
        """ #resizeTimer
        self.resizeTimer.start(150) """
        #isRegenerate
        self.isRegenerate = True
        if self.isRegenerateFirst:
            self.isRegenerateFirst = False
            self.isRegenerate = False

    def titleWidgetInit(self):
        #titleIconLabel QLabel
        self.titleIconLabel = QLabel()
        self.titleIconLabel.setFixedSize(40, 30)
        self.titleIconLabel.setScaledContents(True)
        self.ai_assistant_images_path = os.path.join(images_dir, 'ai_assistant.png').replace('\\', '/')
        self.titleIconLabel.setPixmap(QPixmap(f'{self.ai_assistant_images_path}'))
        #titleLeftSubWidget QWidget
        self.titleLeftSubWidget = Widget()
        self.titleLeftSubWidget.resize(self.titleIconLabel.width() + 15, self.titleIconLabel.height() + 10)
        self.titleLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleLeftSubHLayout QHBoxLayout
        self.titleLeftSubHLayout = QHBoxLayout()
        self.titleLeftSubWidget.setLayout(self.titleLeftSubHLayout)
        self.titleLeftSubHLayout.addWidget(self.titleIconLabel)
        """ self.titleLeftSubHLayout.addWidget(self.titleTextLabel) """
        self.titleLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.titleLeftSubHLayout.setContentsMargins(10, 5, 5, 5)
        """ self.titleLeftSubHLayout.setSpacing(5) """
        #minButton PushButton
        self.minButton = PushButton(tipText='', tipOffsetX=10, tipOffsetY=35)
        self.minButton.setFixedSize(50, 40)
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
        self.maxButton = PushButton(tipText='', tipOffsetX=10, tipOffsetY=35)
        self.maxButton.setFixedSize(50, 40)
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
        self.closeButton = PushButton(tipText='', tipOffsetX=5, tipOffsetY=35)
        self.closeButton.setFixedSize(50, 40)
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
        self.titleRightSubWidget.resize(150, 40)
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
        self.titleWidget.resize(1200, 40)
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
        """ if self.isScreenMax: """
        if self.isMaximized():
            self.showNormal()
            """ self.setGeometry(self.lastNormalGeometry) """
            self.maxButton.setIcon(QIcon(f"{self.max_images_path}"))
            """ self.isScreenMax = False """
        else:
            self.showMaximized()
            """ self.lastNormalGeometry = self.geometry()
            self.setGeometry(-10, -10, self.screen().size().width() + 20, self.screen().size().height() + 20) """
            self.maxButton.setIcon(QIcon(f"{self.normal_images_path}"))
            """ self.isScreenMax = True """

    def UiClose(self):
        self.saveCurChatRecord(withholdCurChatFile=True)
        self.close()

    def settingWidgetInit(self):
        #setting config file
        try:
            if not os.path.exists(config_file_path):
                with open(config_file_path, "w", encoding='utf-8') as f:
                    global init_base_url, init_api_key, init_model, init_maxTokens_currentVal, init_topP_currentVal, init_temperature_currentVal
                    f.write(init_base_url + '\n' + init_api_key + '\n' + init_model + '\n' + str(init_maxTokens_currentVal) + '\n' + str(init_topP_currentVal) + '\n' + str(init_temperature_currentVal) + '\n')
            with open(config_file_path, "r", encoding='utf-8') as f:
                content = f.readlines()
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
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
        self.settingFoldButton = PushButton(tipText='折叠', tipOffsetX=5, tipOffsetY=35, parent=self.mainWidget)
        self.settingFoldButton.setFixedSize(30, 50)
        self.settingFoldButton.setIconSize(QSize(30, 50))
        self.fold_images_path = os.path.join(images_dir, 'fold.png').replace('\\', '/')
        self.fold_hover_images_path = os.path.join(images_dir, 'fold_hover.png').replace('\\', '/')
        self.settingFoldButton.setStyleSheet(f'''
        QPushButton{{
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            background: #d0d0d0;
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
            """ if not self.chatRecordsWidgetIsOpen:
                self.settingWidget.raise_()
                self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
                self.settingAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
                self.settingAnimationMove.start()
                self.settingWidgetIsOpen = True
                self.settingIsTop = True
            else: """
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
            """ if self.settingIsTop:
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
            else: """
            self.settingWidget.raise_()
            self.settingFoldButton.raise_()
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
        """ #resizeTimer
        self.resizeTimer.start(150) """

    def settingUiMoveFinished(self):
        if not self.settingWidgetIsOpen:
            self.settingFoldButton.hide()
        if self.sender() == self.settingAnimationMove:
            self.messageWidgetRegenerate()

    def settingUiAnimationMove2(self, rect):
        self.settingFoldButton.move(rect.x() + self.settingWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.settingFoldButton.height()) // 2)

    def settingFoldButtonClicked(self):
        if not self.chatRecordsWidgetIsOpen:
            print('settingFoldButtonClicked, not chatRecordsWidgetIsOpen')
            self.settingAnimationMove.setStartValue(self.settingWidget.geometry())
            self.settingAnimationMove.setEndValue(QRect(-self.settingWidget.width(), self.titleWidget.height(), self.settingWidget.width(), self.settingWidget.height()))
            self.settingAnimationMove.start()
            self.settingWidgetIsOpen = False
            self.settingIsTop = False
        else:
            print('settingFoldButtonClicked, chatRecordsWidgetIsOpen')
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
        """ #resizeTimer
        self.resizeTimer.start(150) """

    def chatRecordsUiMoveFinished(self):
        if not self.chatRecordsWidgetIsOpen:
            self.chatRecordsFoldButton.hide()
            #delete all item
            self.chatRecordsWidget.delAllListItems()
        if self.sender() == self.chatRecordsAnimationMove:
            self.messageWidgetRegenerate()

    def chatRecordsUiAnimationMove2(self, rect):
        self.chatRecordsFoldButton.move(rect.x() + self.chatRecordsWidget.width(), (self.mainWidget.height() + self.titleWidget.height() - self.chatRecordsFoldButton.height()) // 2)

    def chatRecordsFoldButtonClicked(self):
        if not self.settingWidgetIsOpen:
            print('chatRecordsFoldButtonClicked, not settingWidgetIsOpen')
            self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
            self.chatRecordsAnimationMove.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
            self.chatRecordsAnimationMove.start()
            self.chatRecordsWidgetIsOpen = False
            self.chatRecordsIsTop = False
        else:
            print('chatRecordsFoldButtonClicked, settingWidgetIsOpen')
            self.chatRecordsAnimationMove2.setStartValue(self.chatRecordsWidget.geometry())
            self.chatRecordsAnimationMove2.setEndValue(QRect(-self.chatRecordsWidget.width(), self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
            self.chatRecordsAnimationMove2.start()
            self.chatRecordsWidgetIsOpen = False
            self.chatRecordsIsTop = False
            self.settingIsTop = True

    def baseUrlTextChanged(self, text):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[0] = text + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")

    def apiKeyTextChanged(self, text):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[1] = text + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")

    def modelNameTextChanged(self, text):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[2] = text + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")

    def maxTokensBoxValueChanged(self, i):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[3] = str(i) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        self.maxTokensSlider.setValue(i)

    def topPBoxValueChanged(self, d):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[4] = str(d) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        self.topPSlider.setValue(int(d * 100))

    def temperatureBoxValueChanged(self, d):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[5] = str(d) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        self.temperatureSlider.setValue(int((d - 0.01) * 100))

    def maxTokensSliderValueChanged(self, i):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[3] = str(i) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        self.maxTokensBox.setValue(i)

    def topPSliderValueChanged(self, i):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[4] = str(i / 100) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        self.topPBox.setValue(i / 100)

    def temperatureSliderValueChanged(self, i):
        try:
            with open(config_file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines[5] = str(i / 100 + 0.01) + '\n'
            with open(config_file_path, "w", encoding='utf-8') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f"错误：文件 {config_file_path} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
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
        """ #judge status of sendButton
        if not self.chatInput.sendButtonIsEnable():
            return """
        if not self.isSending:
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
                self.messageSendWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=True, textMaxWidth=self.chatShow.width() * 3 // 4)
                """ self.messageSendWidget.connectSetSizeFinished(self.messageWidgetResize) """
                self.messageSendWidget.connectResizeFinished(self.messageWidgetResize)
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
                """ #disable sendButton
                self.chatInput.disableSendButton() """
                #clear text of TextEditFull
                self.chatInput.clearText()
                self.chatInput.textEdit.isSending = True
                self.chatInput.textEdit.textChanged.emit()
                self.isSending = True
            else:
                #print emptyTextLabel
                self.emptyTextLabel.printStart()
        else:
            self.thread.stop()
            self.isSending = False
        """ self.isSending = not self.isSending """

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
        self.messageRecvWidget = MessageWidget(self.Message, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=False, textMaxWidth=self.chatShow.width() * 3 // 4)
        """ self.messageRecvWidget.connectSetSizeFinished(self.messageWidgetResize) """
        self.messageRecvWidget.connectResizeFinished(self.messageWidgetResize)
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
        """ #messageIsRenewResponse
        if self.messageIsRenewResponse:
            self.messageWidgetIsSelect = True
            self.selectMessageWidgetNumber += 1
            self.messageWidgetList[self.selectMessageWidgetNumber].showColorful()
            self.messageIsRenewResponse = False """

    def recvMessage(self, text):
        if self.first:
            self.first = False
            text = text.strip("\n ")
        self.Message += text
        if self.isContinueShow:
            #messageWidget set text
            self.messageRecvWidget.setText(self.Message)
            #chatShow itemWidget adjust size
            self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
            self.itemRecvHLayout.setContentsMargins(0, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width(), 5)
            #chatShow item adjust size
            self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))

    def messageFinish(self):
        self.chatInput.textEdit.isSending = False
        self.chatInput.textEdit.textChanged.emit()
        #messageRecvWidget
        self.messageRecvWidget.removeLoadingWidget()
        self.messageRecvWidget.toggleWidget()
        #chatShow itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(0, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width(), 5)
        #chatShow item adjust size
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))
        """ #enable sendButton
        self.chatInput.enableSendButton() """
        #message renew response if message is empty
        if self.Message == '':
            del self.messageWidgetList[-1]
            last = self.chatShow.count() - 1
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(last))
            itemWidget.deleteLater()
            lastItem = self.chatShow.takeItem(last)
            del lastItem
            self.messageRenewResponse()
        self.isSending = False

    def textCopy(self):
        #print textCopyLabel
        self.textCopyLabel.printStart()
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def messageRenewResponse(self):
        i = len(self.messageWidgetList) - 1
        j = 0
        context = []
        while i >= j:
            if self.messageWidgetList[i - j].getIsUser():
                for k in range(0, i - j):
                    messageWidget = self.messageWidgetList[k]
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
                #create thread
                self.thread = messageThread(self.messageWidgetList[i - j].getText(), context=context)
                self.thread.started.connect(self.messageStart)
                self.thread.newMessage.connect(self.recvMessage)
                self.thread.finished.connect(self.messageFinish)
                self.thread.start()
                """ #disable sendButton
                self.chatInput.disableSendButton() """
                """ self.messageIsRenewResponse = True """
                break
            else:
                j += 1
        #pushButtonIsPress
        self.pushButtonIsPress = True

    def writeToChatRecordFile(self, withholdCurChatFile=False):
        #chatRecordFileName QString
        self.chatRecordFileName = "chat_"
        self.chatRecordFileName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
        self.chatRecordFileName += ".txt"
        #write to chatRecord file
        try:
            with open(os.path.join(chat_records_dir, self.chatRecordFileName), 'a', encoding='utf-8') as f:
                for i in range(0, self.chatShow.count()):
                    chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                    f.write(chatRecordStr)
        except FileNotFoundError:
            print(f"错误：文件 {os.path.join(chat_records_dir, self.chatRecordFileName)} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
        if not withholdCurChatFile:
            #assign chatRecord fileName to curChatFile
            self.curChatFile = self.chatRecordFileName

    def saveCurChatRecord(self, withholdCurChatFile=False):
        #init
        chatRecordStr = ''
        chatStrCount = 0
        #judge whether messageWidgetList is empty
        if len(self.messageWidgetList) != 0:
            #judge whether curChatFile is empty
            if self.curChatFile == '':
                self.writeToChatRecordFile(withholdCurChatFile)
            else:
                if not os.path.exists(os.path.join(chat_records_dir, self.curChatFile)):
                    self.writeToChatRecordFile(withholdCurChatFile)
                else:
                    try:
                        for i in range(0, len(self.messageWidgetList)):
                            chatStrCount += self.messageWidgetList[i].getText().count('\n') + 2
                        #read curChat file
                        with open(os.path.join(chat_records_dir, self.curChatFile), 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        if chatStrCount > len(lines):
                            #clear curChat file
                            with open(os.path.join(chat_records_dir, self.curChatFile), 'w', encoding='utf-8') as f:
                                f.truncate()
                            #write to curChat file
                            with open(os.path.join(chat_records_dir, self.curChatFile), 'a', encoding='utf-8') as f:
                                for i in range(0, self.chatShow.count()):
                                    chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                                    f.write(chatRecordStr)
                    except FileNotFoundError:
                        print(f"错误：文件 {os.path.join(chat_records_dir, self.curChatFile)} 不存在")
                    except Exception as e:
                        print(f"发生未知错误：{e}")

    def chatRecordsGenerateItem(self, searchText=''):
        #generate item
        for fileName in os.listdir(os.path.join(os.getcwd(), chat_records_dir)):
            if fileName.endswith(".txt"):
                if searchText == '':
                    try:
                        with open(os.path.join(chat_records_dir, fileName), 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                    except FileNotFoundError:
                        print(f"错误：文件 {os.path.join(chat_records_dir, fileName)} 不存在")
                    except Exception as e:
                        print(f"发生未知错误：{e}")
                    #create item
                    chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                    item = self.chatRecordsWidget.addListItem(chatRecordStr)
                    #item set data
                    self.chatRecordsWidget.listItemSetData(item, fileName)
                else:
                    try:
                        with open(os.path.join(chat_records_dir, fileName), 'r', encoding='utf-8') as f:
                            content = f.read()
                        if searchText in content:
                            with open(os.path.join(chat_records_dir, fileName), 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            #create item
                            chatRecordStr = lines[0] + lines[len(lines) - 2].strip('\n')
                            item = self.chatRecordsWidget.addListItem(chatRecordStr)
                            #item set data
                            self.chatRecordsWidget.listItemSetData(item, fileName)
                    except FileNotFoundError:
                        print(f"错误：文件 {os.path.join(chat_records_dir, fileName)} 不存在")
                    except Exception as e:
                        print(f"发生未知错误：{e}")

    def generateCurChatRecord(self, lastIsToggle=True, useThinkExpandList=False):
        #init
        text = ''
        isUser = True
        if useThinkExpandList:
            expandIndex = 0
        #read curChat file
        try:
            with open(os.path.join(chat_records_dir, self.curChatFile), 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"错误：文件 {os.path.join(chat_records_dir, self.curChatFile)} 不存在")
        except Exception as e:
            print(f"发生未知错误：{e}")
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
                if useThinkExpandList:
                    if not isUser:
                        self.messageWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=isUser, thinkIsExpand=self.thinkExpandedList[expandIndex], textMaxWidth=self.chatShow.width() * 3 // 4)
                    else:
                        self.messageWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=isUser, textMaxWidth=self.chatShow.width() * 3 // 4)
                else:
                    self.messageWidget = MessageWidget(text, self.textCopy, self.messageRenewResponse, self.chatShow, isUser=isUser, thinkIsExpand=False, textMaxWidth=self.chatShow.width() * 3 // 4)
                """ self.messageWidget.connectSetSizeFinished(self.messageWidgetResize) """
                self.messageWidget.connectResizeFinished(self.messageWidgetResize)
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
                if useThinkExpandList and not isUser:
                    #expandIndex
                    expandIndex += 1
            else:
                text += lines[i]

    def getSetTexting(self, state):
        self.isSetTexting = state
        return self.isSetTexting

    def messageWidgetRegenerate(self):
        if len(self.messageWidgetList) != 0:
            self.thinkExpandedList = []
            if self.isSetTexting:
                self.isContinueShow = False
            if not self.isSetTexting:
                self.current_scroll_value = self.chatShow.verticalScrollBar().value()
                self.max_scroll_value = self.chatShow.verticalScrollBar().maximum()
            self.saveCurChatRecord()
            for i in range(0, len(self.messageWidgetList)):
                messageWidget = self.messageWidgetList[i]
                if not messageWidget.getIsUser():
                    self.thinkExpandedList.append(messageWidget.getThinkIsExpanded())
            self.messageWidgetList.clear()
            for i in range(0, self.chatShow.count()):
                itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
                itemWidget.deleteLater()
            self.chatShow.clear()
            if not self.isSetTexting:
                self.generateCurChatRecord(useThinkExpandList=True)
                QTimer.singleShot(5, self.setScrollValue)
            else:
                self.generateCurChatRecord(lastIsToggle=False, useThinkExpandList=True)
                self.messageRecvWidget = self.messageWidget
                self.itemRecvHLayout = self.itemHLayout
                self.itemRecvWidget = self.itemWidget
                self.recvItem = self.item
                self.isContinueShow = True
            """ if self.messageWidgetIsSelect:
                self.messageWidgetList[self.selectMessageWidgetNumber].showColorful() """

    def setScrollValue(self):
        new_max_scroll_value = self.chatShow.verticalScrollBar().maximum()
        if self.max_scroll_value != 0:
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
                self.chatRecordsFoldButton.raise_()
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
            font = QFont(font_family, windowFontPointSize)
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
