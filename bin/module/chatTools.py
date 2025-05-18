from imports.MCmain import *
from module.logRecoder import MirrorChatLogger
from module.moduleLoader import load_module
from pathlib import Path
from wcferry import Wcf

def get_directory_info(path):
    """获取目录内容并区分文件和文件夹"""
    path = Path(path)
    contents = []
    
    for item in path.iterdir():
        info = {
            'name': item.name,
            'is_file': item.is_file(),
            'is_dir': item.is_dir(),
            'size': item.stat().st_size if item.is_file() else 0
        }
        contents.append(info)
    
    return contents

class ChatTools:
    
    """聊天工具"""

    def __init__(self, chat_frame):
        """初始化聊天工具"""

        self.chat_frame = chat_frame
        self.functions:dict = {
            "send_file": self.send_file
        }  # 函数字典，用于存储函数信息

        addon_name:str = None
        try:
            # 遍历插件目录
            for addon in get_directory_info("bin\\addon"):
                if addon["is_dir"]:
                    # 加载插件
                    addon_name = addon["name"]
                    load_module(self, path = f"bin\\addon\\{addon['name']}\\tools\\tool.mirc")

                    self.chat_frame.showInfo(
                        title = "插件",
                        type = "success",
                        content = f"{addon_name} 加载成功",
                        duration = 3000
                    )

        except Exception as e:
            # 加载失败
            print(e)
            self.chat_frame.showInfo(
                title = "插件",
                type = "error",
                content = f"{addon_name} 加载失败: {str(e)}",
                duration = 5000
            )
    
    def send_file(self, args:dict):
        """发送文件"""

        def check_file_type(file_path):
            """检查文件类型"""
            return file_path.split(".")[-1]

        if not args["is_silence"]:
            # 使用QFileDialog选择文件
            file_path, _ = QFileDialog.getOpenFileName(
                parent=self.chat_frame,
                caption="选择要发送的文件",
                filter="所有文件 (*.*)"
            )
        else:file_path = args["file_path"]
        
        # 如果用户选择了文件
        if file_path:
            # 获取 wcferry 对象
            wcf:Wcf = self.chat_frame.getwcf()

            if self.chat_frame.currentChat:
                # 如果当前有聊天对象，发送文件
                file_type = check_file_type(file_path)

                MirrorChatLogger.debug(f"发送文件: {file_path}, 类型: {file_type}")
                
                if file_type in ["png", "jpg", "jpeg", "gif", "bmp"]:
                    # 如果是图片文件，发送图片消息
                    wcf.send_image(file_path, self.chat_frame.currentChat["wxid"])
                elif file_type in ["mp4", "avi", "mov", "wmv", "flv"]:
                    # 如果是视频文件，发送视频消息
                    wcf.send_image(file_path, self.chat_frame.currentChat["wxid"])
                else:
                    # 其他文件，发送文件消息
                    wcf.send_file(file_path, self.chat_frame.currentChat["wxid"])

                self.chat_frame.handleFileMessage(args = {
                    "file_path": file_path,
                    "is_me": True
                })

                self.chat_frame.showInfo(
                    title = "发送",
                    content = f"{file_path} 发送成功",
                    type = "success",
                    duration = 3000
                )
            else:
                # 没有聊天对象，不发送
                self.chat_frame.showInfo(
                    title = "消息",
                    content = "当前没有聊天对象",
                    type = "info",
                    duration = 3000
                )
        else:
            # 用户没有选择文件，警告
            self.chat_frame.showInfo(
                title = "警告",
                content = "未选择文件",
                type = "warnning", 
            )