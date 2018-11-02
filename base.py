#相关的基础数据
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel
from PyQt5.QtGui import QPalette,QPixmap,QIcon,QBrush
from PyQt5 import QtCore,QtGui
import sys
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import  pyqtSignal
class TDPushButton(QLabel):
    clicked=pyqtSignal()
    def __init__(self,str1,str2,str3,parent):
        super().__init__(parent)

        self.pic_normal=QPixmap(str1)
        self.pic_hover=QPixmap(str2)
        self.pic_press=QPixmap(str3)
        #图片大小，显示正常状态下的图片
        self.resize(self.pic_normal.size())
        self.setPixmap(self.pic_normal)

    def enterEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.pic_hover)
    def leaveEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.pic_normal)


    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.setPixmap(self.pic_press)
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.clicked.emit()
        self.setPixmap(self.pic_hover)
class Chess(QLabel):
    def __init__(self,color='w',parent=None):
        super().__init__(parent)
        self.color=color
        if color=='w':
            pic=QPixmap("photos/白子.png")
        elif color =='b':
            pic = QPixmap("photos/黑子.png")
        self.resize(pic.size())
        self.setPixmap(pic)
class  BasePlayer(QWidget):
    backSignal =pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.is_black = True
        self.setWindowIcon(QIcon("photos/icon.ico"))
        self.setWindowTitle("五子棋-pa1806")
        self.setFixedSize(760, 650)
    def setup_ui(self):
        self.setFixedSize(760,650)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("photos/游戏界面.png")))
        self.setPalette(palette)

        self.back_btn=TDPushButton("photos/返回按钮_normal.png","photos/返回按钮_hover.png","photos/返回按钮_press.png",self)
        self.back_btn.clicked.connect(self.back)
        self.restart_btn=TDPushButton("photos/开始按钮_normal.png","photos/开始按钮_hover.png","photos/开始按钮_press.png",self)
        self.lose_btn=TDPushButton("photos/认输按钮_normal.png","photos/认输按钮_hover.png","photos/认输按钮_press.png",self)
        self.huiqi_btn=TDPushButton("photos/悔棋按钮_normal.png","photos/悔棋按钮_hover.png","photos/悔棋按钮_press.png",self)
        self.back_btn.move(680,10)
        self.restart_btn.move(640,210)
        self.lose_btn.move(640,290)
        self.huiqi_btn.move(640,380)
    def back(self):
        #关闭本窗体，告诉别人我要返回
        #发射自定信号
        self.backSignal.emit()
        self.close()

def is_win(chessboard):
    #判断棋盘上是否有玩家胜利
    #param chessboard 19x19 举证
    #return 返回胜利者
    for y in range(0,19):
        for x in range(0,19):
            if chessboard[x][y] is None:
                continue
            #不为空
            #右
            try:
                if chessboard[x+1][y] is not None:
                    if chessboard[x][y].color ==chessboard[x+1][y].color:
                        if chessboard[x + 2][y] is not None:
                            if chessboard[x][y].color ==chessboard[x+2][y].color:
                                if chessboard[x + 3][y] is  not None:
                                    if chessboard[x][y].color ==chessboard[x+3][y].color:
                                        if chessboard[x + 4][y] is  not None:
                                            if chessboard[x][y].color ==chessboard[x+4][y].color:
                                                return chessboard[x][y].color
            except IndexError:
                pass
            #下
            try:
                if chessboard[x][y+1] is not None:
                    if chessboard[x][y].color ==chessboard[x][y+1].color:
                        if chessboard[x ][y+2] is not None:
                            if chessboard[x][y].color ==chessboard[x][y+2].color:
                                if chessboard[x ][y+3] is not None:
                                    if chessboard[x][y].color ==chessboard[x][y+3].color:
                                        if chessboard[x][y+4] is  not None:
                                            if chessboard[x][y].color ==chessboard[x][y+4].color:
                                                return chessboard[x][y].color
            except IndexError:
                pass
            #左下
            try:
                if chessboard[x -1][y+1] is not None:
                    if chessboard[x][y].color == chessboard[x-1][y + 1].color:
                        if chessboard[x - 2][y + 2] is not None:
                            if chessboard[x][y].color == chessboard[x-2][y + 2].color:
                                if chessboard[x - 3][y + 3] is  not None:
                                    if chessboard[x][y].color == chessboard[x-3][y + 3].color:
                                        if chessboard[x - 4][y + 4] is not None:
                                            if chessboard[x][y].color == chessboard[x-4][y + 4].color:
                                                return chessboard[x][y].color
            except IndexError:
                pass
            #右下
            try:
                if chessboard[x + 1][y + 1] is not None:
                    if chessboard[x][y].color == chessboard[x+1][y + 1].color:
                        if chessboard[x + 2][y + 2] is not None:
                            if chessboard[x][y].color == chessboard[x+2][y + 2].color:
                                if chessboard[x + 3][y + 3] is not None:
                                    if chessboard[x][y].color == chessboard[x+3][y + 3].color:
                                        if chessboard[x + 4][y + 4] is not None:
                                            if chessboard[x][y].color == chessboard[x+4][y + 4].color:
                                                return chessboard[x][y].color
            except IndexError:
                pass
    return False #
    # def closeEvent(self, a0: QtGui.QCloseEvent):
    #     pass