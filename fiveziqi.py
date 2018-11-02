from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel
from PyQt5.QtGui import QPalette,QPixmap,QIcon,QBrush
import sys
import cgitb
cgitb.enable(format='error')
from base import BasePlayer
from singplayer import SingPlayer
from doubleplayer import DoublePlayer
from networkplayer import NetworkPlayer,NetworkConfig
from base import TDPushButton

class  GameStar(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        #设置窗体的图标
        self.setWindowIcon(QIcon("photos/icon.ico"))
        self.setWindowTitle("五子棋-pa1806")
        self.setFixedSize(760,650)
        #设置窗体大小
        palette =QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("photos/potot2.png")))
        self.setPalette((palette))
        #生成三个按钮
        self.single_btn= TDPushButton("photos/人机对战_normal.png","photos/人机对战_hover.png","photos/人机对战_press.png",self)
        self.double_btn = TDPushButton("photos/30.png","photos/31.png","photos/32.png",self)
        self.network_btn = TDPushButton("photos/联机对战_normal.png","photos/联机对战_hover.png","photos/联机对战_press.png",self)
        self.single_btn.move(250,300)
        self.double_btn.move(250, 400)
        self.network_btn.move(250, 500)
        #三个按钮绑定处理函数，处理函数中实现页面跳转
        self.single_btn.clicked.connect(self.single)
        self.double_btn.clicked.connect(self.double)
        self.network_btn.clicked.connect(self.network)
        self.game_window=None
    def single(self):
        self.game_window=SingPlayer()
        self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()
    def double(self):
        self.game_window = DoublePlayer()
        self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()
    def network(self):
        self.game_window = NetworkConfig(main_window=self)
        #self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()
    def back(self):
        self.show()
        #捕获到返回信号
        #设置窗体的标题
        #设置窗体的固定大小
        #设置窗体的背景
if __name__=="__main__":
    #启动窗口应用
    app= QApplication(sys.argv)
    w =GameStar()
    w.show()
    #启动游戏窗体
    sys.exit(app.exec_())