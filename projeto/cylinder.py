from OpenGL.GL import *

class Cylinder ():
  def __init__(self, coords):
    self.coords = coords;
    glPatchParameteri(GL_PATCH_VERTICES, 2)
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, self.coords.nbytes, self.coords, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

  def draw(self):
    glBindVertexArray(self.vao)
    glDrawArrays(GL_PATCHES, 0, 2)