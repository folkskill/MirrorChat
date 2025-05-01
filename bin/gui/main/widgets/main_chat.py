from imports.MCmain import *
from module.chatTools import *
from module.wechatWapper import *
from module.moduleLoader import load_module
from gui.chat.widgets.message_widget import MessageWidget
from gui.chat.widgets.file_message_widget import FileMessageWidget
from module.logRecoder import MirrorChatLogger

class DebugWXMsgContent:
    def __init__(self, type = None,
                  id = None,
                    xml = None,
                      sender = None,
                        roomid = None,
                          content = None,
                            thumb = None,
                              extra = None):
        self.content = content
        self.type = type
        self.id = id
        self.xml = xml
        self.sender = sender
        self.roomid = roomid
        self.thumb = thumb
        self.extra = extra

class MainChatSingals(QObject):
    """主聊天界面信号类"""
    singal_progess_message = pyqtSignal(WxMsg)

class MainChatFrame(QFrame):
    """ 主聊天界面 """

    @staticmethod
    @MirrorChatLogger.catch()
    def getwcf():
        return wcf
    
    def __init__(self, parent=None):
        """
        初始化主聊天界面
            parent: 父窗口对象

        :return: 无
        """

        super().__init__(parent)

        self.setWindowTitle("聊天")
        self.setObjectName("MainChatFrame")

        self.currentPath = os.getcwd()
        self.currentChat = None  # 当前聊天对象
        self.contacts:list = [
            {
                "wxid": "wxid_1234567890",
                "name": "好友1",
                "gender": "男",
                "remark": "备注1",
                "city": "北京",
                "country": "中国"
            }
        ]
        self.chatObjectlist:list = []  # 用于存储聊天对象的列表
        self.chatMessageWidgetList:list = []  # 用于存储每个聊天的消息列表
        self.icons = {"wxid":FluentIcon.PEOPLE, "@chatroom":FluentIcon.CHAT}
        self.singals = MainChatSingals()

        self.navigationInterface: NavigationInterface
        self.functionButton:      DropDownToolButton
        self.functionMenu:        RoundMenu
        self.rightWidget:         QWidget
        self.rightLayout:         QVBoxLayout
        self.chatWindow:          SmoothScrollArea
        self.chatContent:         QWidget
        self.chatLayout:          QVBoxLayout
        self.leftSpacer:          QWidget
        self.spacer:              QSpacerItem
        self.hBoxLayout:          QHBoxLayout
        self.inputEdit:           QTextBlock
        self.sendButton:          ToolButton
        self.searchEdit:          LineEdit

        # 加载窗口样式设置
        load_module(self, path = "bin\gui\chat\interface\main_chat_frame.mirc")
        
        self.initNavigation()
        # 初始化工具栏按钮
        self.initToolButton()
        # 聊天工具组
        self.chattools = ChatTools(self)
        self.functionButton.setMenu(self.functionMenu)
        
        # 连接信号槽
        self.sendButton.clicked.connect(self.sendMessage)
        self.singals.singal_progess_message.connect(self.receiveMessage)

        # 初始化消息监听
        enableReceivingMsg(self.emitSignalMsg)

    def showInfo(self, content, title:str, duration:int = 3000, type:str = "info"):
        """显示侧边消息"""
        takes = {
            "info": InfoBar.info,
            "warnning": InfoBar.warning,
            "error": InfoBar.error,
            "success": InfoBar.success
        }

        takes[type](
            title = title,
            content = str(content),
            orient = Qt.Orientation.Horizontal,
            position = InfoBarPosition.TOP_RIGHT,
            isClosable = True,
            duration = duration,
            parent = self
        )

    def initToolButton(self):
        """初始化工具栏按钮"""

        @MirrorChatLogger.catch()
        def createTriggedSlot(key_name: str, args: dict = {}):
            return lambda: self.chattools.functions[key_name](args)
        
        self.functionMenu = RoundMenu(parent=self)

        fileAction = Action(FluentIcon.FOLDER_ADD, "发送文件", self)
        fileAction.triggered.connect(createTriggedSlot("send_file",args={"is_silence":False}))
        self.functionMenu.addAction(fileAction)

    def initChatList(self, keywords:list = ["wxid", "@chatroom"]):
        """
        初始化聊天ID列表
            keywords: 关键字列表

        :return: 无
        """

        # 因为要重置，所以要先清空
        self.chatObjectlist.clear()

        for contact in self.contacts:
            # 排除特殊内容
            for keyword in keywords:
                if keyword in contact["wxid"] and contact["name"]:
                    # 写入聊天对象列表
                    self.chatObjectlist.append(contact)
                    self.navigationInterface.addItem(
                        icon = self.icons[keyword],
                        routeKey = contact["wxid"],
                        text = contact["name"],
                        tooltip = contact["name"],
                        position = NavigationItemPosition.SCROLL,
                        onClick = lambda: self.setCurrentChat(self.chatObjectlist.index(contact))
                    )

    def filterContacts(self):
        """根据搜索内容过滤联系人"""
        search_text = self.searchEdit.text().strip().lower()

        if not search_text:
            self.initChatList()
        
        for contact in self.contacts:
            self.navigationInterface.removeWidget(contact["wxid"])
        
        # 重新添加过滤后的联系人
        index = 0
        for contact in self.contacts:
            # 如果搜索内容为空或匹配联系人名称
            if not search_text or search_text in contact["name"].lower():
                ok = False
                icon = None
                keywords = self.icons
        
                # 排除公众号
                for keyword in keywords:
                    if keyword in contact["wxid"] and contact["name"]:
                        icon = keywords[keyword]
                        ok = True
                        break
        
                if not ok:
                    continue

        
                # 使用闭包为每个导航项创建独立的点击事件处理函数
                def create_click_handler(idx):
                    return lambda: self.setCurrentChat(idx)
        
                self.navigationInterface.addItem(
                    icon = icon,
                    routeKey = contact["wxid"],
                    text = contact["name"],
                    tooltip = contact["name"],
                    position = NavigationItemPosition.SCROLL,
                    onClick = create_click_handler(index)
                )
                index += 1

    def initNavigation(self):
        """初始化导航栏"""

        # 添加搜索按钮到导航栏第一个位置
        self.navigationInterface.addItem(
            icon=FluentIcon.SEARCH,
            routeKey="search_button",
            text="搜索",
            tooltip="搜索联系人",
            position=NavigationItemPosition.TOP,
            onClick=self.toggleSearchBox
        )
        
        self.initChatList()

    def toggleSearchBox(self):
        """切换搜索框的显示状态"""
        if self.searchEdit.isVisible():
            self.searchEdit.hide()
        else:
            self.searchEdit.show()
            self.searchEdit.setFocus()
            
    def setCurrentChat(self, index):
        # 设置当前聊天对象
        self.currentChat = self.chatObjectlist[index]
        
        # 隐藏搜索框
        self.searchEdit.hide()
        
        # 清除所有消息控件
        while self.chatLayout.count() > 0:
            # 遍历所有控件
            item = self.chatLayout.takeAt(0)
            widget = item.widget()

            # 只保留leftSpacer和搜索框
            if widget and widget not in [self.leftSpacer, self.spacer, self.searchEdit]:
                widget.deleteLater()

        self.chatMessageWidgetList.clear()  # 清空消息控件列表
        
        self.chatLayout.addWidget(self.leftSpacer)  # 添加占位控件
        self.chatLayout.addSpacerItem(self.spacer)  # 添加占位控件
        
    def emitSignalMsg(self, message:WxMsg):
        self.singals.singal_progess_message.emit(message)

    @pyqtSlot()
    def sendMessage(self):
        if self.currentChat is None:
            self.showInfo(
                title = "消息",
                content = "请选择聊天对象",
                type = "info",
            )
            return
        
        # 原有文本消息处理
        message = self.inputEdit.text()
        
        if message:
            timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
            message_widget = MessageWidget(message, is_me=True, timestamp=timestamp, parent=self.chatContent)
            self.chatLayout.insertWidget(self.chatLayout.count() - 1, message_widget)
            self.chatMessageWidgetList.append(message_widget)  # 存储消息控件
            self.inputEdit.clear()

            # 发送消息到微信
            # sendMsg(message, self.currentChat["wxid"])
            
            # 确保滚动条完全滚动到底部
            QTimer.singleShot(10, self.scrollToBottom)

    @pyqtSlot(WxMsg)
    def receiveMessage(self, message:WxMsg):

        # 原有文本消息处理代码
        print(message)

        # 如果是文件消息
        if message.type == 1090519089:
            self.handleFileMessage(message)
            return


        # 如果不是当前聊天对象的消息，则不处理
        if self.currentChat:
            if message.roomid != self.currentChat["wxid"]:
                if message.id != self.currentChat["wxid"]:
                    MirrorChatLogger.error(f"Received message from {message.id}, but current chat is {self.currentChat['wxid']}")
                    return

        name = message.sender

        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        message_widget = MessageWidget(f"{name}: {message.content}", is_me=False, timestamp=timestamp, parent=self.chatContent)
        # 修改插入方式，确保左对齐
        self.chatLayout.insertWidget(self.chatLayout.count() - 1, message_widget)
        self.chatMessageWidgetList.append(message_widget)  # 存储消息控件

        self.chatLayout.setAlignment(message_widget, Qt.AlignmentFlag.AlignLeft)  # 强制左对齐
        
        # 确保滚动条完全滚动到底部
        QTimer.singleShot(10, self.scrollToBottom)

    def handleFileMessage(self, message: WxMsg, is_me):
        """处理文件消息"""
        if self.currentChat:
            return

        # 获取文件名和路径（需要根据实际消息结构调整）
        file_name = message.content
        
        # 判断是否是自己发送的消息
        # is_me = False
        
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        
        # 创建文件消息控件
        file_widget = FileMessageWidget(
            file_name=file_name,
            file_path=file_name,
            is_me=is_me,
            timestamp=timestamp,
            parent=self.chatContent
        )
        
        # 添加到聊天界面
        self.chatLayout.insertWidget(self.chatLayout.count() - 1, file_widget)
        self.chatMessageWidgetList.append(file_widget)
        
        # 设置对齐方式
        alignment = Qt.AlignmentFlag.AlignRight if is_me else Qt.AlignmentFlag.AlignLeft
        self.chatLayout.setAlignment(file_widget, alignment)
        
        # 滚动到底部
        QTimer.singleShot(10, self.scrollToBottom)

    def scrollToBottom(self):
        """滚动到最底部"""
        # 确保滚动条完全滚动到底部
        scroll_bar = self.chatWindow.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        QApplication.processEvents()
        scroll_bar.setValue(scroll_bar.maximum())

    def closeMsgListener(self):
        """关闭消息监听"""
        # 关闭消息监听线程
        set_receving_msg(False)
        wcf.cleanup()