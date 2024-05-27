from OpenGL.GL import *
import numpy as np

class TexBuffer():
  def __init__ (self, varname, array, type):
    self.varname = varname
    if type == "matrix":
        self.format = GL_RGBA32F
    else:
       self.format = GL_R32F
    self.buffer = glGenBuffers(1)
    self.tex = glGenTextures(1)
    self.__set_data__(array)

  def __set_data__ (self, array):
      glBindTexture(GL_TEXTURE_BUFFER,self.tex)
      glBindBuffer(GL_TEXTURE_BUFFER,self.buffer)
      glBufferData(GL_TEXTURE_BUFFER,array.nbytes,array,GL_STATIC_DRAW)
      glTexBuffer(GL_TEXTURE_BUFFER,self.format,self.buffer)
    
  def get_tex_id (self):
      return self.tex  
  def load (self, shader, unit):
      shader.active_texture(self.varname, unit)
      glBindTexture(GL_TEXTURE_BUFFER,self.tex)

  def unload (self, shader):
      shader.deactive_texture()