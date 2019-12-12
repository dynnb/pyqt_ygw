from ui import *
import pymongo
import sip


def search_onclicked():
    global result_list
    query_list = []

    # 关键字
    keywords = ygw.keywords_lineEdit.text()
    if len(keywords):
        query_list.append({"$or":[{'desc_nw':{'$regex': keywords}},{'name':{'$regex': keywords}}]})

    # 稀有度
    rare = ygw.rare_combo.currentText()
    if rare != "全部卡片":
        pass

    # 等级
    level_range = ygw.level_lineEdit.text()
    if len(level_range):
        query_list.append({"$and":[{'level':{'$gte': level_range.split('-')[0]}},{'level':{'$lte': level_range.split('-')[-1]}}]})

    # 刻度
    degree_range = ygw.degree_lineEdit.text()
    if len(degree_range):
        query_list.append({"$and":[{'level':{'$gte': degree_range.split('-')[0]}},{'level':{'$lte': degree_range.split('-')[-1]}}]})

    # 攻击
    attack_range = ygw.attack_lineEdit.text()
    if len(attack_range):
        query_list.append({"$and":[{'atk':{'$gte': attack_range.split('-')[0]}},{'atk':{'$lte': attack_range.split('-')[-1]}}]})

    #防御
    defence_range = ygw.defence_lineEdit.text()
    if len(defence_range):
        query_list.append({"$and":[{'def':{'$gte': defence_range.split('-')[0]}},{'def':{'$lte': defence_range.split('-')[-1]}}]})

    # link值
    link_range = ygw.link_lineEdit.text()
    if len(link_range):
        query_list.append({"$and":[{'link':{'$gte': link_range.split('-')[0]}},{'link':{'$lte': link_range.split('-')[-1]}}]})

    # 属性
    # attribute = ygw.attribute
    attribute = ygw.attribute
    if attribute != "无":
        query_list.append({'attribute': attribute})

    # 种族
    race = ygw.race
    if race != "无":
        query_list.append({'race': race})

    # 魔法或陷阱种类
    card_type2 = ygw.card_type2
    if card_type2 != "无":
        query_list.append({'type_st':{'$regex': card_type2}})

    # 其他
    other_keywords = ygw.other_keywords
    if other_keywords != "无":
        query_list.append({"$or":[{'type_st':{'$regex': other_keywords}},{'desc':{'$regex': other_keywords}}]})

    if len(query_list):
        result_list = list(collection.find({"$and": query_list}))
    else:
        result_list = list(collection.find())

    update_result(result_list)


def card_type_select():
    global result_list
    
    card_type = ygw.card_type_combo.currentText()
    # 初始化所有变量
    ygw._init_data()

    ygw.keywords_lineEdit.setText('')
    # ygw.rare_combo.setCurrentIndex(0)  
    ygw.type_middle_list[0].setChecked(True)
    ygw.level_lineEdit.setText('')
    ygw.degree_lineEdit.setText('')
    ygw.attack_lineEdit.setText('')
    ygw.defence_lineEdit.setText('')
    ygw.link_lineEdit.setText('')
    ygw.attr_middle_list[0].setChecked(True)
    ygw.race_middle_list[0].setChecked(True)
    ygw.other_middle_list[0].setChecked(True)

    if card_type == "全部卡片":
        result_list = list(collection.find())
        update_result(result_list)
        ygw.magic_window.setHidden(False)
        ygw.monster_window.setHidden(False)
        ygw.attribute_window.setHidden(False)
        ygw.race_window.setHidden(False)
        ygw.other_window.setHidden(False)

    elif card_type == "怪兽":
        query = {'type_st':{'$regex': "怪兽"}}
        result_list = list(collection.find(query))
        update_result(result_list)

        ygw.magic_window.setHidden(True)
        ygw.monster_window.setHidden(False)
        ygw.attribute_window.setHidden(False)
        ygw.race_window.setHidden(False)
        ygw.other_window.setHidden(False) 
    else:
        query = {'type_st':{'$regex': card_type}}
        result_list = list(collection.find(query))
        update_result(result_list)
        ygw.magic_window.setHidden(False)
        ygw.monster_window.setHidden(True)
        ygw.attribute_window.setHidden(True)
        ygw.race_window.setHidden(True)
        ygw.other_window.setHidden(True)

def init_show_card_info_window():
    ygw.right_layout.removeWidget(ygw.show_card_info_window)
    sip.delete(ygw.show_card_info_window)

def update_result(result_list):
    print(len(result_list))
    ygw.right_layout.removeWidget(ygw.result_top_left)
    sip.delete(ygw.result_top_left)
    ygw.right_layout.removeWidget(ygw.result_top_right)
    sip.delete(ygw.result_top_right)

    init_show_card_info_window()

    ygw._create_right_window()
    ygw._create_card_info_window()
    show_card_list(result_list)
    if len(result_list):
        card = result_list[0]
    else:
        return
    show_card_img(card)
    show_card_info(card)

def card_clicked(index):
    ind = index.row()
    card = result_list[ind]
    show_card_img(card)
    init_show_card_info_window()
    ygw._create_card_info_window()
    show_card_info(card)

def show_card_img(card):
    ygw.result_top_right.setPixmap(QPixmap("data/card_icon/{}.jpg".format(card['name_nw'])))


def show_card_list(result_list):
    # ##################搜索出的卡片列表
    card_list_widget = QListWidget(ygw.result_top_left)
    card_list_widget.setCurrentRow(0)
    for result in result_list:
        card_list_widget.addItem(result['name_nw'])
    card_list_widget.clicked.connect(lambda index:card_clicked(index))
    card_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    ygw.result_top_left_layout.addWidget(card_list_widget)

def show_card_info(card):

    name_cn_key = QLabel(ygw.show_card_info_window,text = "中文名")
    ygw.info_layout.addWidget(name_cn_key, 0,0,1,1)
    name_cn_value = QLabel(ygw.show_card_info_window, text=card['name_nw'])
    ygw.info_layout.addWidget(name_cn_value, 0,1,1,5)

    name_ja_key = QLabel(ygw.show_card_info_window,text = "日文名")
    ygw.info_layout.addWidget(name_ja_key, 1,0,1,1)
    name_ja_value = QLabel(ygw.show_card_info_window, text=card['name_ja'])
    ygw.info_layout.addWidget(name_ja_value, 1,1,1,5)

    name_en_key = QLabel(ygw.show_card_info_window,text = "英文名")
    ygw.info_layout.addWidget(name_en_key, 2,0,1,1)
    name_en_value = QLabel(ygw.show_card_info_window, text=card['name_en'])
    ygw.info_layout.addWidget(name_en_value, 2,1,1,5)

    type_key = QLabel(ygw.show_card_info_window,text = "卡片种类")
    ygw.info_layout.addWidget(type_key, 3,0,1,1)
    type_value = QLabel(ygw.show_card_info_window, text=card['type_st'])
    ygw.info_layout.addWidget(type_value, 3,1,1,5)

    password_key = QLabel(ygw.show_card_info_window,text = "卡片密码")
    ygw.info_layout.addWidget(password_key, 4,0,1,1)
    password_value = QLabel(ygw.show_card_info_window, text=card['password'])
    ygw.info_layout.addWidget(password_value, 4,1,1,5)

    rare_key = QLabel(ygw.show_card_info_window,text = "稀有度")
    ygw.info_layout.addWidget(rare_key, 5,0,1,1)
    rare_value = QLabel(ygw.show_card_info_window, text=card['rare'])
    ygw.info_layout.addWidget(rare_value, 5,1,1,5)

    desc_key = QLabel(ygw.show_card_info_window,text = "效果")
    ygw.info_layout.addWidget(desc_key, 8,0,1,6)
    desc_value = QLabel(ygw.show_card_info_window, text=card['desc_nw'])
    desc_value.setWordWrap(True)
    ygw.info_layout.addWidget(desc_value, 9,0,12,6)

    if "怪兽" in card['type_st']:
        if "连接" not in card['type_st']:
            race_key = QLabel(ygw.show_card_info_window,text = "种族")
            ygw.info_layout.addWidget(race_key, 6,0,1,1)
            race_value = QLabel(ygw.show_card_info_window, text=card['race'])
            ygw.info_layout.addWidget(race_value, 6,1,1,1)

            attribute_key = QLabel(ygw.show_card_info_window,text = "属性")
            ygw.info_layout.addWidget(attribute_key, 6,2,1,1)
            attribute_value = QLabel(ygw.show_card_info_window, text=card['attribute'])
            ygw.info_layout.addWidget(attribute_value, 6,3,1,1)

            if "XYZ" not in card['type_st']:
                level_key = QLabel(ygw.show_card_info_window,text = "星级")
            else:
                level_key = QLabel(ygw.show_card_info_window,text = "阶级")
            ygw.info_layout.addWidget(level_key, 6,4,1,1)
            level_value = QLabel(ygw.show_card_info_window, text=card['level'])
            ygw.info_layout.addWidget(level_value, 6,5,1,1)

            atk_key = QLabel(ygw.show_card_info_window,text = "攻击")
            ygw.info_layout.addWidget(atk_key, 7,0,1,1)
            atk_value = QLabel(ygw.show_card_info_window,text=card["atk"])
            ygw.info_layout.addWidget(atk_value, 7,1,1,2)

            def_key = QLabel(ygw.show_card_info_window,text = "防御")
            ygw.info_layout.addWidget(def_key, 7,3,1,1)
            def_value = QLabel(ygw.show_card_info_window,text=card["def"])
            ygw.info_layout.addWidget(def_value, 7,4,1,2)
        else:
            race_key = QLabel(ygw.show_card_info_window,text = "种族")
            ygw.info_layout.addWidget(race_key, 6,0,1,1)
            race_value = QLabel(ygw.show_card_info_window, text=card['race'])
            ygw.info_layout.addWidget(race_value, 6,1,1,2)

            attribute_key = QLabel(ygw.show_card_info_window,text = "属性")
            ygw.info_layout.addWidget(attribute_key, 6,3,1,1)
            attribute_value = QLabel(ygw.show_card_info_window, text=card['attribute'])
            ygw.info_layout.addWidget(attribute_value, 6,4,1,2)

            atk_key = QLabel(ygw.show_card_info_window,text = "攻击")
            ygw.info_layout.addWidget(atk_key, 7,0,1,1)
            atk_value = QLabel(ygw.show_card_info_window,text=card["atk"])
            ygw.info_layout.addWidget(atk_value, 7,1,1,2)

            link_key = QLabel(ygw.show_card_info_window,text = "link值")
            ygw.info_layout.addWidget(link_key, 7,3,1,1)
            link_value = QLabel(ygw.show_card_info_window,text=card["link"])
            ygw.info_layout.addWidget(link_value, 7,4,1,2)
if __name__ == '__main__':
    global collection
    global ygw
    # 连接数据库
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['crawl_db']
    collection = db['OCG_cards']

    app = QApplication(sys.argv)
    ygw = Ygw()
    ygw.setWindowOpacity(1)
    ygw.setGeometry(0, 0, 0, 0)

    result_list = list(collection.find())
    update_result(result_list)
    # 绑定card_type_combo
    ygw.card_type_combo.currentIndexChanged.connect(card_type_select)
    # 绑定搜索按钮
    ygw.search_button.clicked.connect(search_onclicked)
    ygw.show()
    sys.exit(app.exec_())