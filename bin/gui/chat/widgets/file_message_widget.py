from imports.MCmain import *

class FileMessageWidget(QWidget):
    def __init__(self, file_name, file_path, is_me, timestamp, parent=None):
        super().__init__(parent)
        self.file_name = file_name
        self.file_path = file_path
        self.is_me = is_me
        self.timestamp = timestamp
        
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
                border-radius: 10px;
                padding: 8px;
            }
        """ % ("#dcf8c6" if self.is_me else "#ffffff"))
        
        container_layout = QHBoxLayout(container)
        
        # File icon
        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon.fromTheme("text-x-generic").pixmap(32, 32))
        container_layout.addWidget(icon_label)
        
        # File name
        name_label = QLabel(self.file_name, self)
        container_layout.addWidget(name_label)
        
        # Download button
        download_btn = QPushButton("下载", self)
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        download_btn.clicked.connect(self.download_file)
        container_layout.addWidget(download_btn)
        
        # Timestamp
        time_label = QLabel(self.timestamp, self)
        time_label.setStyleSheet("font-size: 10px; color: #666;")
        container_layout.addWidget(time_label)
        
        layout.addWidget(container)
        self.setLayout(layout)

    def download_file(self):
        # Implement file download logic here
        print(f"Downloading file: {self.file_path}")
        # You can use QFileDialog to choose save location
        # and copy the file from self.file_path to the chosen location
