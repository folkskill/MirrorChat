from module.logRecoder import MirrorChatLogger
from queue import Empty
from wcferry import *
import threading
import os

wcf: Wcf
enableReceive = True
WcfWasInit = False

@MirrorChatLogger.catch()
def init_wcferry():
    '''初始化wcferry，必须在使用其他函数之前调用'''
    global wcf, WcfWasInit
    wcf = Wcf()
    WcfWasInit = True

def getinfo(wxid: str):
    global wcf

    return wcf.get_info_by_wxid(wxid)

def sendMsg(msg: str, to: str):
    global wcf

    wcf.send_text(msg, to)

def get_contacts():
    global wcf

    return wcf.get_contacts()

def set_receving_msg(enable: bool):
    global wcf, enableReceive

    if enable: wcf.enable_receiving_msg()
    else: wcf.disable_recv_msg()

    enableReceive = enable

def enableReceivingMsg(handlerFunction):
    """
    开启监听消息线程，处理消息
    handlerFunction: 处理消息的函数，参数为消息内容和发送者的wxid
    示例：
        def handler(msg):
            print(f"收到消息：{msg}")
    """
    global enableReceive, wcf

    def ProcessMsg():
        MirrorChatLogger.info("Start listening for messages...")
        while enableReceive:
            try:
                getM = wcf.get_msg()
                handlerFunction(getM)
            except Empty:
                continue

        MirrorChatLogger.info("Message listening thread closed.")

    set_receving_msg(True)
    threading.Thread(target=ProcessMsg, name="ListenMessageThread").start()

init_wcferry()

if WcfWasInit:
    MirrorChatLogger.success("Wcferry was initialized successfully.")
else:
    MirrorChatLogger.critical("Wcferry was not initialized.")
    os._exit(-1)