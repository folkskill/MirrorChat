from gui.main.widgets.main_chat import MainChatFrame
from gui.settings.settings import SettingsFrame
from module.moduleLoader import load_module
from imports.MCmain import *

class MirrorChatMain(FluentWindow):
    def __init__(self, size:tuple = (900, 600)):
        super().__init__()

        # 创建子界面
        self.homeInterface = MainChatFrame(self)
        self.settingsInterface = SettingsFrame(self)
        
        # 加载窗口样式设置
        load_module(self, [size], "bin\gui\main\interface\mian_window.mirc")
        load_module(self, [], "bin\gui\main\interface\main_subinterface.mirc")

    def closeEvent(self, e):
        """ 重写关闭事件，停止消息接收进程 """
        self.homeInterface.closeMsgListener()

        print("关闭主窗口")

        return super().closeEvent(e)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MirrorChatMain()
    w.show()
    
    sys.exit(app.exec())