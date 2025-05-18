from module.logRecoder import MirrorChatLogger
from module.moduleLoader import load_module
from imports.MCmain import *
from pathlib import Path
import json

class PluginsFrame(QFrame):
    """插件中心框架"""
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PluginsFrame")
        
        self.vBoxLayout: QVBoxLayout
        self.titleLabel: SubtitleLabel
        self.scrollArea: SmoothScrollArea
        self.scrollWidget: QWidget
        self.scrollLayout: QVBoxLayout
        self.topSpacer: QSpacerItem
        
        # 加载界面
        load_module(self, [], "bin/gui/addon/interface/plugins_subinterface.mirc")
        
        # 加载插件信息
        self.loadPlugins()

        # 监听主题变化
        qconfig.themeChanged.connect(self.updateCardStyle)
    
    def loadPlugins(self):
        """加载插件信息"""
        addons_dir = Path("bin/addon")
        for addon_dir in addons_dir.iterdir():
            if addon_dir.is_dir():
                info_file = addon_dir / "addon_info.mrdat"
                if info_file.exists():
                    with open(info_file, "r", encoding="utf-8") as f:
                        info = json.load(f)
                    self.addPluginCard(info, addon_dir.name)

        self.updateCardStyle()

    def addPluginCard(self, info, addon_name):
        """添加插件卡片"""
        card = QFrame(self.scrollWidget)
        card.setObjectName("PluginCard")
        card.setFixedHeight(100)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setProperty("enabled", True)  # 添加启用状态属性

        layout = QHBoxLayout(card)
        # 减小整体内边距，这里把左边距调小
        layout.setContentsMargins(0, 5, 5, 5)  
        
        # 插件图标容器
        iconContainer = QFrame(card)
        iconContainer.setObjectName("IconContainer")
        iconContainer.setFixedSize(50, 50)
        iconLayout = QVBoxLayout(iconContainer)
        iconLayout.setContentsMargins(0, 0, 0, 0)
        
        # 插件图标
        icon = FluentIcon.APPLICATION
        iconLabel = QLabel(iconContainer)
        iconLabel.setPixmap(icon.icon().pixmap(32, 32))
        iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconLayout.addWidget(iconLabel)
        
        # 减小图标与左边的间距
        layout.addSpacing(2)  
        layout.addWidget(iconContainer, alignment=Qt.AlignmentFlag.AlignLeft)
        # 可根据需要调整图标与文字之间的距离
        layout.addSpacing(4)  

        # 插件信息
        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(5)
        infoLayout.setContentsMargins(0, 0, 0, 0)
        
        nameLabel = BodyLabel(info.get("name", "未知插件"), card)
        nameLabel.setWordWrap(True)  # 允许文本换行
        
        authorLabel = CaptionLabel(f"作者: {info.get('author', '未知')}", card)
        authorLabel.setWordWrap(True)  # 允许文本换行
        
        descLabel = CaptionLabel(info.get("description", "无描述"), card)
        descLabel.setWordWrap(True)  # 允许文本换行
        
        infoLayout.addWidget(nameLabel)
        infoLayout.addWidget(authorLabel)
        infoLayout.addWidget(descLabel)
        layout.addLayout(infoLayout, stretch=1)

        # 创建外部容器框架
        container = QFrame(self.scrollWidget)
        container.setObjectName("PluginContainer")
        containerLayout = QHBoxLayout(container)
        containerLayout.setContentsMargins(10, 0, 10, 0)  # 上下边距从5px改为2px
        containerLayout.setSpacing(15)

        # 添加卡片到容器
        containerLayout.addWidget(card, stretch=1)  # 让卡片占据大部分空间

        # 添加独立按钮
        toggleButton = ToolButton(container)
        toggleButton.setObjectName(f"ToggleButton_{addon_name}")
        # 调整按钮高度适配卡片
        button_height = card.height() - 10  # 预留 10px 边距
        toggleButton.setFixedSize(int(button_height * 0.5), button_height)
        toggleButton.setCursor(Qt.CursorShape.PointingHandCursor)  # 鼠标悬停显示手型
        # 设置图标
        toggleButton.setIcon(FluentIcon.MORE)

        # 连接点击事件，点击按钮弹出菜单
        toggleButton.clicked.connect(lambda: self.showButtonMenu(card, toggleButton))
        containerLayout.addWidget(toggleButton, alignment=Qt.AlignmentFlag.AlignVCenter)

        # 设置卡片支持右键菜单
        card.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        card.customContextMenuRequested.connect(lambda pos: self.showContextMenu(card, pos))

        self.scrollLayout.insertWidget(self.scrollLayout.count()-1, container)

    def toggleCardState(self, card: QWidget):
        """切换卡片状态"""
        # 切换启用状态
        is_enabled = not card.property("enabled")
        card.setProperty("enabled", is_enabled)

        # 更新样式
        self.updateCardStyle()

    def updateCardStyle(self):
        """更新卡片样式和frame背景"""
        isDark = isDarkTheme()

        # 颜色定义
        bg_color = '#2E2E2E' if isDark else '#F5F5F5'
        hover_color = '#3A3A3A' if isDark else '#E0E0E0'
        border_color = '#444444' if isDark else '#DDDDDD'
        disabled_color = 'rgba(255, 100, 100, 0.5)'  # 透明红色
        active_color = '#4CAF50' if isDark else '#66BB6A'  # 绿色
        inactive_color = '#f44336' if isDark else '#ef5350'  # 红色
        pressed_color = '#388E3C' if isDark else '#4CAF50'  # 按下时的绿色
        pressed_inactive_color = '#C62828' if isDark else '#D32F2F'  # 按下时的红色

        # 尝试获取按钮高度，如果没有按钮则使用默认值
        button_height = 30  # 默认值
        for i in range(self.scrollLayout.count()):
            item = self.scrollLayout.itemAt(i)
            if item.widget():
                container = item.widget()
                toggleButton = container.findChild(PushButton)
                if toggleButton:
                    button_height = toggleButton.height()
                    break

        style_str = f"""
            #PluginsFrame, #PluginsScrollArea, #PluginsScrollWidget {{
                background-color: {bg_color};
                border: none;
            }}
            #PluginCard {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
                padding: 15px;
            }}
            #PluginCard[enabled=false] {{
                background-color: {disabled_color};
            }}
            #PluginCard:hover {{
                background-color: {hover_color};
            }}
            #IconContainer {{
                background-color: {'rgba(255,255,255,0.1)' if isDark else 'rgba(0,0,0,0.05)'};
                border-radius: 10px;
            }}
            #PluginContainer {{
                background-color: transparent;
                border: none;
                margin: 5px 0;
            }}
            #PluginContainer > #ToggleButton {{
                background-color: {inactive_color};
                border: none;
                border-radius: 8px;
                color: white;
                icon-size: {int(button_height * 0.6)}px;
                transition: background-color 0.2s, transform 0.1s;
                /* 确保按钮在所有状态下都可点击 */
                pointer-events: auto; 
            }}
            #PluginContainer > #ToggleButton[enabled="true"] {{
                background-color: {active_color};
            }}
            #PluginContainer > #ToggleButton:hover {{
                opacity: 0.9;
            }}
            #PluginContainer > #ToggleButton:pressed {{
                background-color: {pressed_color};
                transform: translateY(1px);
            }}
            #PluginContainer > #ToggleButton[enabled="false"]:pressed {{
                background-color: {pressed_inactive_color};
            }}
        """
        self.setStyleSheet(style_str)

    def deleteCard(self, card: QWidget):
        """删除卡片及其对应的按钮"""
        # 找到包含卡片和按钮的容器
        container = card.parent()
        if container and container.objectName() == "PluginContainer":
            # 从布局中移除容器
            layout = self.scrollLayout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() == container:
                    layout.removeWidget(container)
                    container.deleteLater()  # 删除容器及其子控件（卡片和按钮）
                    break

        self.updateCardStyle()

    def disableSelected(self):
        """禁用当前选中的插件"""
        selected_card = self.getSelectedCard()
        if selected_card:
            self.toggleCardState(selected_card)

    def enableSelected(self):
        """启用当前选中的插件"""
        selected_card = self.getSelectedCard()
        if selected_card:
            self.toggleCardState(selected_card)

    def getSelectedCard(self):
        """获取当前选中的卡片"""
        # 这里需要实现获取选中卡片的逻辑
        # 返回当前选中的卡片对象或None
        pass


    def showButtonMenu(self, card: QWidget, button: QWidget):
        """显示按钮点击后的菜单"""
        menu = RoundMenu(parent=button)

        # 添加菜单项
        disable_action = Action(FluentIcon.CANCEL, "禁用", menu)
        enable_action = Action(FluentIcon.ACCEPT, "启用", menu)
        delete_action = Action(FluentIcon.DELETE, "删除", menu)

        # 根据当前状态设置默认选项
        is_enabled = card.property("enabled")
        if is_enabled:
            menu.addAction(disable_action)
        else:
            menu.addAction(enable_action)
        menu.addAction(delete_action)

        # 连接菜单项信号
        disable_action.triggered.connect(lambda: self.toggleCardState(card))
        enable_action.triggered.connect(lambda: self.toggleCardState(card))
        delete_action.triggered.connect(lambda: self.deleteCard(card))

        # 显示菜单
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def showContextMenu(self, card: QWidget, pos):
        """显示卡片右键菜单"""
        menu = RoundMenu(parent=card)

        # 添加菜单项
        disable_action = Action(FluentIcon.CANCEL, "禁用", menu)
        enable_action = Action(FluentIcon.ACCEPT, "启用", menu)
        delete_action = Action(FluentIcon.DELETE, "删除", menu)

        # 根据当前状态设置默认选项
        is_enabled = card.property("enabled")
        if is_enabled:
            menu.addAction(disable_action)
        else:
            menu.addAction(enable_action)
        menu.addAction(delete_action)

        # 连接菜单项信号
        disable_action.triggered.connect(lambda: self.toggleCardState(card))
        enable_action.triggered.connect(lambda: self.toggleCardState(card))
        delete_action.triggered.connect(lambda: self.deleteCard(card))

        # 显示菜单
        global_pos = card.mapToGlobal(pos)
        menu.exec(global_pos)