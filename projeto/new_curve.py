import math
from OpenGL.GL import *
import numpy as np
import glm

from texbuffer import *

class NewCurve ():
  def __init__(self, points):
    self.indices = []
    self.points = []
    self.lines = []
    #tratamento dos pontos
    self.points = self.__remove_repeated_sequence__(points)
    self.__create_indices__()
    self.__calculate_transformation_matrices__()       

    self.points = np.array(self.points, dtype= "float32")
    self.indices = np.array(self.indices, dtype= "uint32")
    self.texbuffer = TexBuffer("transform_buffer", np.array(self.lines, dtype= "float32"))

    glPatchParameteri(GL_PATCH_VERTICES, 4)
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    self.vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    glBufferData(GL_ARRAY_BUFFER, self.points.nbytes, self.points, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    self.ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

  #Remove pontos adjacentes iguais
  def __remove_repeated_sequence__(self, points):
    l = []
    i = 0
    while i < len(points) - 3:
      if((points[i], points[i+1], points[i+2]) != (points[i+3], points[i+4], points[i+5])):
        l.append(points[i])
        l.append(points[i+1])
        l.append(points[i+2])
      i = i + 3    
    l.append(points[i])
    l.append(points[i+1])
    l.append(points[i+2])
    return l

  #calcula matriz de translacao
  def __set_translation_matrix__(self, v0):
    t = v0
    #return glm.mat4x4(1.0)
    return glm.mat4x4(
        glm.vec4(1.0, 0.0, 0.0, 0.0),
		    glm.vec4(0.0, 1.0, 0.0, 0.0),
		    glm.vec4(0.0, 0.0, 1.0, 0.0),
		    glm.vec4(t.x, t.y, t.z, 1.0)
      )

  #calcula matriz de rotacao
  def __set_rotation_matrix__(self, v0, v1, v2):

    y = v1 - v0
    x = v2 - v1

    z = glm.cross(glm.normalize(x), y)

    if math.isnan(z.x) or x == glm.vec3(0):
      z = glm.cross(glm.normalize(y), glm.vec3(-y.y, y.x, 0))
      
    x = glm.cross(glm.normalize(y), z)

    return glm.mat4x4(
      glm.vec4(glm.normalize(x), 0.0),
      glm.vec4(glm.normalize(y), 0.0),
      glm.vec4(glm.normalize(z), 0.0),
      glm.vec4(0.0, 0.0, 0.0, 1.0)
    )
  
  #calcula matriz de transformacao que sera usada no shader
  def __set_transformation__(self,v0, v1, v2, id):
    if id == 0:
      translation = self.__set_translation_matrix__(v0)
      rotation = self.__set_rotation_matrix__(v0, v1, v2)
      matrix = translation*rotation

      self.__mat_to_buffer__(matrix)
      return matrix
    else:
      new_v0 = glm.vec3(self.matrices[id-1] * glm.vec4(v0, 0))
      new_v1 = glm.vec3(self.matrices[id-1] * glm.vec4(v1, 0))
      new_v2 = glm.vec3(self.matrices[id-1] * glm.vec4(v2, 0))
      translation = self.__set_translation_matrix__(new_v0)
      rotation = self.__set_rotation_matrix__(new_v0, new_v1, new_v2)

      matrix = translation*rotation*self.matrices[id-1]

      self.__mat_to_buffer__(matrix)

      return matrix

  def draw(self):
    glBindVertexArray(self.vao)
    glDrawElements(GL_PATCHES, self.indices.size, GL_UNSIGNED_INT, None)

  def set_transformation_buffer(self, shader):
    self.texbuffer.load(shader)

  def __get_point_from_idx__(self, idx):
    return (self.points[3*idx], self.points[3*idx + 1], self.points[3*idx + 2])
  
  def __mat_to_buffer__(self, matrix):
    self.lines.append(matrix[0].x)
    self.lines.append(matrix[1].x)
    self.lines.append(matrix[2].x)
    self.lines.append(matrix[3].x)
    self.lines.append(matrix[0].y)
    self.lines.append(matrix[1].y)
    self.lines.append(matrix[2].y)
    self.lines.append(matrix[3].y)
    self.lines.append(matrix[0].z)
    self.lines.append(matrix[1].z)
    self.lines.append(matrix[2].z)
    self.lines.append(matrix[3].z)

  def __create_indices__(self):
    id = 0
    if len(self.points) == 6:
      self.indices.append(0)
      self.indices.append(0)
      self.indices.append(1)
      self.indices.append(1)
    else:
      while id < len(self.points)/3 - 2:
        if id == 0:
          self.indices.append(id)
          self.indices.append(id)
          self.indices.append(id+1)
          self.indices.append(id+2)

        if id == len(self.points)/3 - 3:
          self.indices.append(id)
          self.indices.append(id+1)
          self.indices.append(id+2)
          self.indices.append(id+2)
          id +=1
        else:
          self.indices.append(id)
          self.indices.append(id+1)
          self.indices.append(id+2)
          self.indices.append(id+3)
          id += 1

  def __calculate_transformation_matrices__(self):
    self.matrices = []
    id = 0
    while id <= len(self.indices) - 4:
      p0 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 1]))
      p1 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 2]))
      p2 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 3]))
      self.matrices.append(self.__set_transformation__(p0, p1, p2, id//4))
      id += 4