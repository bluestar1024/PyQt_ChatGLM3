
import sys
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
#from PyQt5.QtCore import QObject,pyqtProperty
 
#使用一个背景颜色动画来展示Qt属性
class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.color=QColor(0,0,0)
 
        self.animation=QPropertyAnimation(self)
        self.animation.setTargetObject(self) #绑定目标对象
        self.animation.setPropertyName(b'mycolor') #bytearray类型
        self.animation.setStartValue(QColor(255,0,0))
        self.animation.setEndValue(QColor(0,255,255))
        self.animation.setDuration(2000) #2s=2000ms     
        self.animation.setLoopCount(-1) #一直循环
        self.animation.start() #启动动画
 
 
    def paintEvent(self,event):
        super().paintEvent(event)
        painter=QPainter(self)
        painter.fillRect(self.rect(),self.color)
 
    #获取属性值
    @pyqtProperty(QColor)
    def mycolor(self):
        return self.color
 
    #设置属性值，也可以写@mycolor.write
    @mycolor.setter
    def mycolor(self,value):
        self.color=value
        self.update()
 
 
if __name__ == "__main__":
    app=QApplication(sys.argv)
 
    w=MyLabel()
    w.setWindowTitle("龚建波 1992")
    w.resize(400,400)
    w.show()
   
    sys.exit(app.exec_())
