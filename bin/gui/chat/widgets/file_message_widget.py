from bin.imports.MCmain import *
from wcferry import WxMsg
from pathlib import Path
from subprocess import Popen

class FileMessageWidget(QWidget):
    def __init__(self, file_name, file_path, is_me, timestamp, parent=None, wxmsg:WxMsg = None):
        super().__init__(parent)
        self.file_name = file_name
        self.file_path = file_path
        self.is_me = is_me
        self.timestamp = timestamp
        self.wxmsg = wxmsg
        self.widget_parent = parent
        
        # 检查是否是图片文件
        self.is_image = Path(file_name).suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        
        self.initUI()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        if self.is_image:
            # 图片消息使用Fluent风格边框
            self.image_label = QLabel(self)
            pixmap = QPixmap(self.file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
                # 添加Fluent风格边框
                self.image_label.setStyleSheet("""
                    QLabel {
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                        padding: 2px;
                        background: white;
                    }
                """)
            else:
                self.image_label.setText("图片加载失败")
            layout.addWidget(self.image_label)
        else:
            # 使用Fluent风格的文件消息容器
            container = QWidget(self)
            container.setObjectName("fileMessageContainer")
            container.setStyleSheet("""
                #fileMessageContainer {
                    background-color: %s;
                    border-radius: 8px;
                    padding: 12px;
                    min-width: 200px;
                    max-width: 300px;
                    border: 1px solid %s;
                }
            """ % (
                "#e8f5e9" if self.is_me else "#f5f5f5",  # 背景色
                "#c8e6c9" if self.is_me else "#e0e0e0"   # 边框色
            ))
            
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(8)
            
            # 文件信息行
            info_layout = QHBoxLayout()
            info_layout.setSpacing(10)
            
            # 文件图标
            icon_label = QLabel(self)
            icon_provider = QFileIconProvider()
            file_info = QFileInfo(self.file_name)
            file_icon = icon_provider.icon(file_info)
            icon_label.setPixmap(file_icon.pixmap(48, 48))
            info_layout.addWidget(icon_label)
            
            info_layout.addSpacing(5)
            
            # 文件名
            name_label = QLabel(self.file_name, self)
            name_label.setStyleSheet("""
                font-weight: bold;
                font-size: 14px;
            """)
            name_label.setWordWrap(True)
            name_label.setMaximumWidth(200)
            name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            info_layout.addWidget(name_label)
            
            container_layout.addLayout(info_layout)
            
            # 底部时间戳
            bottom_layout = QHBoxLayout()
            bottom_layout.setContentsMargins(0, 0, 0, 0)
            bottom_layout.addStretch()
            
            time_label = QLabel(self.timestamp, self)
            time_label.setStyleSheet("font-size: 10px; color: #666;")
            bottom_layout.addWidget(time_label)
            
            container_layout.addLayout(bottom_layout)
            layout.addWidget(container)

    def show_context_menu(self, pos):
        # 使用Fluent风格的RoundMenu
        menu = RoundMenu(parent=self)
        
        # 使用Fluent风格的Action
        download_action = Action(FluentIcon.DOWNLOAD, "下载文件")
        download_action.triggered.connect(self.download_file)
        menu.addAction(download_action)
        
        if self.is_image:
            view_action = Action(FluentIcon.PHOTO, "查看原图")
            view_action.triggered.connect(self.view_image)
            menu.addAction(view_action)
        
        menu.exec(self.mapToGlobal(pos))

    def download_file(self):
        pass

    def view_image(self):
        # 查看原图
        if self.is_image:
            Popen([self.file_path],shell=True)