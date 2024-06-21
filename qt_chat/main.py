# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:31:44 2024

@author: YXD
"""

import sys, os
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QDoubleSpinBox, QSlider, QSizePolicy, QSpacerItem, QAbstractSpinBox, QGridLayout, QLineEdit, qApp
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QSize, QTimer, QDateTime, QRect, QVariant, QAbstractAnimation, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QBrush, QFontMetricsF, QFont, QIcon, QPalette, QPixmap, QPen
from openai import OpenAI

#Import for test
import random, time

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
        self.contentOutput = "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦\n"
        if self.use_stream:
            #for i in range(0, len(self.contentOutput), 2):
                #self.newMessage.emit(self.contentOutput[i:i+2])
                #time.sleep(1)
            for k in range(0, 3):
                for i in range(0, len(self.contentOutput), 2):
                    self.newMessage.emit(self.contentOutput[i:i+2])
                    time.sleep(0.1)
        else:
            self.newMessage.emit(self.contentOutput)
        return

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.resize(974, 350)
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

    def mousePressEvent(self, event):
        QListWidget.mousePressEvent(self, event)
        event.ignore()

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        QPushButton.mousePressEvent(self, event)
        event.ignore()

class FunWidget(QWidget):
    def __init__(self, parent=None):
        super(FunWidget, self).__init__(parent)
        #cutButton PushButton
        self.cutButton = PushButton()
        self.cutButton.setFixedSize(40, 40)
        self.cutButton.setStyleSheet('''
        QPushButton{
            border-image: url("cut.png");
        }
        QPushButton:hover{
            border-image: url("cut_hover.png");
        }
        ''')
        #chatRecordsButton PushButton
        self.chatRecordsButton = PushButton()
        self.chatRecordsButton.setFixedSize(40, 40)
        self.chatRecordsButton.setStyleSheet('''
        QPushButton{
            border-image: url("chat_records.png");
        }
        QPushButton:hover{
            border-image: url("chat_records_hover.png");
        }
        ''')
        #newChatButton PushButton
        self.newChatButton = PushButton()
        self.newChatButton.setFixedSize(36, 36)
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
        self.mainHLayout.addWidget(self.cutButton)
        self.mainHLayout.addWidget(self.chatRecordsButton)
        self.mainHLayout.addWidget(self.newChatButton)
        self.mainHLayout.setAlignment(Qt.AlignRight)
        self.mainHLayout.setContentsMargins(10, 10, 10, 10)
        self.mainHLayout.setSpacing(10)
        #FunWidget adjust size
        self.resize(984, 60)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def connectCutButtonClick(self, fun):
        self.cutButton.clicked.connect(fun)

    def connectChatRecordsButtonClick(self, fun):
        self.chatRecordsButton.clicked.connect(fun)

class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.resize(954, 130)
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
            border: none;
            image: url("send_disable.png");
        }
        ''')
        self.setStyleSheet('''
        QTextEdit{
            border: none;
            background :transparent;
            font-size: 22px;
            selection-background-color: rgb(150, 10, 250);
        }
        QScrollBar{
            width: 25px;
        }
        ''')

    def mousePressEvent(self, event):
        QTextEdit.mousePressEvent(self, event)
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
        self.setMinimumHeight(40)
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
        #backgroundColorIsLight
        self.backgroundColorIsLight = False

    def paintEvent(self, event):
        #QPainter create
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #QPainterPath
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(self.rect().x() + 1, self.rect().y() + 1, self.rect().width() - 2, self.rect().height() - 2, 16, 16)
        #QBrush
        brush = QBrush(Qt.SolidPattern)
        #add rect and set brush
        if self.backgroundColorIsLight:
            #brush set color
            brush.setColor(QColor(Qt.transparent))
            #QPainter set pen
            pen = QPen(QColor(100, 100, 100))
            painter.setPen(pen)
        else:
            #brush set color
            brush.setColor(QColor(224, 224, 224))
            #QPainter set pen
            painter.setPen(Qt.NoPen)
        #QPainter set brush
        painter.setBrush(brush)
        #QPainter set path
        painter.drawPath(path.simplified())
        #QPainter end
        painter.end()

    def backgroundColorShowLight(self):
        self.backgroundColorIsLight = True
        self.repaint()

    def backgroundColorShowDark(self):
        self.backgroundColorIsLight = False
        self.repaint()

    def clearFocus(self):
        self.textEdit.clearFocus()

    def resetWidgetSize(self):
        self.textEdit.resize(self.width() - 40, self.height() - 40)

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
        self.font.setPixelSize(22)
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
        brush.setColor(QColor(224, 224, 224))
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

class LoadingLabel(QWidget):
    def __init__(self, parent=None):
        super(LoadingLabel, self).__init__(parent)
        self.setFixedSize(70, 28)
        self.mainHLayout = QHBoxLayout()
        self.setLayout(self.mainHLayout)
        self.subWidgetList = []
        for _ in range(3):
            subWidget = QWidget()
            subWidget.setFixedSize(14, 14)
            self.mainHLayout.addWidget(subWidget)
            self.subWidgetList.append(subWidget)
        self.mainHLayout.setContentsMargins(7, 7, 7, 7)
        self.mainHLayout.setSpacing(7)
        #QTimer
        self.loadingTimer = QTimer(self)
        self.loadingTimer.timeout.connect(self.loadingShow)
        self.loadingTimer.start(400)
        self.loadingNum = 0

    def loadingShow(self):
        for subWidget in self.subWidgetList:
            subWidget.setStyleSheet('''
                border: none;
                border-radius: 7px;
                background-color: rgb(150, 150, 150);
            ''')
        self.subWidgetList[self.loadingNum].setStyleSheet('''
            border: none;
            border-radius: 7px;
            background-color: rgb(80, 80, 80);
        ''')
        self.loadingNum = (self.loadingNum + 1) % 3

class MessageWidget(QWidget):
    def __init__(self, text, isUser=True, textMaxWidth=650, parent=None):
        super(MessageWidget, self).__init__(parent)
        self.text = text
        self.isUser = isUser
        #ImageLabel
        self.imageLabel = ImageLabel(isUser=self.isUser)
        #TextLabel
        self.textLabel = TextLabel(text, isUser=self.isUser, maxWidth=textMaxWidth)
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
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
            self.subVLayout1.addWidget(self.textWidget)
            self.subVLayout2.addWidget(self.imageLabel)
        else:
            self.subVLayout1.addWidget(self.imageLabel)
            self.loadingLabel = LoadingLabel()
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
        if not self.loadingLabelIsRemove:
            self.textLayout.removeWidget(self.loadingLabel)
            self.loadingLabel.deleteLater()
            self.loadingLabelIsRemove = True
            self.textWidget.setFixedSize(self.textLabel.width(), self.textLabel.height())
            self.setFixedSize(self.imageLabel.width() + 5 + self.textWidget.width(), self.imageLabel.height() if self.imageLabel.height() > self.textWidget.height() else self.textWidget.height())

    def getText(self):
        return self.text

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
        self.palette.setColor(QPalette.WindowText, QColor(150, 10, 250))
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
            self.label.resize(20, 20)
            self.mainHLayout.addWidget(self.label)
            self.mainHLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.mainHLayout)
            self.setFixedSize(30, 30)
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
            self.label.resize(20, 20)
            self.setFixedSize(30, 30)

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

    def mousePressEvent(self, event):
        QSpinBox.mousePressEvent(self, event)
        event.ignore()

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

    def mousePressEvent(self, event):
        QDoubleSpinBox.mousePressEvent(self, event)
        event.ignore()

    def enterEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def leaveEvent(self, event):
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

class Slider(QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
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

    def mousePressEvent(self, event):
        QSlider.mousePressEvent(self, event)
        event.ignore()

class LineEdit(QLineEdit):
    def __init__(self):
        super(LineEdit, self).__init__()
        #LineEdit
        self.resize(135, 30)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setPlaceholderText("搜索")
        #searchButton QPushButton
        self.searchButton = QPushButton(self)
        self.searchButton.setFixedSize(self.height(), self.height())
        self.searchButton.setIcon(QIcon("search.png"))
        self.searchButton.setIconSize(QSize(self.searchButton.width(), self.searchButton.height()))
        self.searchButton.setCursor(Qt.PointingHandCursor)
        self.searchButton.move(0, 0)
        #LineEdit
        self.setStyleSheet('''
        QPushButton{
            border: none;
        }
        QLineEdit{
            border: none;
            border-radius: 5px;
            background-color: #252525;
            padding-left: 30px;
        }
        ''')

class ChatRecordsWidget(QWidget):
    def __init__(self, parent=None):
        super(ChatRecordsWidget, self).__init__(parent)
        #ChatRecordsWidget adjust size
        self.resize(180, 390)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #LineEdit
        self.lineEdit = LineEdit()
        #clearAllButton QPushButton
        self.clearAllButton = QPushButton()
        self.clearAllButton.setFixedSize(self.lineEdit.height(), self.lineEdit.height())
        self.clearAllButton.setIconSize(QSize(self.clearAllButton.width(), self.clearAllButton.height()))
        self.clearAllButton.setCursor(Qt.PointingHandCursor)
        self.clearAllButton.setStyleSheet('''
        QPushButton{
            border: none;
            image: url("clearAll.png");
        }
        QPushButton:hover{
            image: url("clearAll_hover.png");
        }
        ''')
        #searchWidget QWidget
        self.searchWidget = QWidget()
        self.searchWidget.resize(self.width() - 10, 30)
        self.searchWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #searchHLayout QHBoxLayout
        self.searchHLayout = QHBoxLayout()
        self.searchWidget.setLayout(self.searchHLayout)
        self.searchHLayout.addWidget(self.lineEdit)
        self.searchHLayout.addWidget(self.clearAllButton)
        self.searchHLayout.setContentsMargins(0, 0, 0, 0)
        self.searchHLayout.setSpacing(5)
        self.searchHLayout.setStretch(0, 1)
        self.searchHLayout.setStretch(1, 0)
        #QLabel
        self.label = QLabel()
        self.label.resize(self.width() - 10, 30)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.font = QFont()
        self.font.setPixelSize(30)
        self.font.setBold(True)
        self.label.setFont(self.font)
        self.label.setText("聊天记录")
        self.label.setAlignment(Qt.AlignLeft)
        #QListWidget
        self.listWidget = QListWidget()
        self.listWidget.resize(self.width() - 10, 310)
        self.listWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setStyleSheet('''
        QListWidget{
            border: none;
            background: transparent;
        }
        ''')
        #mainWidget QWidget
        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName("chatRecordsFrame")
        self.mainWidget.resize(self.width(), self.height())
        self.mainWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #mainVLayout QVBoxLayout
        self.mainVLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.addWidget(self.label)
        self.mainVLayout.addWidget(self.searchWidget)
        self.mainVLayout.addWidget(self.listWidget)
        self.mainVLayout.setContentsMargins(5, 0, 5, 0)
        self.mainVLayout.setSpacing(10)
        self.mainVLayout.setStretch(0, 0)
        self.mainVLayout.setStretch(1, 0)
        self.mainVLayout.setStretch(2, 1)
        #ChatRecordsWidget set styleSheet
        self.setStyleSheet('''
        QWidget#chatRecordsFrame{
            border: none;
            border-radius: 10px;
        }
        ''')

    def connectListItemClick(self, fun):
        self.listWidget.itemClicked.connect(fun)

    def addListItem(self, string):
        self.chatRecordItem = QListWidgetItem(string, self.listWidget)
        self.chatRecordItem.setSizeHint(QSize(self.listWidget.width(), 60))
        return self.chatRecordItem

    def delListItem(self, item):
        self.listWidget.takeItem(self.listWidget.row(item))
        item.deleteLater()

    def listItemSetData(self, item, string):
        item.setData(Qt.UserRole, QVariant(string))

    def listItemToString(self, item):
        return item.data(Qt.UserRole)

    def stringToListItem(self, string):
        for i in range(0, self.listWidget.count()):
            if self.listWidget.item(i).data(Qt.UserRole) == string:
                return self.listWidget.item(i)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        self.setStyleSheet('''
        @font-face {
            font-family: "阿里妈妈东方大楷 Regular";
            font-weight: 484;
            src: url("EastDakaiFont/XO2u6KVS95AG.woff2") format("woff2"), url("EastDakaiFont/XO2u6KVS95AG.woff") format("woff");
            font-display: swap;
        }
        ''')
        self.setObjectName("MainWindow")
        self.installEventFilter(self)
        #chatShowSpacer QSpacerItem
        self.chatShowSpacer = QSpacerItem(self.width() - 50, 10, hPolicy=QSizePolicy.Expanding, vPolicy=QSizePolicy.Fixed)
        #ListWidget
        self.chatShow = ListWidget()
        #chatShowFull QWidget
        self.chatShowFull = QWidget()
        self.chatShowFull.resize(974, 390)
        self.chatShowFull.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #chatShowFullVLayout QVBoxLayout
        self.chatShowFullVLayout = QVBoxLayout()
        self.chatShowFull.setLayout(self.chatShowFullVLayout)
        self.chatShowFullVLayout.addSpacerItem(self.chatShowSpacer)
        self.chatShowFullVLayout.addWidget(self.chatShow)
        self.chatShowFullVLayout.setContentsMargins(0, 0, 0, 0)
        self.chatShowFullVLayout.setSpacing(0)
        self.chatShowFullVLayout.setStretch(0, 0)
        self.chatShowFullVLayout.setStretch(1, 1)
        #setting QWidget init
        self.settingWidgetInit()
        #topWidget QWidget
        self.topWidget = QWidget()
        self.topWidget.resize(1024, 360)
        self.topWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #topHLayout QHBoxLayout
        self.topHLayout = QHBoxLayout()
        self.topWidget.setLayout(self.topHLayout)
        self.topHLayout.addWidget(self.buttonWidget)
        self.topHLayout.addWidget(self.chatShowFull)
        self.topHLayout.setContentsMargins(0, 0, 10, 0)
        self.topHLayout.setSpacing(0)
        self.topHLayout.setStretch(0, 0)
        self.topHLayout.setStretch(1, 1)
        #FunWidget
        self.chatFun = FunWidget()
        self.chatFun.connectCutButtonClick(self.saveImage)
        self.chatFun.connectChatRecordsButtonClick(self.showChatRecords)
        #TextEditFull
        self.chatInput = TextEditFull()
        self.chatInput.connectSendButtonClick(self.sendMessage)
        #bottomWidget QWidget
        self.bottomWidget = QWidget()
        self.bottomWidget.resize(1024, 240)
        self.bottomWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #bottomVLayout QVBoxLayout
        self.bottomVLayout = QVBoxLayout()
        self.bottomWidget.setLayout(self.bottomVLayout)
        self.bottomVLayout.addWidget(self.chatFun)
        self.bottomVLayout.addWidget(self.chatInput)
        self.bottomVLayout.setContentsMargins(20, 0, 20, 20)
        self.bottomVLayout.setSpacing(0)
        self.bottomVLayout.setStretch(0, 0)
        self.bottomVLayout.setStretch(1, 1)
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
        self.mainVLayout.setStretch(1, 2)
        #messageWidget list
        self.messageWidgetList = []
        #ChatRecordsWidget
        self.chatRecordsWidget = ChatRecordsWidget(self)
        self.chatRecordsWidget.connectListItemClick(self.generateChatRecord)
        self.chatRecordsWidget.move(834, 10)
        self.chatRecordsWidget.raise_()
        self.chatRecordsWidget.hide()
        #chatRecords dictionary
        #self.ChatRecordsDict = {}
        #emptyTextLabel PrintLabel
        self.emptyTextLabel = PrintLabel("文本不能为空", self)
        self.emptyTextLabel.move(int((self.width() - self.emptyTextLabel.width()) / 2), self.chatShow.height() - self.emptyTextLabel.height() + 60)
        self.emptyTextLabel.raise_()
        self.emptyTextLabel.hide()
        #saveImageLabel PrintLabel
        self.saveImageLabel = PrintLabel('', self)
        self.saveImageLabel.move(int((self.width() - self.saveImageLabel.width()) / 2), self.chatShow.height() - self.saveImageLabel.height() + 60)
        self.saveImageLabel.raise_()
        self.saveImageLabel.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.settingWidgetIsOpen:
                notSettingRect = QRect(self.settingWidget.width(), 0, self.width() - self.settingWidget.width(), self.height())
                if notSettingRect.contains(event.pos()):
                    self.animationMove.setDirection(QAbstractAnimation.Backward)
                    self.animationMove.start()
                    self.settingWidgetIsOpen = False
            else:
                chatInputRect = QRect(self.chatInput.geometry().x(), self.chatInput.geometry().y() + self.topWidget.height(), self.chatInput.geometry().width(), self.chatInput.geometry().height())
                if chatInputRect.contains(event.pos()):
                    self.chatInput.backgroundColorShowLight()
                else:
                    self.chatInput.backgroundColorShowDark()
                    self.chatInput.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def resizeEvent(self, event):
        #TextLabel max width
        textMaxWidth = int(self.chatShow.width() * 2 / 3)
        for i in range(0, self.chatShow.count()):
            #messageWidget set max width of textLabel
            self.messageWidgetList[i].setTextMaxWidth(textMaxWidth)
            messageWidget = self.messageWidgetList[i]
            #chatShow itemWidget adjust size
            self.chatShow.itemWidget(self.chatShow.item(i)).setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            if messageWidget.getIsUser():
                self.chatShow.itemWidget(self.chatShow.item(i)).layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 5, 5, 5, 5)
            else:
                self.chatShow.itemWidget(self.chatShow.item(i)).layout().setContentsMargins(5, 5, itemWidget.width() - messageWidget.width() - 5, 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))
        #TextEditFull adjust size
        self.chatInput.resetWidgetSize()
        #move emptyTextLabel
        self.emptyTextLabel.move(int((self.width() - self.emptyTextLabel.width()) / 2), self.chatShow.height() - self.emptyTextLabel.height() + 60)
        #move saveImageLabel
        self.saveImageLabel.move(int((self.width() - self.saveImageLabel.width()) / 2), self.chatShow.height() - self.saveImageLabel.height() + 60)

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
        self.maxTokensWidget.resize(301, 120)
        self.maxTokensWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.maxTokensWidget.setObjectName("maxTokensWidget")
        self.maxTokensWidget.setStyleSheet('''
        QWidget#maxTokensWidget{
            border-radius: 20px;
            background: #a0a0a0;
        }
        ''')
        #setting maxTokens top sub QWidget
        self.maxTokensTopSubWidget = QWidget()
        self.maxTokensTopSubWidget.resize(261, 40)
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
        self.maxTokensTopSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting maxTokens bottom sub QWidget
        self.maxTokensBottomSubWidget = QWidget()
        self.maxTokensBottomSubWidget.resize(261, 40)
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
        self.maxTokensBottomSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting maxTokens QVBoxLayout
        self.maxTokensVLayout = QVBoxLayout()
        self.maxTokensWidget.setLayout(self.maxTokensVLayout)
        self.maxTokensVLayout.addWidget(self.maxTokensTopSubWidget)
        self.maxTokensVLayout.addWidget(self.maxTokensBottomSubWidget)
        self.maxTokensVLayout.setContentsMargins(20, 20, 20, 20)
        self.maxTokensVLayout.setSpacing(0)
        #setting topP QWidget
        self.topPWidget = QWidget()
        self.topPWidget.resize(301, 120)
        self.topPWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.topPWidget.setObjectName("topPWidget")
        self.topPWidget.setStyleSheet('''
        QWidget#topPWidget{
            border-radius: 20px;
            background: #a0a0a0;
        }
        ''')
        #setting topP top sub QWidget
        self.topPTopSubWidget = QWidget()
        self.topPTopSubWidget.resize(261, 40)
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
        self.topPTopSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting topP bottom sub QWidget
        self.topPBottomSubWidget = QWidget()
        self.topPBottomSubWidget.resize(261, 40)
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
        self.topPBottomSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting topP QVBoxLayout
        self.topPVLayout = QVBoxLayout()
        self.topPWidget.setLayout(self.topPVLayout)
        self.topPVLayout.addWidget(self.topPTopSubWidget)
        self.topPVLayout.addWidget(self.topPBottomSubWidget)
        self.topPVLayout.setContentsMargins(20, 20, 20, 20)
        self.topPVLayout.setSpacing(0)
        #setting temperature QWidget
        self.temperatureWidget = QWidget()
        self.temperatureWidget.resize(301, 120)
        self.temperatureWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.temperatureWidget.setObjectName("temperatureWidget")
        self.temperatureWidget.setStyleSheet('''
        QWidget#temperatureWidget{
            border-radius: 20px;
            background: #a0a0a0;
        }
        ''')
        #setting temperature top sub QWidget
        self.temperatureTopSubWidget = QWidget()
        self.temperatureTopSubWidget.resize(261, 40)
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
        self.temperatureTopSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting temperature bottom sub QWidget
        self.temperatureBottomSubWidget = QWidget()
        self.temperatureBottomSubWidget.resize(261, 40)
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
        self.temperatureBottomSubHLayout.setContentsMargins(0, 0, 0, 0)
        #setting temperature QVBoxLayout
        self.temperatureVLayout = QVBoxLayout()
        self.temperatureWidget.setLayout(self.temperatureVLayout)
        self.temperatureVLayout.addWidget(self.temperatureTopSubWidget)
        self.temperatureVLayout.addWidget(self.temperatureBottomSubWidget)
        self.temperatureVLayout.setContentsMargins(20, 20, 20, 20)
        self.temperatureVLayout.setSpacing(0)
        #setting QWidget
        self.settingWidget = QWidget(self)
        self.settingWidget.resize(self.width() // 3, self.height())
        self.settingWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.settingWidget.setObjectName("settingWidget")
        self.settingWidget.setStyleSheet('''
        QWidget#settingWidget{
            background: #d0d0d0;
        }
        ''')
        self.settingWidget.move(-self.settingWidget.width(), 0)
        #setting QVBoxLayout
        self.settingVLayout = QVBoxLayout()
        self.settingWidget.setLayout(self.settingVLayout)
        self.settingVLayout.addWidget(self.maxTokensWidget)
        self.settingVLayout.addWidget(self.topPWidget)
        self.settingVLayout.addWidget(self.temperatureWidget)
        self.settingVLayout.setContentsMargins(20, 60, 20, 60)
        self.settingVLayout.setSpacing(60)
        #animationMove QPropertyAnimation
        self.animationMove = QPropertyAnimation(self.settingWidget, b'geometry')
        self.animationMove.setDuration(1000)
        self.animationMove.setEasingCurve(QEasingCurve.OutQuad)
        self.animationMove.setStartValue(QRect(-self.settingWidget.width(), 0, self.settingWidget.width(), self.settingWidget.height()))
        self.animationMove.setEndValue(QRect(0, 0, self.settingWidget.width(), self.settingWidget.height()))
        #settingWidgetIsOpen
        self.settingWidgetIsOpen = False
        #settingButton PushButton
        self.settingButton = PushButton()
        self.settingButton.setFixedSize(40, 40)
        self.settingButton.setIcon(QIcon("setting.png"))
        self.settingButton.setIconSize(QSize(28, 28))
        self.settingButton.setStyleSheet('''
        QPushButton{
            border: none;
            background: transparent;
        }
        QPushButton:hover{
            border-radius: 20px;
            background: white;
        }
        ''')
        self.settingButton.clicked.connect(self.settingButtonClicked)
        #buttonSpacerItem QSpacerItem
        self.buttonSpacerItem = QSpacerItem(40, self.chatShowFull.height() - 40, hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Expanding)
        #buttonWidget QWidget
        self.buttonWidget = QWidget()
        self.buttonWidget.resize(40, self.chatShowFull.height())
        self.buttonWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        #buttonVLayout QVBoxLayout
        self.buttonVLayout = QVBoxLayout()
        self.buttonWidget.setLayout(self.buttonVLayout)
        self.buttonVLayout.addWidget(self.settingButton)
        self.buttonVLayout.addSpacerItem(self.buttonSpacerItem)
        self.buttonVLayout.setContentsMargins(0, 0, 0, 0)

    def settingButtonClicked(self):
        self.settingWidget.raise_()
        self.animationMove.setDirection(QAbstractAnimation.Forward)
        self.animationMove.start()
        self.settingWidgetIsOpen = True
        #TextLabel max width
        '''textMaxWidth = int(self.chatShow.width() * 2 / 3)
        for i in range(0, self.chatShow.count()):
            #messageWidget set max width of textLabel
            self.messageWidgetList[i].setTextMaxWidth(textMaxWidth)
            messageWidget = self.messageWidgetList[i]
            #chatShow itemWidget adjust size
            self.chatShow.itemWidget(self.chatShow.item(i)).setFixedSize(self.chatShow.width(), messageWidget.height() + 10)
            itemWidget = self.chatShow.itemWidget(self.chatShow.item(i))
            if messageWidget.getIsUser():
                self.chatShow.itemWidget(self.chatShow.item(i)).layout().setContentsMargins(itemWidget.width() - messageWidget.width() - 5, 5, 5, 5)
            else:
                self.chatShow.itemWidget(self.chatShow.item(i)).layout().setContentsMargins(5, 5, itemWidget.width() - messageWidget.width() - 5, 5)
            #chatShow item adjust size
            self.chatShow.item(i).setSizeHint(QSize(self.chatShow.width(), messageWidget.height() + 10))'''

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
        if not self.chatInput.sendButtonIsEnable():
            return
        #get text from TextEditFull
        text = self.chatInput.toPlainText()
        if not text == '':
            #MessageWidget
            self.messageSendWidget = MessageWidget(text, isUser=True, textMaxWidth=int(self.chatShow.width() * 2 / 3))
            self.messageWidgetList.append(self.messageSendWidget)
            #itemSendWidget QWidget
            self.itemSendWidget = QWidget(self)
            self.itemSendHLayout = QHBoxLayout()
            self.itemSendHLayout.addWidget(self.messageSendWidget)
            self.itemSendWidget.setLayout(self.itemSendHLayout)
            self.itemSendWidget.setFixedSize(self.chatShow.width(), self.messageSendWidget.height() + 10)
            self.itemSendHLayout.setContentsMargins(self.itemSendWidget.width() - self.messageSendWidget.width() - 5, 5, 5, 5)
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
        #MessageWidget
        self.messageRecvWidget = MessageWidget(self.Message, isUser=False, textMaxWidth=int(self.chatShow.width() * 2 / 3))
        self.messageWidgetList.append(self.messageRecvWidget)
        #itemRecvWidget QWidget
        self.itemRecvWidget = QWidget(self)
        self.itemRecvHLayout = QHBoxLayout()
        self.itemRecvHLayout.addWidget(self.messageRecvWidget)
        self.itemRecvWidget.setLayout(self.itemRecvHLayout)
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
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
        #messageWidget set text of textLabel
        self.messageRecvWidget.setText(self.Message)
        #chatShow itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
        #chatShow item adjust size
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))

    def messageFinish(self):
        #messageRecvWidget remove LoadingLabel
        self.messageRecvWidget.removeLoadingLabel()
        #chatShow itemWidget adjust size
        self.itemRecvWidget.setFixedSize(self.chatShow.width(), self.messageRecvWidget.height() + 10)
        self.itemRecvHLayout.setContentsMargins(5, 5, self.itemRecvWidget.width() - self.messageRecvWidget.width() - 5, 5)
        #chatShow item adjust size
        self.recvItem.setSizeHint(QSize(self.chatShow.width(), self.messageRecvWidget.height() + 10))
        #enable sendButton
        self.chatInput.enableSendButton()

    def saveImage(self):
        #chatRect QRect
        self.chatRect = QRect()
        if self.settingButtonIsRight:
            self.chatRect = QRect(self.chatShow.x() + 40, self.chatShow.y(), self.chatShow.width(), self.chatShow.height())
        else:
            self.chatRect = QRect(self.topWidget.x(), self.topWidget.y(), self.topWidget.width(), self.topWidget.height())
        #chatPixmap QPixmap
        self.chatPixmap = self.grab(self.chatRect)
        #chatPixmapName QString
        self.chatPixmapName = "chat_"
        self.chatPixmapName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
        self.chatPixmapName += ".png"
        #save image
        if self.chatPixmap.save(self.chatPixmapName, "png"):
            self.saveImageLabel.setText("图像保存成功")
            self.saveImageLabel.move(int((self.width() - self.saveImageLabel.width()) / 2), self.chatShow.height() - self.saveImageLabel.height() + 60)
            self.saveImageLabel.printStart()
        else:
            self.saveImageLabel.setText("图像保存失败")
            self.saveImageLabel.move(int((self.width() - self.saveImageLabel.width()) / 2), self.chatShow.height() - self.saveImageLabel.height() + 60)
            self.saveImageLabel.printStart()

    def showChatRecords(self):
        #init
        chatRecordStr = ''
        isNewFile = True
        isLatest = False
        oldFileName = ''
        #generate item
        for fileName in os.listdir(os.curdir):
            if fileName.endswith(".txt"):
                with open(fileName, 'r') as f:
                    lines = f.readlines()
                #create item
                chatRecordStr = lines[0] + '\n' + lines[len(lines) - 2]
                self.chatRecordsWidget.addListItem(chatRecordStr)
        #judge whether messageWidgetList is empty
        if len(self.messageWidgetList) != 0:
            chatRecordStr = self.messageWidgetList[1].getText()
            #judge old or Latest
            for fileName in os.listdir(os.curdir):
                if fileName.endswith(".txt"):
                    with open(fileName, 'r') as f:
                        lines = f.readlines()
                    if lines[2] == chatRecordStr:
                        isNewFile = False
                        if len(lines) == len(self.messageWidgetList) * 2:
                            isLatest = True
                        else:
                            oldFileName = fileName
                        break
            if not isNewFile:
                if not isLatest:
                    #delete item
                    #item = [k for k, v in self.ChatRecordsDict if v == oldFileName]
                    #self.ChatRecordsDict.pop(item)
                    item = self.chatRecordsWidget.stringToListItem(oldFileName)
                    self.chatRecordsWidget.delListItem(item)
                    #item.deleteLater()
                    #create item
                    chatRecordStr = self.messageWidgetList[0].getText() + '\n' + self.messageWidgetList[len(self.messageWidgetList) - 1].getText()
                    item = self.chatRecordsWidget.addListItem(chatRecordStr)
                    #change chatRecord file name
                    self.chatRecordFileName = "chat_"
                    self.chatRecordFileName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
                    self.chatRecordFileName += ".txt"
                    os.rename(oldFileName, self.chatRecordFileName)
                    #clear chatRecord file
                    with open(self.chatRecordFileName, 'w') as f:
                        f.truncate()
                    #write to chatRecord file
                    with open(self.chatRecordFileName, 'a') as f:
                        for i in range(0, self.chatShow.count()):
                            chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                            f.write(chatRecordStr)
                    #add to dictionary
                    #self.ChatRecordsDict[self.chatRecordItem] = self.chatRecordFileName
                    #item set data
                    self.chatRecordsWidget.listItemSetData(item, self.chatRecordFileName)
            else:
                #create item
                chatRecordStr = self.messageWidgetList[0].getText() + '\n' + self.messageWidgetList[len(self.messageWidgetList) - 1].getText()
                item = self.chatRecordsWidget.addListItem(chatRecordStr)
                #chatRecordFileName QString
                self.chatRecordFileName = "chat_"
                self.chatRecordFileName += QDateTime.currentDateTime().toString("yyyy_MM_dd_HH_mm_ss")
                self.chatRecordFileName += ".txt"
                #write to chatRecord file
                with open(self.chatRecordFileName, 'a') as f:
                    for i in range(0, self.chatShow.count()):
                        chatRecordStr = self.messageWidgetList[i].getText() + '\n' + str(self.messageWidgetList[i].getIsUser()) + '\n'
                        f.write(chatRecordStr)
                #add to dictionary
                #self.ChatRecordsDict[self.chatRecordItem] = self.chatRecordFileName
                #item set data
                self.chatRecordsWidget.listItemSetData(item, self.chatRecordFileName)
        #show chatRecordsWidget
        self.chatRecordsWidget.show()

    def generateChatRecord(self, item):
        #init
        isUser = True
        self.messageWidgetList.clear()
        #read chatRecord file
        #with open(self.ChatRecordsDict[item], 'r') as f:
        with open(self.chatRecordsWidget.listItemToString(item), 'r') as f:
            lines = f.readlines()
        #generate QListWidgetItem
        for i in range(0, len(lines), 2):
            if lines[i + 1] == "True":
                isUser = True
            else:
                isUser = False
            #MessageWidget
            self.messageWidget = MessageWidget(lines[i], isUser=isUser, textMaxWidth=int(self.chatShow.width() * 2 / 3))
            self.messageWidgetList.append(self.messageWidget)
            #itemWidget QWidget
            self.itemWidget = QWidget(self)
            self.itemHLayout = QHBoxLayout()
            self.itemHLayout.addWidget(self.messageWidget)
            self.itemWidget.setLayout(self.itemHLayout)
            self.itemWidget.setFixedSize(self.chatShow.width(), self.messageWidget.height() + 10)
            if isUser:
                self.itemHLayout.setContentsMargins(self.itemWidget.width() - self.messageWidget.width() - 5, 5, 5, 5)
            else:
                self.itemHLayout.setContentsMargins(5, 5, self.itemWidget.width() - self.messageWidget.width() - 5, 5)
            #QListWidgetItem
            self.item = QListWidgetItem(self.chatShow)
            self.item.setSizeHint(QSize(self.chatShow.width(), self.messageWidget.height() + 10))
            self.chatShow.setItemWidget(self.item, self.itemWidget)
            self.chatShow.setCurrentItem(self.item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
