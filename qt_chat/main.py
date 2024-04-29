# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:31:44 2024

@author: YXD
"""

import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QEvent
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QKeyEvent
from openai import OpenAI

base_url = "https://7613907zg6.vicp.fun/v1"
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
        response = client.chat.completions.create(
            model="chatglm3-6b",
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
        return

class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.resize(994, 130)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setPlaceholderText("按Shift+Enter换行、按Enter提交")
        self.sendButton = QPushButton()
        self.sendButton.setFixedSize(40, 40)
        self.sendButton.setCursor(Qt.PointingHandCursor)
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
            border: 2px solid rgb(23, 146, 230);
            border-radius: 10px;
            image: url("send_disable.png");
        }
        ''')
        self.setStyleSheet('''
        QTextEdit{
            border: none;
            background :transparent;
            font-size: 20px;
            selection-background-color: rgb(150, 10, 250);
        }
        QScrollBar{
            width: 25px;
        }
        ''')

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

    def getSendButtonIsEnable(self):
        return self.sendButton.isEnabled()

    def sendButtonShow(self):
        if self.toPlainText() == '':
            self.sendButton.setStyleSheet('''
            QPushButton{
                border: none;
                image: url("send.png");
            }
            QPushButton:disabled{
                border: 2px solid rgb(23, 146, 230);
                border-radius: 10px;
                image: url("send_disable.png");
            }
            ''')
        else:
            self.sendButton.setStyleSheet('''
            QPushButton{
                border: 2px solid rgb(150, 10, 250);
                border-radius: 10px;
                image: url("send_hover.png");
            }
            QPushButton:disabled{
                border: 2px solid rgb(23, 146, 230);
                border-radius: 10px;
                image: url("send_disable.png");
            }
            ''')

class TextWidget(QWidget):
    def __init__(self, parent=None):
        super(TextWidget, self).__init__(parent)
        self.textEdit = TextEdit()
        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName("TextBorderWidget")
        self.mainHLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainHLayout)
        self.mainHLayout.addWidget(self.textEdit)
        self.mainHLayout.setContentsMargins(5, 5, 5, 5)
        self.mainWidget.resize(self.textEdit.width() + 10, self.textEdit.height() + 10)
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.resize(self.mainWidget.size())
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setStyleSheet('''
        QWidget#TextBorderWidget{
            border: 2px solid rgb(150, 10, 250);
            border-radius: 10px;
        }
        ''')

    def resetWidgetSize(self):
        self.textEdit.resize(self.width() - 10, self.height() - 10)
        self.mainWidget.resize(self.width(), self.height())

    def toPlainText(self):
        return self.textEdit.toPlainText()

    def clear(self):
        self.textEdit.clear()

    def connectButtonClick(self, fun):
        self.textEdit.connectSendButtonClick(fun)

    def enableButton(self):
        self.textEdit.enableSendButton()

    def disableButton(self):
        self.textEdit.disableSendButton()

    def getButtonIsEnable(self):
        return self.textEdit.getSendButtonIsEnable()

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.resize(974, 440)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        ''')

class ImageLabel(QLabel):
    def __init__(self, isUser=True, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setFixedSize(36, 36)
        if isUser:
            self.setPixmap(QPixmap("user.png"))
        else:
            self.setPixmap(QPixmap("ai.png"))

class TextLabel(QWidget):
    def __init__(self, text, isUser=True, maxWidth=650, parent=None):
        super(TextLabel, self).__init__(parent)
        self.text = text.strip('\n')
        self.label = QLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setWordWrap(True)
        self.maxWidth = maxWidth
        self.label.setMaximumWidth(self.maxWidth)
        self.font = QFont()
        self.font.setPixelSize(20)
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
                labelHeight = (count + 1) * (textHeight + 7) - 1
            else:
                for i in range(0, count + 1):
                    if i != count:
                        tempTextWidth = self.font_metrics.width(textList[i] + ' ')
                        tempTextWidth = math.ceil(tempTextWidth / (self.maxWidth - 24)) * (self.maxWidth - 24)
                    else:
                        tempTextWidth = self.font_metrics.width(textList[i])
                    textWidth += int(tempTextWidth)
                labelWidth = self.maxWidth
                labelHeight = int(math.ceil(textWidth / (self.maxWidth - 24)) * (textHeight + 7) - 1)
            self.label.setText(self.text)
            self.label.setFixedSize(labelWidth, labelHeight)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(labelWidth + 10, labelHeight + 10)
        else:
            self.label.setFixedSize(26, 26)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(36, 36)
        self.isUser = isUser

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
        #add rect and set brush
        if self.isUser:
            path.addRect(self.rect().width() - 15, self.rect().y(), 15, 15)
            brush.setColor(QColor(10, 160, 10))
        else:
            path.addRect(self.rect().x(), self.rect().y(), 15, 15)
            brush.setColor(QColor(150, 150, 200))
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
                labelHeight = (count + 1) * (textHeight + 7) - 1
            else:
                for i in range(0, count + 1):
                    if i != count:
                        tempTextWidth = self.font_metrics.width(textList[i] + ' ')
                        tempTextWidth = math.ceil(tempTextWidth / (self.maxWidth - 24)) * (self.maxWidth - 24)
                    else:
                        tempTextWidth = self.font_metrics.width(textList[i])
                    textWidth += int(tempTextWidth)
                labelWidth = self.maxWidth
                labelHeight = int(math.ceil(textWidth / (self.maxWidth - 24)) * (textHeight + 7) - 1)
            self.label.setText(self.text)
            self.label.setFixedSize(labelWidth, labelHeight)
            self.setFixedSize(labelWidth + 10, labelHeight + 10)
        else:
            self.label.setFixedSize(26, 26)
            self.setFixedSize(36, 36)

    def setMaxWidth(self, maxWidth):
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
                labelHeight = (count + 1) * (textHeight + 7) - 1
            else:
                for i in range(0, count + 1):
                    if i != count:
                        tempTextWidth = self.font_metrics.width(textList[i] + ' ')
                        tempTextWidth = math.ceil(tempTextWidth / (self.maxWidth - 24)) * (self.maxWidth - 24)
                    else:
                        tempTextWidth = self.font_metrics.width(textList[i])
                    textWidth += int(tempTextWidth)
                labelWidth = self.maxWidth
                labelHeight = int(math.ceil(textWidth / (self.maxWidth - 24)) * (textHeight + 7) - 1)
            self.label.setText(self.text)
            self.label.setFixedSize(labelWidth, labelHeight)
            self.setFixedSize(labelWidth + 10, labelHeight + 10)
        else:
            self.label.setFixedSize(26, 26)
            self.setFixedSize(36, 36)

class MessageWidget(QWidget):
    def __init__(self, text, isUser=True, textMaxWidth=650, parent=None):
        super(MessageWidget, self).__init__(parent)
        self.isUser = isUser
        #ImageLabel
        self.imageLabel = ImageLabel(isUser=self.isUser)
        #TextLabel
        self.textLabel = TextLabel(text, isUser=self.isUser, maxWidth=textMaxWidth)
        #LoadingLabel
        self.loadingLabel = LoadingLabel()
        #LoadingLabel flag
        self.loadingLabelIsRemove = True
        #textWidget QWidget
        self.textWidget = QWidget()
        #textLayout QHBoxLayout
        self.textLayout = QVBoxLayout()
        self.textLayout.addWidget(self.textLabel)
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        self.textWidget.setLayout(self.textLayout)
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
        #add imageLabel and textLabel
        if self.isUser:
            #self.subVLayout1.addWidget(self.textLabel)
            #self.subVLayout2.addWidget(self.imageLabel)
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
            self.subVLayout1.addWidget(self.textWidget)
            self.subVLayout2.addWidget(self.imageLabel)
        else:
            #self.subVLayout1.addWidget(self.imageLabel)
            #self.subVLayout2.addWidget(self.textLabel)
            self.subVLayout1.addWidget(self.imageLabel)
            self.textLayout.addWidget(self.loadingLabel)
            self.textLayout.setSpacing(0)
            self.textWidget.setFixedSize(self.textLabel.width() if self.textLabel.width() > self.loadingLabel.width() else self.loadingLabel.width(), self.textLabel.height() + self.loadingLabel.height())
            self.subVLayout2.addWidget(self.textWidget)
            #LoadingLabel flag
            self.loadingLabelIsRemove = False
        #mainHLayout add subVLayout
        self.mainHLayout.addLayout(self.subVLayout1)
        self.mainHLayout.addLayout(self.subVLayout2)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.setSpacing(5)
        #main widget set size
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def setText(self, text):
        self.textLabel.setText(text)
        if self.isUser:
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
        elif not self.loadingLabelIsRemove:
            self.textWidget.setFixedSize(self.textLabel.width() if self.textLabel.width() > self.loadingLabel.width() else self.loadingLabel.width(), self.textLabel.height() + self.loadingLabel.height())
        else:
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def getIsUser(self):
        return self.isUser

    def setTextMaxWidth(self, textMaxWidth):
        self.textLabel.setMaxWidth(textMaxWidth)
        if self.isUser:
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
        elif not self.loadingLabelIsRemove:
            self.textWidget.setFixedSize(self.textLabel.width() if self.textLabel.width() > self.loadingLabel.width() else self.loadingLabel.width(), self.textLabel.height() + self.loadingLabel.height())
        else:
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def removeLoadingLabel(self):
        self.textLayout.removeWidget(self.loadingLabel)
        self.loadingLabel.hide()
        self.loadingLabelIsRemove = True
        self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
        self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

class LoadingLabel(QWidget):
    def __init__(self, parent=None):
        super(LoadingLabel, self).__init__(parent)
        self.subWidget1 = QWidget()
        self.subWidget2 = QWidget()
        self.subWidget3 = QWidget()
        self.subWidgetList = []
        self.subWidgetList.append(self.subWidget1)
        self.subWidgetList.append(self.subWidget2)
        self.subWidgetList.append(self.subWidget3)
        self.mainHLayout = QHBoxLayout()
        for subWidget in self.subWidgetList:
            subWidget.setFixedSize(18, 18)
            self.mainHLayout.addWidget(subWidget)
        self.mainHLayout.setContentsMargins(8, 8, 8, 8)
        self.mainHLayout.setSpacing(8)
        self.setLayout(self.mainHLayout)
        self.setFixedSize(86, 34)
        #QTimer
        self.loadingTimer = QTimer()
        self.loadingTimer.timeout.connect(self.loadingShow)
        self.loadingTimer.start(500)
        self.loadingNum = 0

    def loadingShow(self):
        for subWidget in self.subWidgetList:
            subWidget.setFixedSize(18, 18)
            subWidget.setStyleSheet('''
                border: none;
                border-radius: 9px;
                background-color: rgb(150, 150, 150);
            ''')
        self.subWidgetList[self.loadingNum].setStyleSheet('''
            border: none;
            border-radius: 9px;
            background-color: rgb(80, 80, 80);
        ''')
        self.loadingNum = (self.loadingNum + 1) % 3

class PrintLabel(QWidget):
    def __init__(self, parent=None):
        super(PrintLabel, self).__init__(parent)
        self.label = QLabel()
        self.font = QFont()
        self.font.setPixelSize(20)
        self.font.setBold(True)
        self.label.setFont(self.font)
        self.palette = self.label.palette()
        self.palette.setColor(QPalette.WindowText, QColor(150, 10, 250))
        self.label.setPalette(self.palette)
        self.label.setText("文本不能为空")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.adjustSize()
        self.mainHLayout = QHBoxLayout()
        self.mainHLayout.addWidget(self.label)
        self.mainHLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.mainHLayout)
        self.setFixedSize(self.label.width() + 10, self.label.height() + 10)

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

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        self.setFixedSize(40, 40)
        self.setIcon(QIcon("right_arrow.png"))
        self.setIconSize(QSize(40, 40))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('''
        QPushButton{
            border: none;
        }
        ''')

class Label(QLabel):
    def __init__(self, parent=None):
        super(Label, self).__init__(parent)
        self.font = QFont()
        self.font.setBold(True)
        self.setFont(self.font)
        self.palette = self.palette()
        self.palette.setColor(QPalette.WindowText, QColor(150, 10, 250))
        self.setPalette(self.palette)

class SpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(SpinBox, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setStyleSheet('''
        QSpinBox{
            border: 2px solid rgb(150, 10, 250);
            border-radius: 8px;
            background: transparent;
            font: bold;
            color: rgb(150, 10, 250);
            selection-background-color: rgb(150, 10, 250);
        }
        QSpinBox::up-button{
            width: 12px;
            height: 12px;
            border-image: url("up_arrow.png");
        }
        QSpinBox::up-button:pressed{
            margin-top: 1px;
        }
        QSpinBox::down-button{
            width: 12px;
            height: 12px;
            border-image: url("down_arrow.png");
        }
        QSpinBox::down-button:pressed{
            margin-bottom: 1px;
        }
        ''')

    def enterEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def leaveEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setStyleSheet('''
        QDoubleSpinBox{
            border: 2px solid rgb(150, 10, 250);
            border-radius: 8px;
            background: transparent;
            font: bold;
            color: rgb(150, 10, 250);
            selection-background-color: rgb(150, 10, 250);
        }
        QDoubleSpinBox::up-button{
            width: 12px;
            height: 12px;
            border-image: url("up_arrow.png");
        }
        QDoubleSpinBox::up-button:pressed{
            margin-top: 1px;
        }
        QDoubleSpinBox::down-button{
            width: 12px;
            height: 12px;
            border-image: url("down_arrow.png");
        }
        QDoubleSpinBox::down-button:pressed{
            margin-bottom: 1px;
        }
        ''')

    def enterEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def leaveEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

class Slider(QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.resize(221, 30)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setStyleSheet('''
        QSlider::groove:horizontal{
            height: 6px;
            border-radius: 3px;
            background-color: rgb(150, 150, 150);
        }
        QSlider::handle:horizontal{
            width: 20px;
            margin: -7px 0px -7px 0px;
            border-radius: 10px;
            background-color: rgb(80, 80, 80);
        }
        QSlider::sub-page:horizontal{
            border-radius: 3px;
            background-color: rgb(150, 10, 250);
        }
        ''')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        #messageListItem QSpacerItem
        self.messageListSpacerItem = QSpacerItem(self.width() - 50, 10, hPolicy=QSizePolicy.Expanding, vPolicy=QSizePolicy.Fixed)
        #ListWidget
        self.messageList = ListWidget()
        #messageListWidget QWidget
        self.messageListWidget = QWidget()
        self.messageListWidget.resize(974, 450)
        self.messageListWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #messageListVLayout QVBoxLayout
        self.messageListVLayout = QVBoxLayout()
        self.messageListWidget.setLayout(self.messageListVLayout)
        self.messageListVLayout.addSpacerItem(self.messageListSpacerItem)
        self.messageListVLayout.addWidget(self.messageList)
        self.messageListVLayout.setContentsMargins(0, 0, 0, 0)
        self.messageListVLayout.setSpacing(0)
        self.messageListVLayout.setStretch(0, 0)
        self.messageListVLayout.setStretch(1, 1)
        #setting QWidget init
        self.settingWidgetInit()
        #topWidget QWidget
        self.topWidget = QWidget()
        self.topWidget.resize(1024, 450)
        self.topWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #topHLayout QHBoxLayout
        self.topHLayout = QHBoxLayout()
        self.topWidget.setLayout(self.topHLayout)
        self.topHLayout.addWidget(self.settingWidget)
        self.topHLayout.addWidget(self.buttonWidget)
        self.topHLayout.addWidget(self.messageListWidget)
        self.topHLayout.setContentsMargins(0, 0, 10, 0)
        self.topHLayout.setSpacing(0)
        self.topHLayout.setStretch(0, 1)
        self.topHLayout.setStretch(1, 0)
        self.topHLayout.setStretch(2, 3)
        #TextWidget
        self.messageInput = TextWidget()
        self.messageInput.connectButtonClick(self.sendMessage)
        #bottomWidget QWidget
        self.bottomWidget = QWidget()
        self.bottomWidget.resize(1024, 150)
        self.bottomWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #bottomHLayout QHBoxLayout
        self.bottomHLayout = QHBoxLayout()
        self.bottomWidget.setLayout(self.bottomHLayout)
        self.bottomHLayout.addWidget(self.messageInput)
        self.bottomHLayout.setContentsMargins(10, 0, 10, 10)
        self.bottomHLayout.setStretch(0, 1)
        #mainWidget QWidget
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.resize(1024, 600)
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.topWidget)
        self.mainVLayout.addWidget(self.bottomWidget)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        self.mainVLayout.setStretch(0, 3)
        self.mainVLayout.setStretch(1, 1)
        #messageWidget list
        self.messageWidgetList = []
        #PrintLabel
        self.printLabel = PrintLabel(self)
        self.printLabel.move(int((self.width() - self.printLabel.width()) / 2), self.messageList.height() - self.printLabel.height())
        self.printLabel.raise_()
        self.printLabel.hide()
        #printTimer QTimer
        self.printTimer = QTimer(self)
        self.printTimer.timeout.connect(self.printEnd)

    def resizeEvent(self, event):
        #TextLabel max width
        textMaxWidth = int(self.messageList.width() * 2 / 3)
        for i in range(0, self.messageList.count()):
            #messageWidget set max width of textLabel
            self.messageWidgetList[i].setTextMaxWidth(textMaxWidth)
            messageWidget = self.messageWidgetList[i]
            #messageList itemWidget adjust size
            self.messageList.itemWidget(self.messageList.item(i)).setFixedSize(self.messageList.width(), messageWidget.height() + 10)
            itemWidget = self.messageList.itemWidget(self.messageList.item(i))
            if messageWidget.getIsUser():
                self.messageList.itemWidget(self.messageList.item(i)).layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 5, 5, 5, 5)
            else:
                self.messageList.itemWidget(self.messageList.item(i)).layout().setContentsMargins(5, 5, itemWidget.width() - messageWidget.width() - 5, 5)
            #messageList item adjust size
            self.messageList.item(i).setSizeHint(QSize(self.messageList.width(), messageWidget.height() + 10))
        #TextWidget adjust size
        self.messageInput.resetWidgetSize()
        #move printLabel
        self.printLabel.move(int((self.width() - self.printLabel.width()) / 2), self.messageList.height() - self.printLabel.height())

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
        self.maxTokensWidget.resize(241, 70)
        self.maxTokensWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting maxTokens sub-Widget
        self.maxTokensSubWidget = QWidget()
        self.maxTokensSubWidget.resize(221, 30)
        self.maxTokensSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting maxTokens QHBoxLayout
        self.maxTokensHLayout = QHBoxLayout()
        self.maxTokensSubWidget.setLayout(self.maxTokensHLayout)
        self.maxTokensHLayout.addWidget(self.maxTokensLabel)
        self.maxTokensHLayout.addWidget(self.maxTokensBox)
        self.maxTokensHLayout.setContentsMargins(0, 0, 0, 0)
        #setting maxTokens QVBoxLayout
        self.maxTokensVLayout = QVBoxLayout()
        self.maxTokensWidget.setLayout(self.maxTokensVLayout)
        self.maxTokensVLayout.addWidget(self.maxTokensSubWidget)
        self.maxTokensVLayout.addWidget(self.maxTokensSlider)
        self.maxTokensVLayout.setContentsMargins(10, 0, 10, 0)
        self.maxTokensHLayout.setSpacing(10)
        #setting topP QWidget
        self.topPWidget = QWidget()
        self.topPWidget.resize(241, 70)
        self.topPWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting topP sub-Widget
        self.topPSubWidget = QWidget()
        self.topPSubWidget.resize(221, 30)
        self.topPSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting topP QHBoxLayout
        self.topPHLayout = QHBoxLayout()
        self.topPSubWidget.setLayout(self.topPHLayout)
        self.topPHLayout.addWidget(self.topPLabel)
        self.topPHLayout.addWidget(self.topPBox)
        self.topPHLayout.setContentsMargins(0, 0, 0, 0)
        #setting topP QVBoxLayout
        self.topPVLayout = QVBoxLayout()
        self.topPWidget.setLayout(self.topPVLayout)
        self.topPVLayout.addWidget(self.topPSubWidget)
        self.topPVLayout.addWidget(self.topPSlider)
        self.topPVLayout.setContentsMargins(10, 0, 10, 0)
        self.topPHLayout.setSpacing(10)
        #setting temperature QWidget
        self.temperatureWidget = QWidget()
        self.temperatureWidget.resize(241, 70)
        self.temperatureWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting temperature sub-Widget
        self.temperatureSubWidget = QWidget()
        self.temperatureSubWidget.resize(221, 30)
        self.temperatureSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #setting temperature QHBoxLayout
        self.temperatureHLayout = QHBoxLayout()
        self.temperatureSubWidget.setLayout(self.temperatureHLayout)
        self.temperatureHLayout.addWidget(self.temperatureLabel)
        self.temperatureHLayout.addWidget(self.temperatureBox)
        self.temperatureHLayout.setContentsMargins(0, 0, 0, 0)
        #setting temperature QVBoxLayout
        self.temperatureVLayout = QVBoxLayout()
        self.temperatureWidget.setLayout(self.temperatureVLayout)
        self.temperatureVLayout.addWidget(self.temperatureSubWidget)
        self.temperatureVLayout.addWidget(self.temperatureSlider)
        self.temperatureVLayout.setContentsMargins(10, 0, 10, 0)
        self.temperatureVLayout.setSpacing(10)
        #setting QWidget
        self.settingWidget = QWidget()
        self.settingWidget.resize(int((self.messageList.width() - 10) / 4 + 10), self.messageListWidget.height())
        self.settingWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.settingWidget.hide()
        #setting QVBoxLayout
        self.settingVLayout = QVBoxLayout()
        self.settingWidget.setLayout(self.settingVLayout)
        self.settingVLayout.addWidget(self.maxTokensWidget)
        self.settingVLayout.addWidget(self.topPWidget)
        self.settingVLayout.addWidget(self.temperatureWidget)
        self.settingVLayout.setContentsMargins(10, 0, 0, 0)
        #PushButton
        self.settingButton = PushButton()
        self.settingButton.clicked.connect(self.settingButtonClicked)
        #buttonSpacerItem QSpacerItem
        self.buttonSpacerItem = QSpacerItem(40, self.messageListWidget.height() - 40, hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Expanding)
        #buttonWidget QWidget
        self.buttonWidget = QWidget()
        self.buttonWidget.resize(40, self.messageListWidget.height())
        self.buttonWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        #buttonVLayout QVBoxLayout
        self.buttonVLayout = QVBoxLayout()
        self.buttonWidget.setLayout(self.buttonVLayout)
        self.buttonVLayout.addWidget(self.settingButton)
        self.buttonVLayout.addSpacerItem(self.buttonSpacerItem)
        self.buttonVLayout.setContentsMargins(0, 0, 0, 0)
        #right
        self.buttonIconIsRight = True

    def settingButtonClicked(self):
        if self.buttonIconIsRight:
            self.settingButton.setIcon(QIcon("left_arrow.png"))
            self.settingWidget.show()
            self.buttonIconIsRight = False
        else:
            self.settingButton.setIcon(QIcon("right_arrow.png"))
            self.settingWidget.hide()
            self.messageList.resize(self.width() - 50, self.messageList.height())
            self.buttonIconIsRight = True
        #TextLabel max width
        textMaxWidth = int(self.messageList.width() * 2 / 3)
        for i in range(0, self.messageList.count()):
            #messageWidget set max width of textLabel
            self.messageWidgetList[i].setTextMaxWidth(textMaxWidth)
            messageWidget = self.messageWidgetList[i]
            #messageList itemWidget adjust size
            self.messageList.itemWidget(self.messageList.item(i)).setFixedSize(self.messageList.width(), messageWidget.height() + 10)
            itemWidget = self.messageList.itemWidget(self.messageList.item(i))
            if messageWidget.getIsUser():
                self.messageList.itemWidget(self.messageList.item(i)).layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 5, 5, 5, 5)
            else:
                self.messageList.itemWidget(self.messageList.item(i)).layout().setContentsMargins(5, 5, itemWidget.width() - messageWidget.width() - 5, 5)
            #messageList item adjust size
            self.messageList.item(i).setSizeHint(QSize(self.messageList.width(), messageWidget.height() + 10))

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

    def sendMessage(self):
        #judge status of sendButton
        if not self.messageInput.getButtonIsEnable():
            return
        #get text from TextWidget
        text = self.messageInput.toPlainText()
        if not text == '':
            #MessageWidget
            self.messageSendWidget = MessageWidget(text, isUser=True, textMaxWidth=int(self.messageList.width() * 2 / 3))
            self.messageWidgetList.append(self.messageSendWidget)
            #itemSendWidget QWidget
            self.itemSendWidget = QWidget(self)
            self.itemSendHLayout = QHBoxLayout()
            self.itemSendHLayout.addWidget(self.messageSendWidget)
            self.itemSendWidget.setLayout(self.itemSendHLayout)
            self.itemSendWidget.setFixedSize(self.messageList.width(), self.messageSendWidget.height() + 10)
            self.itemSendHLayout.setContentsMargins(self.itemSendWidget.width() - self.messageSendWidget.width() - 5, 5, 5, 5)
            #sendItem QListWidgetItem
            self.sendItem = QListWidgetItem(self.messageList)
            self.sendItem.setSizeHint(QSize(self.messageList.width(), self.messageSendWidget.height() + 10))
            self.messageList.setItemWidget(self.sendItem, self.itemSendWidget)
            self.messageList.setCurrentItem(self.sendItem)
            #create thread
            self.thread = messageThread(text)
            self.thread.started.connect(self.messageStart)
            self.thread.newMessage.connect(self.recvMessage)
            self.thread.finished.connect(self.messageFinish)
            self.thread.start()
            #disable sendButton
            self.messageInput.disableButton()
            #clear text of TextWidget
            self.messageInput.clear()
        else:
            #show printLabel
            self.printLabel.show()
            #start printTimer
            self.printTimer.start(2000)

    def messageStart(self):
        #message
        self.Message = ""
        #MessageWidget
        self.messageRecvWidget = MessageWidget(self.Message, isUser=False, textMaxWidth=int(self.messageList.width() * 2 / 3))
        self.messageWidgetList.append(self.messageRecvWidget)
        #itemRecvWidget QWidget
        self.itemRecvWidget = QWidget(self)
        self.itemRecvHLayout = QHBoxLayout()
        self.itemRecvHLayout.addWidget(self.messageRecvWidget)
        self.itemRecvWidget.setLayout(self.itemRecvHLayout)
        self.itemRecvWidget.setFixedSize(self.messageList.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
        #recvItem QListWidgetItem
        self.recvItem = QListWidgetItem(self.messageList)
        self.recvItem.setSizeHint(QSize(self.messageList.width(), self.messageRecvWidget.height() + 10))
        self.messageList.setItemWidget(self.recvItem, self.itemRecvWidget)
        self.messageList.setCurrentItem(self.recvItem)
        #first
        self.first = True

    def recvMessage(self, text):
        if self.first:
            self.first = False
            text = text.strip("\n ")
        self.Message += text
        #messageWidget set text of textLabel
        self.messageRecvWidget.setText(self.Message)
        #messageList itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.messageList.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
        #messageList item adjust size
        self.recvItem.setSizeHint(QSize(self.messageList.width(), self.messageRecvWidget.height() + 10))

    def messageFinish(self):
        #messageRecvWidget remove LoadingLabel
        self.messageRecvWidget.removeLoadingLabel()
        #messageList itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.messageList.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
        #messageList item adjust size
        self.recvItem.setSizeHint(QSize(self.messageList.width(), self.messageRecvWidget.height() + 10))
        #enable sendButton
        self.messageInput.enableButton()

    def printEnd(self):
        #hide printLabel
        self.printLabel.hide()
        #stop printTimer
        self.printTimer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
