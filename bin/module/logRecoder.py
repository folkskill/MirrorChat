from loguru import logger as MirrorChatLogger

MirrorChatLogger.add(
    sink="logs/{time:YYYY-MM-DD}.log",
    enqueue=True,
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

def processStop(type = MirrorChatLogger.info):
    """
    处理程序停止时的操作，如关闭日志文件等。
    """
    MirrorChatLogger.remove()
    MirrorChatLogger.success("The log system has been closed.")