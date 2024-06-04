#classe de linha para teste de desempenho
from OpenGL.GL import *
import numpy as np

class Polyline ():
    def __init__(self, points):
        self.points = np.array(points, dtype= "float32")
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.points.nbytes, self.points, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_STRIP,0, self.points.size//3)

