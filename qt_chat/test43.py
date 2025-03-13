import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMenu, QAction, QWidgetAction, QPushButton, QHBoxLayout, QActionGroup, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QSize


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.player_menu = CustomMenu(self)
        self.player_menu.setMinimumWidth(220)

        # 歌曲名称菜单项
        self.song_name_action = QAction("凡人修仙传", self)
        self.song_name_action.setIcon(QIcon("cut.png"))

        # 播放控制菜单项
        self.play_widget_action = QWidgetAction(self)
        self.play_widget = QWidget(self)
        self.play_back_button = QPushButton(self)
        self.play_back_button.setObjectName("PlayerButton")
        self.play_back_button.setIcon(QIcon("cut.png"))
        self.play_back_button.setIconSize(QSize(32, 32))

        self.play_button = QPushButton(self)
        self.play_button.setObjectName("PlayerButton")
        self.play_button.setIcon(QIcon("cut.png"))
        self.play_button.setIconSize(QSize(32, 32))

        self.play_forward_button = QPushButton(self)
        self.play_forward_button.setObjectName("PlayerButton")
        self.play_forward_button.setIcon(QIcon("cut.png"))
        self.play_forward_button.setIconSize(QSize(32, 32))

        self.h_layout = QHBoxLayout(self.play_widget)
        self.h_layout.addWidget(self.play_back_button)
        self.h_layout.addWidget(self.play_button)
        self.h_layout.addWidget(self.play_forward_button)
        self.play_widget_action.setDefaultWidget(self.play_widget)

        # 播放顺序子菜单
        self.play_procedure_action = QAction("顺序播放", self)
        self.play_procedure_action.setIcon(QIcon("cut.png"))
        self.procedure_menu = CustomMenu(self)
        self.procedure_menu.setMinimumWidth(150)

        self.list_cycle_action = QAction("列表循环", self)
        self.list_cycle_action.setIcon(QIcon("cut.png"))
        self.list_cycle_action.setCheckable(True)
        self.list_cycle_action.setChecked(False)

        self.single_cycle_action = QAction("单曲循环", self)
        self.single_cycle_action.setIcon(QIcon("cut.png"))
        self.single_cycle_action.setCheckable(True)
        self.single_cycle_action.setChecked(False)

        self.random_play_action = QAction("随机播放", self)
        self.random_play_action.setIcon(QIcon("cut.png"))
        self.random_play_action.setCheckable(True)
        self.random_play_action.setChecked(False)

        self.order_play_action = QAction("顺序播放", self)
        self.order_play_action.setIcon(QIcon("cut.png"))
        self.order_play_action.setCheckable(True)
        self.order_play_action.setChecked(True)

        self.procedure_action_group = QActionGroup(self)
        self.procedure_action_group.setExclusive(True)
        self.procedure_action_group.addAction(self.list_cycle_action)
        self.procedure_action_group.addAction(self.single_cycle_action)
        self.procedure_action_group.addAction(self.random_play_action)
        self.procedure_action_group.addAction(self.order_play_action)

        self.procedure_menu.addAction(self.list_cycle_action)
        self.procedure_menu.addAction(self.single_cycle_action)
        self.procedure_menu.addAction(self.random_play_action)
        self.procedure_menu.addAction(self.order_play_action)
        self.play_procedure_action.setMenu(self.procedure_menu)

        # 其他菜单项
        self.favorite_action = QAction("喜欢", self)
        self.favorite_action.setIcon(QIcon("cut.png"))
        self.settings_action = QAction("设置", self)
        self.settings_action.setIcon(QIcon("cut.png"))
        self.exit_action = QAction("退出", self)
        self.exit_action.setIcon(QIcon("cut.png"))

        # 添加菜单项到主菜单
        self.player_menu.addAction(self.song_name_action)
        self.player_menu.addSeparator()
        self.player_menu.addAction(self.play_widget_action)
        self.player_menu.addSeparator()
        self.player_menu.addAction(self.play_procedure_action)
        self.player_menu.addSeparator()
        self.player_menu.addAction(self.favorite_action)
        self.player_menu.addAction(self.settings_action)
        self.player_menu.addAction(self.exit_action)

        # 设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.slot_context_menu_requested)
        self.setMinimumSize(600, 500)

    def slot_context_menu_requested(self, pos: QPoint):
        self.player_menu.exec(self.mapToGlobal(pos))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    """ # 加载样式表
    with open(":/Resource/DefaultTheme", "r") as style_file:
        app.setStyleSheet(style_file.read()) """
    app.setStyleSheet('''
    * {
        outline: none;
    }

    QDialog {
        background: #D6DBE9;
    }

    QMenu {
        border: 1px solid #CCCCCC; /* 边框宽度为1px，颜色为#CCCCCC */
        border-radius: 5px; /* 边框圆角 */
        background-color: #FAFAFC; /* 背景颜色 */
        font-size: 10pt; /* 文本字体大小 */
        font-family: "Microsoft YaHei"; /* 文本字体族 */
        padding: 5px 0px 5px 0px; /* 菜单项距菜单顶部边界和底部边界分别有5px */
    }

    QMenu::item { /* 菜单子控件item，为菜单项在default的状态 */
        border: 0px solid transparent;
        background-color: transparent;
        color: black; /* 文本颜色 */
        min-height: 40px; /* 菜单项的最小高度 */
        margin: 2px 5px 2px 10px; /* 菜单项距其上下菜单项分别有2px，距菜单左右边界分别有10px和5px */
        /*padding: 0px 0px 0px 25px;*/ /* 也可使用padding定义菜单项与上下左右的距离 */
    }

    QMenu::item:selected { /* 为菜单项在selected的状态 */
        background-color: #EDEDEF;
    }

    QMenu::item:disabled{ /* 为菜单项在disabled的状态 */
        color: #CCCCCC;
        background: none;
    }

    QMenu::separator { /* 菜单子控件separator，定义菜单项之间的分隔线 */
        height: 1px;
        background: #CCCCCC;
        margin-left: 2px; /* 距离菜单左边界2px */
        margin-right: 2px; /* 距离菜单右边界2px */
    }

    QMenu::right-arrow { /* 菜单子控件right-arrow，定义子菜单指示器 */
        width: 24px;
        height: 24px;
        image: url(:/Resource/right_arrow);
    }

    QMenu::left-arrow { /* 菜单子控件left-arrow，定义子菜单指示器 */
        width: 24px;
        height: 24px;
        image: url(:/Resource/left_arrow);
    }

    /*
    QMenu::icon:checked {
        border: none;
        background-color: transparent;
        position: absolute;
        width: 24px;
        height: 24px;
    }*/

    QMenu::item::indicator { /* 菜单项子控件indicator，定义菜单项在选中状态下的指示器 */
        width: 24px;
        height: 24px;
    }

    QMenu::item::indicator:unchecked { /* 定义菜单项未选中的状态 */
        image: none;
    }

    QMenu::item::indicator:checked { /* 定义菜单项选中的状态 */
        image: url(:/Resource/checkebox);
    }

    QPushButton#PlayerButton { /* 自定义菜单项中的按钮 */
        border: none;
        background-color: transparent;
    }

    QPushButton#PlayerButton:hover {
        padding-top: 2px;
        padding-left: 2px;
    }

    QPushButton#PlayerButton:pressed {
        padding: 0px;
    }
    ''')

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
