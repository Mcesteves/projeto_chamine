from OpenGL.GL import *
import numpy as np

class TexBuffer():
  def __init__ (self, varname, array):
    self.varname = varname
    self.buffer = glGenBuffers(1)
    self.tex = glGenTextures(1)
    self.__setData__(array)

    def __set_data__ (self, array):
        self.format = GL_RGBA32F
        glBindTexture(GL_TEXTURE_BUFFER,self.tex)
        glBindBuffer(GL_TEXTURE_BUFFER,self.buffer)
        glBufferData(GL_TEXTURE_BUFFER,array.nbytes,array,GL_STATIC_DRAW)
        glTexBuffer(GL_TEXTURE_BUFFER,self.format,self.buffer)
    
    def get_tex_id (self):
        return self.tex

    def load (self, shader):
        shader.active_texture(self.varname)
        glBindTexture(GL_TEXTURE_BUFFER,self.tex)

    def unload (self, shader):
        shader.deactive_texture()