#classe de linha para teste de desempenho
from OpenGL.GL import *
import glm
import numpy as np

class Polyline ():
    def __init__(self, points):
        l = self.__calculate_tangent__(points)
        self.points = np.array(l, dtype= "float32")
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

    def __calculate_tangent__(self,points):
        i = 0
        l = []
        while i < len(points)/3 - 1:
            t = glm.vec3(points[3*(i+1)],points[3*(i+1)+1],points[3*(i+1)+2]) - glm.vec3(points[3*i],points[3*i+1],points[3*i+2])
            l.append(points[3*i])
            l.append(points[3*i+1])
            l.append(points[3*i+2])
            i += 1
        return l



