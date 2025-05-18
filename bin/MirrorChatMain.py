from gui.addon.widgets.plugins_frame import PluginsFrame
from gui.main.widgets.main_chat import MainChatFrame
from gui.settings.settings import SettingsFrame
from module.logRecoder import MirrorChatLogger
from module.moduleLoader import load_module
from imports.MCmain import *

class MirrorChatMain(FluentWindow):
    """ 主界面 """

    def __init__(self, size:tuple = (900, 600)):
        super().__init__()
        
        # 创建子界面
        self.homeInterface = MainChatFrame(self)
        self.settingsInterface = SettingsFrame(self)
        self.pluginsInterface = PluginsFrame(self)
        
        # 加载窗口样式设置
        load_module(self, [size], "bin\gui\main\interface\mian_window.mirc")
        load_module(self, [], "bin\gui\main\interface\main_subinterface.mirc")

    def closeEvent(self, e):
        """ 重写关闭事件，停止消息接收进程 """

        MirrorChatLogger.info("Closing MirrorChatMain...")

        return super().closeEvent(e)

def main():
    app = QApplication(sys.argv)
    w = MirrorChatMain()
    
    # 设置程序图标
    app_icon = QIcon("logo.png")
    app.setWindowIcon(app_icon)
    w.setWindowIcon(app_icon)
    
    w.show()

    quitCode = app.exec()

    MirrorChatLogger.info("MirrorChatMain is quiting...")
    w.homeInterface.closeMsgListener()

    if quitCode != 0:
        # 退出失败，写入日志错误信息
        MirrorChatLogger.error(f"MirrorChatMain quitted with code {quitCode}.")
    else:
        # 退出成功
        MirrorChatLogger.success("MirrorChatMain quitted successfully.")

    sys.exit(quitCode)

if __name__ == '__main__':
    MirrorChatLogger.success("Starting MirrorChatMain...")
    main()