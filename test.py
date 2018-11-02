# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/8/29 11:08'

import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QCheckBox,QLineEdit,QListWidget,QListWidgetItem,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout #QGridLayout
from PyQt5 import QtGui

class Window(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("网络配置")
        self.resize(300,300)

        self.name_label = QLabel("昵称：",self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText("玩家0")

        self.h1 = QHBoxLayout()  # 生成布局管理器
        self.h1.addWidget(self.name_label,3)  # 把空间加入 管理器
        self.h1.addWidget(self.name_edit,7)

        self.player_label = QLabel("玩家列表：",self)
        self.refresh_btn = QPushButton("刷新",self)

        self.h2 = QHBoxLayout()  # 生成布局管理器
        self.h2.addWidget(self.player_label,5)  # 把空间加入 管理器
        self.h2.addWidget(self.refresh_btn,5)

        self.player_list = QListWidget(self)
        item1 = QListWidgetItem("条目1")
        item2 = QListWidgetItem("条目2")
        item3 = QListWidgetItem("条目3")
        self.player_list.addItem(item1)
        self.player_list.addItem(item2)
        self.player_list.addItem(item3)
        self.player_list.itemDoubleClicked.connect(self.item_clicked)

        self.join_btn = QPushButton("加入房间",self)
        self.battle_btn = QPushButton("选择对战",self)
        self.battle_btn.setEnabled(False)
        # 第三行的水平布局
        self.h3 = QHBoxLayout()
        self.h3.addWidget(self.join_btn)
        self.h3.addWidget(self.battle_btn)
        # 主布局，垂直布局 管理所有的布局
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.h1)
        self.main_layout.addLayout(self.h2)
        self.main_layout.addWidget(self.player_list)
        self.main_layout.addLayout(self.h3)

        self.setLayout(self.main_layout)  # 让窗体应用布局管理

    def item_clicked(self,item):
        print(item.text())

class Window2(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("五子棋")
        self.window_pale = QtGui.QPalette()
        self.window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("potot2.png")))
        self.setPalette(self.window_pale)
        self.is_click = False
        self.resize(580,520)
        self.btn1 = QPushButton("单人对战",self)
        self.btn1.move(210,310)
        self.btn1.resize(80, 40)
        self.btn1.setEnabled(True)
        self.btn2 = QPushButton("双人对战",self)
        self.btn2.move(210,350)
        self.btn2.resize(80, 40)
        self.btn2.setEnabled(True)
        self.btn3 = QPushButton("联机对战", self)
        self.btn3.move(210, 390)
        self.btn3.resize(80, 40)
        self.btn3.setEnabled(True)
        # 点击按钮 执行一个操作！
        self.btn1.clicked.connect(self.func3)
        # 界面跳转
        self.btn2.clicked.connect(self.func3)
        self.btn3.clicked.connect(self.func2)

    # def func(self, checked):
    #     print(checked)
    #         # print("enter the function")
    #     if not self.is_click:
    #         self.btn1.setText("1按钮")
    #         self.btn2.setEnabled(True)
    #     else:
    #         self.btn1.setText("按钮1")
    #         self.btn2.setEnabled(False)
    #         self.is_click = not self.is_click

    def func2(self):
            # 界面跳转， 把新窗体打开，把自己关掉
        self.w = Window()
        self.w.show()
        self.close()

    def func3(self):
        self.w = Window3()
        self.w.show()
        self.close()
class Window3(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("五子棋")
            self.window_pale = QtGui.QPalette()
            self.window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("photo1.png")))
            self.setPalette(self.window_pale)
            #self.is_click = False
            self.resize(580, 520)
            self.btn1 = QPushButton("开始", self)
            self.btn1.move(500, 180)
            self.btn1.resize(80, 40)
            self.btn2 = QPushButton("悔棋", self)
            self.btn2.move(500, 220)
            self.btn2.resize(80, 40)
            #self.btn2.setEnabled(False)
            self.btn3 = QPushButton("催促", self)
            self.btn3.move(500, 260)
            self.btn3.resize(80, 40)
            self.btn4 = QPushButton("退出", self)
            self.btn4.move(500, 300)
            self.btn4.resize(80, 40)
            # 点击按钮 执行一个操作！
            #self.btn1.clicked.connect(self.func)
            # 界面跳转
            self.btn4.clicked.connect(self.func3)

        def func2(self):
        # 界面跳转， 把新窗体打开，把自己关掉
            self.w = Window()
            self.w.show()
            self.close()
        def func3(self):
            self.w=Window2()
            self.w.show()
            self.close()
if __name__ == '__main__':
    # 创建Qt应用对象
    app = QApplication(sys.argv)
    w = Window2()
    w.show()
    # 进入消息循环
    sys.exit(app.exec_())
    #创建窗体
    # w = QWidget()
    # w.resize(400,400)#重设窗体大小
    # w.setFixedSize(400,400)#设置固定大小
    # w.setWindowTitle("酷炫的五子棋")#设置窗体标题
    # w.move(50,50)#移动
    # #按钮
    # btn = QPushButton(parent=w,text="按钮")#指定父控件
    # btn.move(100,100)
    # btn.setText("加入游戏")
    # #复选框
    # check1=QCheckBox(parent=w,text="111")
    # check2 = QCheckBox(parent=w, text="222")
    # check3 = QCheckBox(parent=w, text="333")
    # check1.move(150,100)
    # check2.move(200, 100)
    # check3.move(250, 100)
    # #输入框
    # edit =QLineEdit(parent=w)
    # edit.move(100,200)
    # edit.resize(200,30)
    # #列表窗体
    # list_widget=QListWidget(parent=w)
    # list_widget.move(100,250)
    # list_widget.resize(200,200)
    # iten1=QListWidgetItem("条目1")
    # iten2 = QListWidgetItem("条目2")
    # iten3 = QListWidgetItem("条目3")

    # list_widget.addItem(iten1)
    # list_widget.addItem(iten2)
    # list_widget.addItem(iten3)
    # btn.show()
    # w.show()
    # #进入消息循环
    sys.exit(app.exec_())