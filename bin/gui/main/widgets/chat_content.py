from bin.imports.MCmain import *
from bin.imports.OpenGL import *
from inspect import currentframe
from bin.module.logRecoder import MirrorChatLogger
from bin.module.moduleLoader import static_load_module, load_module
 
def getFName():
    return currentframe().f_back.f_code.co_name

class ChatContent(QOpenGLWidget):
    headpath = "bin/gui/main/styles"

    def __init__(self, parent=None, backgroundStyle = "sea"):
        super().__init__(parent)
        self.shader_program:QOpenGLShaderProgram
        self.rotation_x = 0
        self.rotation_y = 0
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.vertices = None
        self.indices = None
        self.timer:QTimer = None
        self.paintThread:QThread = None
        self.backgroundStyle = backgroundStyle
        self.times = 0
        self.running = True

        self.funcDict = {
            self.initializeGL.__name__  :"",
            self.updateRotation.__name__:"",
            self.PaintOpenGL.__name__   :""
        }

        load_module(self, path=f"{self.headpath}/{self.backgroundStyle}/{getFName()}.mirc")

        # 载入脚本函数
        self.load_func()

    def closeEvent(self, e):
        """ 重写关闭事件，停止进程 """
        self.running = False
        return super().closeEvent(e)
        
    @MirrorChatLogger.catch()
    def load_func(self):
        """从脚本中加载函数"""
        for funcName in self.funcDict:
            # 如果脚本不存在，跳过
            path = f"{self.headpath}/{self.backgroundStyle}/{funcName}.mirc"
            if not os.path.exists(path):
                MirrorChatLogger.warning(f"The script {path} not exists, skip it.")
                continue
            # 读取脚本内容
            code = open(path, "r", encoding = "utf-8").read().replace('\r\n', ';')
            self.funcDict[funcName] = code

    def initializeGL(self):
        self.shader_program:QOpenGLShaderProgram
        static_load_module(self, code=self.funcDict[getFName()])

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def updateRotation(self):
        static_load_module(self, code=self.funcDict[getFName()])

    def paintGL(self):
        self.updateRotation()
        self.PaintOpenGL()

    def PaintOpenGL(self):
        """OpenGL绘制函数"""
        self.times += 0.001
        static_load_module(self, code=self.funcDict[getFName()])

if __name__ == "__main__":
    app = QApplication([])
    widget = ChatContent()
    widget.show()
    app.exec() 