from imports.MCmain import *

class MessageWidget(QWidget):
    def __init__(self, message, is_me=False, timestamp=None, parent=None):
        super().__init__(parent)
        self.is_me = is_me
        self.message = message
        
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
            padding: 0px 0px 0px 23px;
            margin: 0;
            text-align: left;
        """)
        
        # 修改主布局的边距
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # 设置对齐方式
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True) 
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.message_label.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

        # 添加消息控件
        self.Mlayout.addWidget(self.message_label, 0, Qt.AlignmentFlag.AlignLeft)

        # 自动调整大小
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.adjustWidth()
        self.setContentsMargins(10, 10, 20, 10)
        self.setAlignment(is_me)

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
        min_width = 120  # 增加最小宽度
        max_width = 400  # 增加最大宽度
        
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
        path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), 10, 10)
        
        # 设置透明背景
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        
        painter.drawPath(path)
        
        super().paintEvent(event)