from queue import Empty
from wcferry import *
import threading

wcf = Wcf()
enableReceive = True

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
        print("开启监听消息线程...")
        while enableReceive:
            try:
                getM = wcf.get_msg()
                handlerFunction(getM)
            except Empty:
                continue
            except Exception as e:
                print(f"ERROR: {e}")
            
        print("监听消息线程已关闭...")

    set_receving_msg(True)
    threading.Thread(target=ProcessMsg, name="ListenMessageThread").start()

if __name__ == '__main__':
    enableReceivingMsg(lambda msg: print(f"收到消息：{msg.content}"))
    while True: pass