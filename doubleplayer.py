from base import BasePlayer,Chess,is_win
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox,QLabel
#生成逻辑棋盘
#chessboard=[[None for i in range(0,19)] for j in range(0,19)]
class DoublePlayer(BasePlayer):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.is_black=True
        self.chessboard=chessboard=[[None for i in range(0,19)] for j in range(0,19)]
        self.is_over=True
        self.restart_btn.clicked.connect(self.restart)
        self.win_label=None
        self.huiqi_btn.clicked.connect(self.huiqi)
        self.lose_btn.clicked.connect(self.lose)
        self.history=[]
    def restart(self):
        self.is_over=False
        if self.win_label is not None:
            self.win_label.close()
        for i in range(19):
            for j in range(19):
                if self.chessboard[j][i] is not None:
                    self.chessboard[j][i].close()
                    self.chessboard[j][i]=None
    def huiqi(self):

        if self.is_over:
            return
        a = self.history.pop()
        xx = a[0]
        yy = a[1]
        if self.chessboard[xx][yy] is not None:
            self.chessboard[xx][yy].close()
            self.chessboard[xx][yy] = None

            self.is_black = not self.is_black

    def lose(self):
        if  self.is_over:
            return
        xx = self.history[::-1][0][0]
        yy = self.history[::-1][0][1]
        self.win_label = QLabel(self)
        if self.chessboard[xx][yy].color == 'b':
            pic = QPixmap("photos/黑棋胜利.png")
        else:
            pic = QPixmap("photos/白棋胜利.png")
        self.win_label.setPixmap(pic)
        self.win_label.move(100, 100)
        self.win_label.show()
        self.is_over = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.is_over:
            return
        if a0.x() <40 or a0.x()>600:
            return
        if a0.y()<40 or a0.y()>600:
            return
        if self.is_black:
            self.chess=Chess(color='b',parent=self)
        else:
            self.chess = Chess(color='w', parent=self)
        #self.is_black=not self.is_black
        if (a0.x()-50)%30<=15:
            x=(a0.x()-50)//30*30+50
        else:
            x=((a0.x()-50)//30+1)*30+50
        if (a0.y() - 50) % 30 <= 15:
            y = (a0.y()-50) // 30 * 30 + 50
        else:
            y = ((a0.y() - 50) // 30 + 1) * 30 + 50
        xx =(x-50)//30
        yy =(y-50)//30


        if self.chessboard[xx][yy] is not None:
            return
        self.chessboard[xx][yy]=self.chess
        self.history.append([xx, yy])

        x=x-self.chess.width()/2
        y=y-self.chess.height()/2
        self.chess.move(x,y)
        self.chess.show()
        self.is_black = not self.is_black
        color = is_win(self.chessboard)

        if color  is False:
            return
        else:
            #QMessageBox.information(self,"消息","{}棋胜利".format(color))
            self.win_label =QLabel(self)
            if color=='b':
                pic =QPixmap("photos/黑棋胜利.png")
            else:
                pic = QPixmap("photos/白棋胜利.png")
            self.win_label.setPixmap(pic)
            self.win_label.move(100,100)
            self.win_label.show()
            self.is_over=True