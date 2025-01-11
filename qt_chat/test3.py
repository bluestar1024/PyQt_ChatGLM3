import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QCursor
from enum import Enum

class RegionEnum(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM=3
    LEFTTOP = 4
    RIGHTTOP = 5
    LEFTBOTTOM = 6
    RIGHTBOTTOM = 7
    MIDDLE = 8

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent) 
        self.resize(1024, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle('AI助理')
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setMinimumSize(250, 150)
        self.leftButtonIsPress = False
        self.regionDir = RegionEnum.MIDDLE
        self.setMouseTracking(True)

    def regionDivision(self):
        PADDING = 2
        if self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + PADDING and self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + PADDING:
            # 左上角
            self.regionDir = RegionEnum.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - PADDING and self.cursorGlobalX <= self.uiGlobalBR.x() and self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + PADDING:
            # 右上角
            self.regionDir = RegionEnum.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + PADDING and self.cursorGlobalY >= self.uiGlobalBR.y() - PADDING and self.cursorGlobalY <= self.uiGlobalBR.y():
            # 左下角
            self.regionDir = RegionEnum.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - PADDING and self.cursorGlobalX <= self.uiGlobalBR.x() and self.cursorGlobalY >= self.uiGlobalBR.y() - PADDING and self.cursorGlobalY <= self.uiGlobalBR.y():
            # 右下角
            self.regionDir = RegionEnum.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif self.cursorGlobalX >= self.uiGlobalTL.x() and self.cursorGlobalX <= self.uiGlobalTL.x() + PADDING:
            # 左边
            self.regionDir = RegionEnum.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif self.cursorGlobalX >= self.uiGlobalBR.x() - PADDING and self.cursorGlobalX <= self.uiGlobalBR.x():
            # 右边
            self.regionDir = RegionEnum.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif self.cursorGlobalY >= self.uiGlobalTL.y() and self.cursorGlobalY <= self.uiGlobalTL.y() + PADDING:
            # 上边
            self.regionDir = RegionEnum.TOP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif self.cursorGlobalY >= self.uiGlobalBR.y() - PADDING and self.cursorGlobalY <= self.uiGlobalBR.y():
            # 下边
            self.regionDir = RegionEnum.BOTTOM
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            # 默认
            self.regionDir = RegionEnum.MIDDLE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        print('mouseReleaseEvent')
        if event.button() == Qt.LeftButton:
            self.leftButtonIsPress = False
            #if self.regionDir != RegionEnum.MIDDLE:
                #self.releaseMouse()
                #self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        print('mousePressEvent')
        match event.button():
            case Qt.LeftButton:
                self.leftButtonIsPress = True
                if self.regionDir == RegionEnum.MIDDLE:
                    #self.mouseGrabber()
                #else:
                    self.pressPosDistanceUiGlobalTL = self.geometry().topLeft() - event.globalPos()
            case Qt.RightButton:
                self.close()
            case _:
                QMainWindow.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        print('mouseMoveEvent')
        self.cursorGlobalPos = event.globalPos()
        self.cursorGlobalX = self.cursorGlobalPos.x()
        self.cursorGlobalY = self.cursorGlobalPos.y()
        #self.uiRect = self.rect()
        #self.uiGlobalTL = self.mapToGlobal(self.uiRect.topLeft())
        #self.uiGlobalBR = self.mapToGlobal(self.uiRect.bottomRight())
        self.uiGlobalTL = self.geometry().topLeft()
        self.uiGlobalBR = self.geometry().bottomRight()

        if not self.leftButtonIsPress:
            self.regionDivision()
        else:
            if self.regionDir != RegionEnum.MIDDLE:
                print('RegionEnum.MIDDLE')
                uiGlobalRect = QRect(self.uiGlobalTL, self.uiGlobalBR)
                match self.regionDir:
                    case RegionEnum.LEFT:
                        print('RegionEnum.LEFT')
                        if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                            uiGlobalRect.setX(self.cursorGlobalX)
                    case RegionEnum.RIGHT:
                        print('RegionEnum.RIGHT')
                        if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                            uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
                    case RegionEnum.TOP:
                        print('RegionEnum.TOP')
                        if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                            uiGlobalRect.setY(self.cursorGlobalY)
                    case RegionEnum.BOTTOM:
                        print('RegionEnum.BOTTOM')
                        if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                            uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
                    case RegionEnum.LEFTTOP:
                        print('RegionEnum.LEFTTOP')
                        if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                            uiGlobalRect.setX(self.cursorGlobalX)
                        if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                            uiGlobalRect.setY(self.cursorGlobalY)
                    case RegionEnum.RIGHTTOP:
                        print('RegionEnum.RIGHTTOP')
                        if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                            uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
                        if self.uiGlobalBR.y() - self.cursorGlobalY > self.minimumHeight():
                            uiGlobalRect.setY(self.cursorGlobalY)
                    case RegionEnum.LEFTBOTTOM:
                        print('RegionEnum.LEFTBOTTOM')
                        if self.uiGlobalBR.x() - self.cursorGlobalX > self.minimumWidth():
                            uiGlobalRect.setX(self.cursorGlobalX)
                        if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                            uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
                    case RegionEnum.RIGHTBOTTOM:
                        print('RegionEnum.RIGHTBOTTOM')
                        if self.cursorGlobalX - self.uiGlobalTL.x() > self.minimumWidth():
                            uiGlobalRect.setWidth(self.cursorGlobalX - self.uiGlobalTL.x())
                        if self.cursorGlobalY - self.uiGlobalTL.y() > self.minimumHeight():
                            uiGlobalRect.setHeight(self.cursorGlobalY - self.uiGlobalTL.y())
                self.setGeometry(uiGlobalRect)
            else:
                self.move(self.pressPosDistanceUiGlobalTL + event.globalPos())
        QMainWindow.mouseMoveEvent(self, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
