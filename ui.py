import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from config import *
class Ygw(QWidget):

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_data()
        # 组件透明度设置
        self.diaphaneity = QGraphicsOpacityEffect()  
        self.diaphaneity.setOpacity(0.5)
        # 样式设置
        QssTools.set_qss_to_obj('./ygw.qss', self)
        # obj为组件
        # obj.setGraphicsEffect(op)  
        # obj.setAutoFillBackground(True)        
        # 添加背景图片
        window_pale = QPalette() 
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./data/image/樱花屋.jpg"))) 
        self.setPalette(window_pale)

        self.left_layout =  QGridLayout(self.left)
        self.right_layout = QGridLayout(self.right)
        self._create_left_window()
        self._create_right_window()
        self._create_card_info_window()


    def _init_data(self):
        self.attribute = "无"
        self.race = "无"
        self.card_type2 = "无"
        self.other_keywords = "无"



    def _init_window(self):
        self.width =1024
        self.height=768
        self.setWindowTitle('游戏王查询器')
        self.resize(self.width,self.height)
        self.setFixedSize(self.width,self.height)
        # 左边窗口
        self.left = QFrame(self)
        self.left.resize(512,768)
        # 右边窗口
        self._init_right_window()
    def _init_right_window(self):
        self.right = QFrame(self)
        self.right.resize(self.width/2,self.height)
        main_window = QGridLayout(self)
        main_window.addWidget(self.left, 0, 0, 1, 1)
        main_window.addWidget(self.right, 0, 1, 1, 1)
  

    def rare_select(self):
        print("current item is {0}".format(self.rare_combo.currentText()))
    def _create_left_window(self):

        #######################关键字
        keywords_label=QLabel(self.left)
        keywords_label.setText("关键字")
        self.left_layout.addWidget(keywords_label, 0, 0, 1, 2)
        self.keywords_lineEdit = QLineEdit(self.left)

        # # 文本背景颜色设置
        # self.keywords_lineEdit.setStyleSheet("background-color:KEY_COLOR")
        # self.keywords_lineEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.left_layout.addWidget(self.keywords_lineEdit,0, 2, 1, 7)
         
        ########################卡片类型
        card_type_label=QLabel(self.left)
        card_type_label.setText("卡种")
        self.left_layout.addWidget(card_type_label, 1, 0, 1, 2)
        self.card_type_combo = QComboBox(self.left)

        crad_type_list = ["全部卡片","怪兽","魔法","陷阱"]
        for card_type in crad_type_list:
            self.card_type_combo.addItem(card_type)
        self.left_layout.addWidget(self.card_type_combo, 1, 4, 1, 3)
        

        #*****************************卡片稀有度
        rare_types_label=QLabel(self.left)
        rare_types_label.setText("稀有度")
        self.left_layout.addWidget(rare_types_label, 2, 0, 1, 2)
        self.rare_combo = QComboBox(self.left)

        rare_list = ["全部卡片","OCG独有","TCG独有","OT通用"]
        for rare in rare_list:
            self.rare_combo.addItem(rare)
        self.left_layout.addWidget(self.rare_combo, 2, 4, 1, 3)
        self.rare_combo.currentIndexChanged.connect(self.rare_select)

        #****************************魔法、陷阱
        self.magic_window = QFrame(self.left)
        self.left_layout.addWidget(self.magic_window,3,0,1,10)
        self.magic_layout = QGridLayout(self.magic_window)
        # 魔法/陷阱类型
        type_label=QLabel(self.magic_window)
        type_label.setText("类型")
        self.magic_layout.addWidget(type_label, 0, 0, 1, 1)

        type_list=["无" ,"装备","场地","速攻","仪式","永续","反击","通常"]
        self.type_middle_list= []
        for i in range(len(type_list)):
            self.type_bt = QRadioButton(type_list[i], self.magic_window)
            self.type_bt.clicked.connect(lambda: self.type_changed(self.sender().text()))
            self.type_middle_list.append(self.type_bt)
            self.magic_layout.addWidget(self.type_bt,0+i//8,2+i%8,1,1)
        self.type_middle_list[0].setChecked(True)

        #****************************monster
        self.monster_window = QFrame(self.left)
        self.left_layout.addWidget(self.monster_window,4,0,4,10)
        self.monster_layout = QGridLayout(self.monster_window)

        # 星阶
        level_label=QLabel(self.monster_window)
        level_label.setText("星阶")
        self.monster_layout.addWidget(level_label, 0, 0, 1, 1)

        self.level_lineEdit = QLineEdit(self.left)
        self.monster_layout.addWidget(self.level_lineEdit,0, 1, 1, 7)

        # 刻度
        degree_label=QLabel(self.monster_window)
        degree_label.setText("刻度")

        self.monster_layout.addWidget(degree_label, 1, 0, 1, 1)
        self.degree_lineEdit = QLineEdit(self.left)
        self.monster_layout.addWidget(self.degree_lineEdit,1, 1, 1, 7)

        # 攻击力
        attack_label=QLabel(self.monster_window)
        attack_label.setText("攻击力")
        self.monster_layout.addWidget(attack_label, 2, 0, 1, 1)

        self.attack_lineEdit = QLineEdit(self.left)
        self.monster_layout.addWidget(self.attack_lineEdit,2, 1, 1, 7)

        # 防御力
        defence_label=QLabel(self.monster_window)
        defence_label.setText("防御力")
        self.monster_layout.addWidget(defence_label, 3, 0, 1, 1)

        self.defence_lineEdit = QLineEdit(self.left)
        self.monster_layout.addWidget(self.defence_lineEdit,3, 1, 1, 7)

        # link值
        link_label=QLabel(self.monster_window)
        link_label.setText("link值")
        self.monster_layout.addWidget(link_label, 4, 0, 1, 1)

        self.link_lineEdit = QLineEdit(self.left)
        self.monster_layout.addWidget(self.link_lineEdit,4, 1, 1, 7)

        # 属性
        self.attribute_window = QFrame(self.left)
        self.left_layout.addWidget(self.attribute_window,8,0,1,10)
        self.attribute_layout = QGridLayout(self.attribute_window)

        attribute_label=QLabel(self.attribute_window)
        attribute_label.setText("属性")
        self.attribute_layout.addWidget(attribute_label, 0, 0, 1, 1)

        attribute_list=["无","光","地","暗","水","炎","神","风"]
        self.attr_middle_list= []
        for i in range(len(attribute_list)):
            self.attribute_bt = QRadioButton(attribute_list[i], self.attribute_window)
            self.attribute_bt.clicked.connect(lambda: self.attr_changed(self.sender().text()))

            self.attr_middle_list.append(self.attribute_bt)
            self.attribute_layout.addWidget(self.attribute_bt,0+i//8,1+i%8,1,1)
        self.attr_middle_list[0].setChecked(True)


        # 种族
        self.race_window = QFrame(self.left)
        self.left_layout.addWidget(self.race_window,9,0,4,10)
        self.race_layout = QGridLayout(self.race_window)

        race_label=QLabel(self.race_window)
        race_label.setText("种族")
        self.race_layout.addWidget(race_label, 0, 0, 1, 2)

        race_list=["无",'水','兽','兽战士','创造神','恐龙','幻神兽','龙','天使','恶魔','鱼','昆虫','机械','植物','念动力','炎','爬虫类','岩石','海龙','魔法师','雷','战士','鸟兽','不死','幻龙','电子界']
        self.race_middle_list= []
        for i in range(len(race_list)):
            self.race_bt = QRadioButton(race_list[i], self.race_window)
            self.race_bt.clicked.connect(lambda: self.race_changed(self.sender().text()))

            self.race_middle_list.append(self.race_bt)
            self.race_layout.addWidget(self.race_bt,0+i//7,2+i%7,1,1)
        self.race_middle_list[0].setChecked(True)

        # 其他
        self.other_window = QFrame(self.left)
        self.left_layout.addWidget(self.other_window,13,0,3,10)
        self.other_layout = QGridLayout(self.other_window)

        other_label=QLabel(self.race_window)
        other_label.setText("其他")
        self.other_layout.addWidget(other_label, 0, 0, 1, 2)

        other_list=["无",'通常','效果','仪式','融合','同调','XYZ','卡通','同盟','灵魂','调整','二重','灵摆','反转','特殊召唤','连接']
        self.other_middle_list= []
        for i in range(len(other_list)):
            self.other_bt = QRadioButton(other_list[i], self.other_window)
            self.other_bt.clicked.connect(lambda: self.other_keywords_changed(self.sender().text()))
            self.other_middle_list.append(self.other_bt)
            self.other_layout.addWidget(self.other_bt,0+i//8,2+i%8,1,1)
        self.other_middle_list[0].setChecked(True)

        #***************************搜索按钮
        self.search_button = QPushButton("搜索", self.left)
        self.left_layout.addWidget(self.search_button,16,4,1,1)

    def attr_changed(self, btnText):
        self.attribute = btnText
    def type_changed(self, btnText):
        self.card_type2 = btnText
    def race_changed(self, btnText):
        self.race = btnText
    def other_keywords_changed(self, btnText):
        self.other_keywords = btnText

    def _create_right_window(self):

        self.result_top_left = QFrame(self.right)
        self.result_top_left_layout = QHBoxLayout(self.result_top_left)

        self.result_top_right = QLabel(self.right)
        self.right_layout.addWidget(self.result_top_left,0,0,2,1)
        self.right_layout.addWidget(self.result_top_right,0,1,2,1)

    def _create_card_info_window(self):
        self.show_card_info_window = QFrame(self.right)
        self.show_card_info_window.setFrameShape(QFrame.StyledPanel)
        self.right_layout.addWidget(self.show_card_info_window,2,0,3,2)
        self.info_layout = QGridLayout(self.show_card_info_window)


