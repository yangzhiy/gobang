
from base import BasePlayer,Chess,is_win
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox,QLabel
import random

class SingPlayer(BasePlayer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_black = True
        self.chessboard = chessboard = [[None for i in range(0, 19)] for j in range(0, 19)]
        self.is_over = True
        self.restart_btn.clicked.connect(self.restart)
        self.win_label = None
        self.huiqi_btn.clicked.connect(self.huiqi)
        self.lose_btn.clicked.connect(self.lose)
        self.num = []

    def restart(self):
        self.is_over = False
        if self.win_label is not None:
            self.win_label.close()
        for i in range(19):
            for j in range(19):
                if self.chessboard[j][i] is not None:
                    self.chessboard[j][i].close()
                    self.chessboard[j][i] = None

    def huiqi(self):
        if  self.is_over:
            return
        a = self.num.pop()
        xx = a[0]
        yy = a[1]
        if self.chessboard[xx][yy] is not None:
            self.chessboard[xx][yy].close()
            self.chessboard[xx][yy] = None
        a = self.num.pop()
        xx = a[0]
        yy = a[1]
        if self.chessboard[xx][yy] is not None:
            self.chessboard[xx][yy].close()
            self.chessboard[xx][yy] = None

    def lose(self):
        if  self.is_over:
            return
        xx = self.num[::-1][0][0]
        yy = self.num[::-1][0][1]
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
        if a0.x() < 40 or a0.x() > 600:
            return
        if a0.y() < 40 or a0.y() > 600:
            return
        if self.is_black:
            self.chess = Chess(color='b', parent=self)
        else:
            self.chess = Chess(color='w', parent=self)
        self.is_black = not self.is_black
        if (a0.x() - 50) % 30 <= 15:
            x = (a0.x() - 50) // 30 * 30 + 50
        else:
            x = ((a0.x() - 50) // 30 + 1) * 30 + 50
        if (a0.y() - 50) % 30 <= 15:
            y = (a0.y() - 50) // 30 * 30 + 50
        else:
            y = ((a0.y() - 50) // 30 + 1) * 30 + 50
        xx = (x - 50) // 30
        yy = (y - 50) // 30

        #self.num.append([xx, yy])
        if self.chessboard[xx][yy] is not None:
            return
        self.chessboard[xx][yy] = self.chess
        self.num.append([xx,yy])

        x = x - self.chess.width() / 2
        y = y - self.chess.height() / 2
        self.chess.move(x, y)
        self.chess.show()
        color = is_win(self.chessboard)

        if color is False:
           pass
        else:
            # QMessageBox.information(self,"消息","{}棋胜利".format(color))
            self.win_label = QLabel(self)
            if color == 'b':
                pic = QPixmap("photos/黑棋胜利.png")
            else:
                pic = QPixmap("photos/白棋胜利.png")
            self.win_label.setPixmap(pic)
            self.win_label.move(100, 100)
            self.win_label.show()
            self.is_over = True
        self.auto_run()

#判断完胜负，计算机落子
    def auto_run(self):
    #分别保存计算机白子和黑子的分数
        score_c = [[0 for i in range(0,19)]for j in range(0,19)]
        score_p = [[0 for i in range(0,19)] for j in range(0,19)]
        for j in range(0,19):
            for i in range(0,19):
                if self.chessboard[i][j] is not None:
                    continue #如果有棋子，继续下一个点
            #假设下黑棋的分数
                self.chessboard[i][j]=Chess('b',self)
                score_c[i][j]+=self.score(i,j,'b')
            #假设下白棋的分数
                self.chessboard[i][j] = Chess('w', self)
                score_p[i][j] += self.score(i, j, 'w')
            #恢复棋盘为空
                self.chessboard[i][j]=None
        r_score_c=[]
        r_score_p =[]
        for item in score_c:
            r_score_c+=item
        for item in score_p:
            r_score_p+=item
            #最终分数，去两者中最大的，然后将取值合并成为一个数组
        result=[max(a,b) for a,b in zip(r_score_c,r_score_p)]
        #取出最大值点的下标
        chess_index=result.index(max(result))
        #通过下标计算出落子的位置，
        xx= chess_index//19
        yy= chess_index%19


    #计算机执行落子函数
        if self.is_black:
            self.chess =Chess('b',self)
        else:
            self.chess =Chess('w',self)

        x =xx *30 +50-15
        y =yy*30+50-15
        self.chess.move(x,y)
        self.chess.show()
        self.chessboard[xx][yy] =self.chess
        self.num.append((xx,yy))
        self.is_black =not self.is_black
        color = is_win(self.chessboard)
        if color is False:
            pass
        else:

            self.win_label = QLabel(self)
            if color == 'b':
                pic = QPixmap("photos/黑棋胜利.png")
            else:
                pic = QPixmap("photos/白棋胜利.png")
            self.win_label.setPixmap(pic)
            self.win_label.move(100, 100)
            self.win_label.show()
            self.is_over = True

    def score( self,x,y,color):
        #计算如果在x,y这个点下color颜色的棋子，会的多少分
        blank_score=[0,0,0,0]
        chess_score=[0,0,0,0]
        #右方向

        for i in range(x,x+5):
            if i >=19:
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color==color:
                #如果是相同点，同色点分数加1
                    chess_score[0] +=1
                #朝同一方向进行，美遇到相同的颜色，加1
                else:
                    break
            else:
                blank_score[0]+= 1
                break


        for i in range(x-1, x -5,-1):
            if i <= 0:
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color == color:
                    # 如果是相同点，同色点分数加1
                    chess_score[0] += 1
        # 朝同一方向进行，美遇到相同的颜色，加1
                else:
                    break
            else:
                blank_score[0] += 1
                break
            #下方向
        for j in range(y,y+5):
            if j >=19:
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color==color:
                    chess_score[1]+=1
                else:
                    break
            else:
                blank_score[1]+=1
                break
            #上方向
        for j in range(y-1,y-5,-1):
            if j <= 0:
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color==color:
                    chess_score[1]+=1
                else:
                    break
            else:
                blank_score[1]+=1
                break
                #右下方向
        j = y
        for i in range(x,x+5):
            if i>=19 or j>=19:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color==color:
                    chess_score[2] +=1
                else:
                    break
            else:
                blank_score[2]+=1
                break
            j+=1
                #左上
        j =y-1
        for i in range(x-1,x-5,-1):
            if i<=0 or j<=0:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color==color:
                    chess_score[2]+=1
                else:
                    break
            else:
                blank_score[2]+=1
                break
            j -=1
        j = y
        for i in range(x , x - 5, -1):
            if i <= 0 or j >= 19:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j+=1
                    #右上
        j = y - 1
        for i in range(x + 1, x + 5):
            if i >=19 or j <= 0:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j-=1
                    #计算总分
        for score in chess_score:
            if score > 4:#如果某个方向超过4 ，则此处五子连珠
                return 100
        for i in range(0,len(blank_score)):
            if blank_score[i]==0:#说明在此方向上没有同色，也没有继续落子的地方
                blank_score[i] -= 20
                    #四个方向的分数胡，将两个列表一次相加
        result =[a+b for a,b in zip (chess_score,blank_score)]
        return max(result)#返回四个方向的最大值
