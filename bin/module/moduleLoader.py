"""
本模块用于加载模块。
使用方法：
    `from moduleLoader import load_module`
    `load_module(Qobject, args = [], path = "",)`

参数：
    `Qobject`: 要加载模块的对象
    `args`: 要传递给模块的参数
    `path`: 模块的路径

"""
from bin.module.logRecoder import MirrorChatLogger
from colorama import Fore

@MirrorChatLogger.catch()
def static_load_module(Qobject, args = [], code = ""):
    """
    参数：
        `Qobject`: 要加载模块的对象
        `args`: 要传递给模块的参数
        `path`: 模块的路径
    """
    # 执行整个文件内容
    exec(code)

@MirrorChatLogger.catch()
def load_module(Qobject, args = [], path = "", silence = False):
    """
    参数：
        `Qobject`: 要加载模块的对象
        `args`: 要传递给模块的参数
        `path`: 模块的路径
    """
    if not silence:
        MirrorChatLogger.info(f"Loading module at: {Fore.BLUE}{path}")
    # 读取文件内容并统一换行符
    content = open(path, "r", encoding = "utf-8").read().replace('\r\n', ';')
    # 执行整个文件内容
    exec(content)