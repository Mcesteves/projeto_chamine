from OpenGL.GL import *
import numpy as np
import glm

def read_shader_file (filename):
  with open(filename) as f:
    lines = f.readlines()
  return lines

class Shader:
  def __init__(self, light=None, space="camera"):
    self.light = light
    self.pid = None
    self.space = space
    self.shaders = []
    self.texunit = 0

  
  def attach_vertex_shader (self, filename):
    self.shaders.append(self.__create_shader(GL_VERTEX_SHADER, filename))

  def attach_fragment_shader (self, filename):
    self.shaders.append(self.__create_shader(GL_FRAGMENT_SHADER, filename))

  # def attach_geometry_shader (self, filename):
  #   self.shaders.append(self.__create_shader(GL_GEOMETRY_SHADER, filename))
    
  def attach_tesselation_shader (self, control_filename, evaluation_filename):
    self.shaders.append(self.__create_shader(GL_TESS_CONTROL_SHADER,control_filename))
    self.shaders.append(self.__create_shader(GL_TESS_EVALUATION_SHADER,evaluation_filename))

  def link (self):
    glBindVertexArray(glGenVertexArrays(1))
    self.pid = self.__create_program(*self.shaders)

  def get_light (self):
    return self.light

  def get_lightning_space (self):
    return self.space

  def use_program (self):
    type(self.pid)
    glUseProgram(self.pid)

  def active_texture (self, varname):
    self.set_uniform(varname,self.texunit)
    glActiveTexture(GL_TEXTURE0+self.texunit)
    #self.texunit += 1

  def deactive_texture (self):
    self.texunit -= 1


  def __create_shader (self, type, filename):
    id = glCreateShader(type)
    if not id:
      raise RuntimeError("Could not create shader.")
    fileText = read_shader_file(filename)
    glShaderSource(id, fileText)
    self.__compile_shader(id, filename)
    return id
  
  def __compile_shader (self, id, filename):
    glCompileShader(id)
    if not glGetShaderiv(id, GL_COMPILE_STATUS):
      error = glGetShaderInfoLog(id).decode()
      raise RuntimeError("Error: " + filename + "\n" + error)
    
  def __create_program (self, *argv):
    id = glCreateProgram()
    if not id:
      raise RuntimeError("Could not create shader")
    for arg in argv:
      glAttachShader(id, arg) 
    self.__link_program(id)
    return id
  
  def __link_program (self, id):
    glLinkProgram(id)
    if not glGetProgramiv(id, GL_LINK_STATUS):
        error = glGetProgramInfoLog(id).decode()
        raise RuntimeError('Linking error: ' + error)
    
  def set_uniform (self, varname, x):
    loc = glGetUniformLocation(self.pid,varname)
    tp = type(x)
    if tp == int:
      glUniform1i(loc,x)
    elif tp == float:
      glUniform1f(loc,x)
    elif tp == glm.vec3:
      glUniform3fv(loc,1,glm.value_ptr(x))
    elif tp == glm.vec4:
      glUniform4fv(loc,1,glm.value_ptr(x))
    elif tp == glm.mat4x4:
      glUniformMatrix4fv(loc,1,GL_FALSE,glm.value_ptr(x))
    elif tp == list:
      tpe = type(x[0])
      if tpe == int:
        glUniform1iv(loc,len(x),np.array(x,dtype='int'))
      elif tpe == float:
        glUniform1fv(loc,len(x),np.array(x,dtype='float'))
      elif tpe == glm.vec3:
        glUniform3fv(loc,len(x),np.array(x,dtype='float'))
      elif tpe == glm.vec4:
        glUniform4fv(loc,len(x),np.array(x,dtype='float'))
      elif tpe == glm.mat4x4:
        glUniformMatrix4fv(loc,len(x),GL_FALSE,np.array(x,dtype='float'))
      else:
        raise SystemError("Type not supported in list in Shader.SetUniform: " + str(tpe))
    else:
      raise SystemError("Type not supported in Shader.SetUniform: " + str(tp))
