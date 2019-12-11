class QssTools(object):
    """
    定义一个读取样式的工具类
    """
    @classmethod
    def set_qss_to_obj(cls, file_path, obj):
        with open(file_path, 'r') as f:
            obj.setStyleSheet(f.read())


# 颜色参数
ORANGE1 = "#FFCC00"
ORANGE2 = "#FF9900"

YELLOW = "#FFFF00"
YELLOW2 = "#FF6633"

PINK = "#FF66FF"

GREEN1 = "#CCFF00"
GREEN2 = "#CCFF33"

LIME = "Lime"
LIGHTGREEN = "#33FF00"

PURPLE = "#CC00FF"
LIGHTPURPLE = "#6600FF"
