from PyQt6.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram
from OpenGL.GL import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

class OpenGLBackground(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shader_program = None

    def initializeGL(self):
        # 设置背景颜色
        glClearColor(0.2, 0.2, 0.2, 1.0)  # 深灰色背景
        glEnable(GL_DEPTH_TEST)

        # 创建并编译着色器
        self.shader_program = QOpenGLShaderProgram(self)
        self.shader_program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex, """
            #version 330 core
            layout (location = 0) in vec3 aPos;
            void main()
            {
                gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
            }
        """)
        self.shader_program.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, """
            #version 330 core
            out vec4 FragColor;
            void main()
            {
                FragColor = vec4(0.8, 0.2, 0.2, 1.0);  // 红色背景
            }
        """)
        self.shader_program.link()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 绘制一个简单的三角形作为背景
        vertices = [
            -0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0,  0.5, 0.0
        ]
        vertex_data = (GLfloat * len(vertices))(*vertices)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertex_data)
        glEnableVertexAttribArray(0)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableVertexAttribArray(0)

class SmoothScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 创建一个自定义的OpenGL背景
        self.opengl_background = OpenGLBackground(self)
        self.opengl_background.resize(self.width(), self.height())

        # 创建滚动区域的内容
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        for i in range(1, 100):
            self.scroll_layout.addWidget(QPushButton(f"按钮 {i}"))
        self.setWidget(self.scroll_content)

        # 设置透明背景
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
        self.scroll_content.setStyleSheet("QWidget{background: transparent}")

        # 将OpenGL背景设置为滚动区域的背景
        self.setWidgetResizable(True)
        self.viewport().stackUnder(self.opengl_background)

if __name__ == "__main__":
    app = QApplication([])
    scroll_area = SmoothScrollArea()
    scroll_area.show()
    app.exec()