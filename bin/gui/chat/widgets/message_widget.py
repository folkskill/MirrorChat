from bin.imports.MCmain import *
from bin.module.wechatWapper import WxMsg

class MessageWidget(QWidget):
    def __init__(self, message:WxMsg | str, is_me=False, timestamp=None, parent=None):
        super().__init__(parent)
        self.is_me = is_me
        self.message = message
        self.wparent = parent
        
        # 设置透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # 主布局
        self.Mlayout = QVBoxLayout(self)
        self.Mlayout.setContentsMargins(0, 0, 0, 0)  # 增加外边距
        self.Mlayout.setSpacing(2)
        
        # 消息内容
        self.message_label = QLabel(message, self)
        self.message_label.setWordWrap(True)
        
        # 修改消息标签样式，增加内边距
        self.message_label.setStyleSheet("""
            font-size: 15px;
            color: black;
            text-align: left;
        """)
        
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # 设置对齐方式
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True) 
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

        # 添加消息控件
        self.Mlayout.addWidget(self.message_label, 0, Qt.AlignmentFlag.AlignLeft)

        # 自动调整大小
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.adjustWidth()
        self.setContentsMargins(10, 10, 10, 10)
        self.setAlignment(is_me)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextEvent)

    def setAlignment(self, is_me):
        # 根据消息来源设置对齐方式
        if is_me:
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.setStyleSheet("""
                QWidget {
                    margin-left: 60px;
                    margin-right: 0px;
                }
            """)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.setStyleSheet("""
                QWidget {
                    margin-left: 0px;
                    margin-right: 60px;
                }
            """)
    
    def adjustWidth(self):
        # 根据文本内容计算最佳宽度
        font_metrics = self.message_label.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.message_label.text())
        
        # 设置最小和最大宽度
        min_width = 100    # 最小宽度
        max_width = 400  # 最大宽度
        
        # 计算实际需要的宽度，考虑字符宽度和边距
        content_width = min(max(text_width, min_width), max_width)
        
        # 设置固定宽度并允许高度自适应
        self.setFixedWidth(content_width)
        self.message_label.setFixedWidth(content_width)
        self.message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def paintEvent(self, event):
        # 自定义绘制圆角矩形背景
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 设置背景颜色
        bg_color = QColor("#95ec69") if self.is_me else QColor("#f1f1f1")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # 绘制圆角矩形
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), 5, 5)
        
        # 设置透明背景
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        
        painter.drawPath(path)
        
        super().paintEvent(event)

    def contextEvent(self, pos:QPoint):
        """ 右键菜单事件 """
        menu = RoundMenu(parent=self.parent())
        copy_action = Action(FluentIcon.COPY, "复制")
        copy_action.triggered.connect(self.copy_text)
        show_full_action = Action(FluentIcon.VIEW, "查看")
        show_full_action.triggered.connect(self.show_full_text)
        menu.addAction(copy_action)

        text:str = self.message.content if self.message is WxMsg else self.message
        # 如果文本过长，添加查看完整内容选项
        if len(text) > 100:  # 简单判断文本是否过长
            menu.addAction(show_full_action)

        menu.setMinimumWidth(300)
        menu.setMaximumWidth(350)
        menu.setFixedWidth(350)
        menu.setDefaultAction(show_full_action)

        pos.setX(pos.x() - 100)
        menu.exec(self.mapToGlobal(pos))

    def copy_text(self):
        """ 复制文本到剪贴板 """
        clipboard = QApplication.clipboard()
        text:str = self.message.content if self.message is WxMsg else self.message
        clipboard.setText(text)

    def show_full_text(self):
        """ 显示完整文本内容 """
        text:str = self.message.content if self.message is WxMsg else self.message
        self.wparent.showMessageBox(text[:15], text)