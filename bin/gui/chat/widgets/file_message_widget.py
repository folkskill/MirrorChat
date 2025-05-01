from imports.MCmain import *
from wcferry import WxMsg

class FileMessageWidget(QWidget):
    def __init__(self, file_name, file_path, is_me, timestamp, parent=None, wxmsg:WxMsg = None):
        super().__init__(parent)
        self.file_name = file_name
        self.file_path = file_path
        self.is_me = is_me
        self.timestamp = timestamp
        self.wxmsg = wxmsg
        
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Main container with rounded corners
        container = QWidget(self)
        container.setObjectName("fileMessageContainer")
        container.setStyleSheet("""
            #fileMessageContainer {
                background-color: %s;
                border-radius: 5px;
                padding: 10px;
                min-width: 200px;
                max-width: 300px;
            }
        """ % ("#dcf8c6" if self.is_me else "#ffffff"))
        
        container_layout = QVBoxLayout(container)  # 改为垂直布局
        container_layout.setSpacing(8)
        
        # File info row
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)  # 增加间距从2改为10
        
        # File icon
        icon_label = QLabel(self)
        # 根据文件扩展名获取对应图标
        icon_provider = QFileIconProvider()
        file_info = QFileInfo(self.file_name)
        file_icon = icon_provider.icon(file_info)
        icon_label.setPixmap(file_icon.pixmap(48, 48))
        info_layout.addWidget(icon_label)
        
        # 添加间距
        info_layout.addSpacing(5)  # 额外增加5像素间距
        
        # File name with ellipsis
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
        
        # Bottom row (buttons and timestamp)
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Download button
        download_btn = QPushButton("下载", self)
        download_btn.setFixedSize(80, 24)
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        download_btn.clicked.connect(self.download_file)
        bottom_layout.addWidget(download_btn)
        
        # Spacer
        bottom_layout.addStretch()
        
        # Timestamp
        time_label = QLabel(self.timestamp, self)
        time_label.setStyleSheet("font-size: 10px; color: #666;")
        bottom_layout.addWidget(time_label)
        
        container_layout.addLayout(bottom_layout)
        
        layout.addWidget(container)
        self.setLayout(layout)

    def download_file(self):
        pass