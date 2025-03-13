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

config_file_name = 'config.txt'
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
        self.mainHLayout.setContentsMargins(10, 3, 3, 3)
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
        brush.setColor(Qt.transparent)
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
        font_file_path = 'msyhl.ttc'
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

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignHCenter)
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
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('''
        QMainWindow{
            background-color: #30F030;
        }
        ''')
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
        self.chatFun.connectSettingButtonClick(self.settingButtonClicked)
        self.chatFun.connectChatRecordsButtonClick(self.showChatRecords)
        self.chatFun.connectNewChatButtonClick(self.newChat)
        #ListWidget
        self.chatShow = ListWidget()
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
        shadow = QGraphicsDropShadowEffect(self.mainWidget)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.mainWidget.setGraphicsEffect(shadow)
        #MainWindow
        #self.setCentralWidget(self.mainWidget)
        #messageWidget list
        self.messageWidgetList = []
        #setting QWidget init
        self.settingWidgetInit()
        #ChatRecordsWidget
        self.chatRecordsWidget = ChatRecordsWidget(self.mainWidget)
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
        self.chatRecordsAnimationMove2.finished.connect(self.chatRecordsUiMoveFinished)
        #chatRecordsWidgetIsOpen
        self.chatRecordsWidgetIsOpen = False
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

    def mouseMoveEvent(self, event):
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
        print('stretch', self.uiGlobalTL)
        print('stretch', self.uiGlobalBR)
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
        print('stretch', windowGlobalRect)
        print('stretch', uiGlobalRect)
        self.setGeometry(windowGlobalRect)
        #self.mainWidget.setGeometry(uiGlobalRect)

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
        QMainWindow.mouseReleaseEvent(self, event)

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
        #TextEditFull adjust size
        self.chatInput.resetWidgetSize()
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
        self.titleIconLabel.setPixmap(QPixmap('AI助理.png'))
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
        self.titleLeftSubWidget.resize(self.titleIconLabel.width() + self.titleTextLabel.width() + 11, 36)
        self.titleLeftSubWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        #titleLeftSubHLayout QHBoxLayout
        self.titleLeftSubHLayout = QHBoxLayout()
        self.titleLeftSubWidget.setLayout(self.titleLeftSubHLayout)
        self.titleLeftSubHLayout.addWidget(self.titleIconLabel)
        self.titleLeftSubHLayout.addWidget(self.titleTextLabel)
        self.titleLeftSubHLayout.setAlignment(Qt.AlignLeft)
        self.titleLeftSubHLayout.setContentsMargins(10, 3, 3, 3)
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
            self.maxButton.setIcon(QIcon("max.png"))
        else:
            self.showMaximized()
            self.maxButton.setIcon(QIcon("normal.png"))

    def UiClose(self):
        self.saveCurChatRecord(withholdCurChatFile=True)
        self.close()

    def settingWidgetInit(self):
        #setting config file
        if not os.path.exists(config_file_name):
            with open(config_file_name, "w") as f:
                global init_base_url, init_api_key, init_model, init_maxTokens_currentVal, init_topP_currentVal, init_temperature_currentVal
                f.write(init_base_url + '\n' + init_api_key + '\n' + init_model + '\n' + str(init_maxTokens_currentVal) + '\n' + str(init_topP_currentVal) + '\n' + str(init_temperature_currentVal) + '\n')
        with open(config_file_name, "r") as f:
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
        #settingAnimationMove2 QPropertyAnimation
        self.settingAnimationMove2 = QPropertyAnimation(self.settingWidget, b'geometry')
        self.settingAnimationMove2.setDuration(1000)
        self.settingAnimationMove2.setEasingCurve(QEasingCurve.OutQuad)
        #settingWidgetIsOpen
        self.settingWidgetIsOpen = False

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
        self.chatShow.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.mainWidget.width() - rect.x() - self.settingWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.settingWidget.width(), 0, 0, 0)
        #
        print('setting move', self.settingWidget.geometry())
        print('setting move', self.chatRecordsWidget.geometry())
        print('setting move', self.mainWidget.geometry())
        print('setting move', self.geometry())

    def chatRecordsUiAnimationMove(self, rect):
        self.chatShow.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width() - 29, self.chatShow.height())
        self.chatShowWidget.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.chatShowWidget.height())
        self.chatInput.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width() - 40, self.chatInput.height())
        self.chatInput.resetWidgetSize()
        self.chatInputWidget.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.chatInputWidget.height())
        self.splitter.resize(self.mainWidget.width() - rect.x() - self.chatRecordsWidget.width(), self.splitter.height())
        self.contentVLayout.setContentsMargins(rect.x() + self.chatRecordsWidget.width(), 0, 0, 0)
        #
        print('record move', self.settingWidget.geometry())
        print('record move', self.chatRecordsWidget.geometry())
        print('record move', self.mainWidget.geometry())
        print('record move', self.geometry())

    def chatRecordsUiMoveFinished(self):
        if not self.chatRecordsWidgetIsOpen:
            #delete all item
            self.chatRecordsWidget.delAllListItems()

    def sendMessage(self):
        return

    def messageStart(self):
        return

    def recvMessage(self, text):
        return

    def messageFinish(self):
        return

    def showChatRecords(self):
        if not self.chatRecordsWidgetIsOpen:
            if not self.settingWidgetIsOpen:
                #show chatRecordsWidget
                self.chatRecordsWidget.raise_()
                self.chatRecordsAnimationMove.setStartValue(self.chatRecordsWidget.geometry())
                self.chatRecordsAnimationMove.setEndValue(QRect(0, self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                self.chatRecordsAnimationMove.start()
                self.chatRecordsWidgetIsOpen = True
                self.chatRecordsIsTop = True
            else:
                #show chatRecordsWidget
                self.chatRecordsWidget.raise_()
                self.chatRecordsAnimationMove2.setStartValue(self.chatRecordsWidget.geometry())
                self.chatRecordsAnimationMove2.setEndValue(QRect(0, self.titleWidget.height(), self.chatRecordsWidget.width(), self.chatRecordsWidget.height()))
                self.chatRecordsAnimationMove2.start()
                self.chatRecordsWidgetIsOpen = True
                self.chatRecordsIsTop = True
                self.settingIsTop = False
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
        return 

    def clearAllChatRecords(self):
        return

    def generateChatRecord(self, item):
        return

    def newChat(self):
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font_file_path = 'msyhl.ttc'
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
