from base import BasePlayer
from base import TDPushButton ,Chess,is_win
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QLineEdit,QHBoxLayout,QVBoxLayout,QMessageBox
import socket
import threading
import json
import pygame
pygame.init()
#接收完整的数据帧
def recv_sockdata(the_socket):
    total_data = ""
    while True:

        data = the_socket.recv(1024).decode()
        if "END" in data:
            total_data += data[:data.index("END")]
            break
        total_data += data
    return total_data
#网络设置窗口
class NetworkConfig(QWidget):
    def __init__(self, main_window=None,parent=None):
        super().__init__(parent)
        #用一个变量保存主窗体
        self.main_window=main_window
        self.name_label=QLabel("昵称",self)
        self.name_edit =QLineEdit(self)
        self.name_edit.setText("玩家1")
        self.h1=QHBoxLayout()
        self.h1.addWidget(self.name_label,3)
        self.h1.addWidget(self.name_edit,7)
        self.ip_label = QLabel("主机ip", self)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.setText("127.0.0.1")
        self.h2 = QHBoxLayout()
        self.h2.addWidget(self.ip_label, 3)
        self.h2.addWidget(self.ip_edit, 7)
        self.con_btn = QPushButton("连接主机",self)
        self.ser_btn = QPushButton("我是主机", self)
        self.con_btn.clicked.connect(self.client_mode)
        self.ser_btn.clicked.connect(self.server_mode)
        self.h3 = QHBoxLayout()
        self.h3.addWidget(self.con_btn)
        self.h3.addWidget(self.ser_btn)
        self.v=QVBoxLayout()
        self.v.addLayout(self.h1)
        self.v.addLayout(self.h2)
        self.v.addLayout(self.h3)
        self.setLayout(self.v)
        self.game_window=None
    def client_mode(self):
        #启动客户端模式的程序
        self.game_window=NetworkClient(name=self.name_edit.text(),ip=self.ip_edit.text())
        self.game_window.show()
        self.game_window.backSignal.connect(self.main_window.back)
        self.close()
    def server_mode(self):
        #启动服务器模式的程序
        self.game_window = NetworkServer(name=self.name_edit.text())
        self.game_window.show()
        self.game_window.backSignal.connect(self.main_window.back)
        self.close()


class NetworkPlayer(BasePlayer):
    dataSignal =pyqtSignal(dict)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.tcp_socket =None
        self.chessboard = [[None for i in range(0,19)]for j in range(0,19)]
        self.history=[]
        self.dataSignal.connect(self.deal_data)
        self.restart_btn.clicked.connect(self.restart)
        self.lose_btn.clicked.connect(self.lose)
        self.huiqi_btn.clicked.connect(self.huiqi)
        self.is_over=True
        self.is_connect=True
        self.my_trun=True
        self.win_label=None

    def setup_ui(self):
        super().setup_ui()
        self.state_lable=QLabel("游戏状态",self)
        self.state_lable.move(660, 170)
        self.setWindowTitle('等待链接')
        self.cuicu_btn=TDPushButton("photos/催促按钮_normal.png","photos/催促按钮_hover.png","photos/催促按钮_press.png",self)
        self.cuicu_btn.show()
        self.cuicu_btn.move(640,460)
        self.cuicu_btn.clicked.connect(self.sound)
    def sound(self):
        self.tcp_socket.sendall((json.dumps({"msg":"sound"})+"END").encode())
        self.sound1()
    def sound1(self):
        sound = pygame.mixer.Sound("photos/cuicu.wav")
        sound.set_volume(1)
        sound.play()
    def deal_data(self,data):
        print(data)
        if data["msg"] == "name":
            name = data['data']
            title = '与' + name + '联机对战中'

            self.setWindowTitle(title)
            self.state_lable = QLabel("连接成功", self)
            self.state_lable.show()
            self.state_lable.move(660,200)


        if data["msg"] =="pos":#收到落子位置的代码
            pos = data['data']
            xx=pos[0]
            yy=pos[1]
            colors=pos[2]
            self.chess = Chess(color=colors, parent=self)
            self.is_black = not self.is_black
            self.my_trun = not self.my_trun

            if self.chessboard[xx][yy] is not None:
                return
            self.chessboard[xx][yy] = self.chess

            self.history.append((xx, yy))
            x = xx * 30 + 50 - 15
            y = yy * 30 + 50 - 15
            self.chess.move(x, y)
            self.state_text.setText("己方下棋")
            self.chess.show()
            sound = pygame.mixer.Sound("photos/luozisheng.wav")
            sound.set_volume(1)
            sound.play()
            color = is_win(self.chessboard)
            if color is False:
                return
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

        if  data['msg']=="error":
            QMessageBox.information(self,"消息","对方已退出游戏，联机异常，即将返回")
            self.backSignal.emit()
            self.close()
        if  data['msg']=="restart":
            question =QMessageBox.question(self,"消息","对方请求重新开始，是否同意",QMessageBox.Yes | QMessageBox.No)
            if question ==QMessageBox.Yes:
                self.restartyes()
                self.restart1()
                self.state_text.setText("己方下棋")
            if question ==QMessageBox.No:
                self.restartno()
        if  data['msg']=="restartyes":
            QMessageBox.information(self,"消息","对方已同意")
            self.restart1()
            self.state_text.setText("对方下棋")
        if  data['msg']=="restartno":
            QMessageBox.information(self,"消息","对方拒绝重新开始")
            #self.restartno()
        if  data["msg"] =="lose":
            QMessageBox.information(self,"消息","对方认输")
            self.lose1()
        if  data['msg']=="huiqi":
            hhuiqi=QMessageBox.question(self,"消息","请求悔棋",QMessageBox.Yes |QMessageBox.No)
            if hhuiqi ==QMessageBox.Yes:
                self.huiqiyes()
                self.huiqi1()
            if hhuiqi ==QMessageBox.No:
                self.huiqino()
        if  data["msg"] =="huiqiyes":
            QMessageBox.information(self,"消息","OK")
            self.huiqi1()
        if  data["msg"]=="huiqino":
            QMessageBox.information(self,"消息","对方不同意")
        if  data["msg"] =="sound":
            self.sound1()




    def recv_data(self,sock):
        #收到数据
        print("recv_data")
        while self.is_connect:
            try:
                r_data=recv_sockdata(sock)
            except ConnectionResetError as e:
                print(e)
                data = {"msg":"error","data":'disconnect'}
                self.dataSignal.emit(data)
                break
            except ConnectionAbortedError:
                pass
            data=json.loads(r_data)
            self.dataSignal.emit(data)
    def restart(self):
        self.tcp_socket.sendall((json.dumps({"msg":"restart"})+"END").encode())

    def restart1(self):
        self.is_over=False
        if self.win_label is not None:
            self.win_label.close()
        for i in range(19):
            for j in range(19):
                if self.chessboard[j][i] is not None:
                    self.chessboard[j][i].close()
                    self.chessboard[j][i] = None

    def restartyes(self):
        self.tcp_socket.sendall((json.dumps({"msg":"restartyes"})+"END").encode())
    def restartno(self):
        self.tcp_socket.sendall((json.dumps({"msg":"restartno"})+"END").encode())
    def lose(self):
        if self.is_over:
            return

        self.tcp_socket.sendall((json.dumps({"msg":"lose"})+"END").encode())
        self.lose1()
    def lose1(self):
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
    def huiqi(self):
        if self.is_over:
            return
        self.tcp_socket.sendall((json.dumps({"msg":"huiqi"})+"END").encode())

    def huiqi1(self):
        if  self.is_over:
            return
        a = self.history.pop()
        xx = a[0]
        yy = a[1]
        if self.chessboard[xx][yy] is not None:
            self.chessboard[xx][yy].close()
            self.chessboard[xx][yy] = None
            self.is_black = not self.is_black
            self.my_trun = not self.my_trun
    def huiqiyes(self):
        self.tcp_socket.sendall((json.dumps({"msg": "huiqiyes"}) + "END").encode())
    def huiqino(self):
        self.tcp_socket.sendall((json.dumps({"msg": "huiqino"}) + "END").encode())

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.is_over:
            return
        if not self.my_trun:
            return

        if a0.x() < 40 or a0.x() > 600:
            return
        if a0.y() < 40 or a0.y() > 600:
            return
            # 通过标识，决定棋子的颜色

        if self.is_black:
            self.chess = Chess(color='b',parent=self)
        else:
            self.chess = Chess('w',self)
            # 将棋子定位到准确的坐标点
        if (a0.x() - 50) % 30 <= 15:
            x = (a0.x() - 50) // 30 * 30 + 50
        else:
            x = ((a0.x() - 50) // 30 + 1) * 30 + 50

        if (a0.y() - 50) % 30 <= 15:
            y = (a0.y() - 50) // 30 * 30 + 50
        else:
            y = ((a0.y() - 50) // 30 + 1) * 30 + 50
            # 在棋盘数组中，保存棋子对象
        xx = (x - 50) // 30
        yy = (y - 50) // 30
        # 如果此处已经有棋子，点击失效
        if self.chessboard[xx][yy] is not None:
            return

        self.chessboard[xx][yy] = self.chess
        self.history.append([xx, yy])

        x = x - self.chess.width() / 2
        y = y - self.chess.height() / 2
        self.chess.move(x, y)
        self.state_text.setText("对方下棋")
        self.chess.show()
        sound = pygame.mixer.Sound("photos/luozisheng.wav")
        sound.set_volume(1)
        sound.play()

        #落子后发送棋子的位置
        if self.is_black:
            pos_data ={"msg":"pos","data":(xx,yy,"b")}
            self.tcp_socket.sendall((json.dumps(pos_data)+"END").encode())
        else:
            pos_data = {"msg": "pos", "data": (xx, yy, "w")}
            self.tcp_socket.sendall((json.dumps(pos_data) + "END").encode())
        self.is_black = not self.is_black
        self.my_trun = not self.my_trun
        color = is_win(self.chessboard)
        if color is False:
            return
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

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.is_connect =False
        self.tcp_socket.close()
        super().closeEvent(a0)

class NetworkServer(NetworkPlayer):
    def __init__(self,name="玩家1",parent=None):
        super().__init__(parent)
        self.name =name
        self.state_text = QLabel(self)
        self.state_text.setText("回合状态")
        self.state_text.show()
        self.state_text.move(660, 150)
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ser_socket.bind(("0.0.0.0", 3006))
        except OSError:
             QMessageBox.information(self,"消息","端口已经被占用，请重试")

        self.ser_socket.listen(8)
        th = threading.Thread(target=self.start_listen)
        th.start()

    def start_listen(self):
        print("start listening")
        while self.is_connect:
            sock, addr = self.ser_socket.accept()
            self.tcp_socket = sock
            # 发送了自己的昵称
            self.tcp_socket.sendall((json.dumps({"msg": "name", "data": self.name})+"END").encode())
            self.recv_data(self.tcp_socket)

class NetworkClient(NetworkPlayer):
   def __init__(self,name="玩家1",ip="127.0.0.1",parent=None):
       super().__init__(parent)
       self.name = name
       self.state_text = QLabel(self)
       self.state_text.setText("回合状态")
       self.state_text.show()
       self.state_text.move(660, 150)
       self.my_trun = False
       self.tcp_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       addr=(ip,3006)
       try:
           self.tcp_socket.connect(addr)
       except ConnectionRefusedError as b:
           print(b)
           QMessageBox.information(self,"消息","连接失败，请确定另一个设备已打开或重新连接")


       self.tcp_socket.sendall((json.dumps({"msg":"name","data":self.name})+"END").encode())
       th = threading.Thread(target=self.recv_data,args=(self.tcp_socket,))

       th.start()