from imports.MCmain import *
from module.moduleLoader import load_module

class SubInstance(QFrame):
    def __init__(self, text: str, parent=None, path = ""):
        super().__init__(parent=parent)

        # 载入模块
        load_module(self, [text], path)