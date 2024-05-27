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
    self.angles = []
    #tratamento dos pontos
    self.points = self.__remove_repeated_sequence__(points)
    self.__create_indices__()
    self.__calculate_transformation_matrices__()    

    self.points = np.array(self.points, dtype= "float32")
    self.indices = np.array(self.indices, dtype= "uint32")
    self.mat_textbuffer = TexBuffer("transform_buffer", np.array(self.lines, dtype= "float32"), "matrix")
    self.angles_textbuffer = TexBuffer("angle_buffer", np.array(self.angles, dtype= "float32"), None)

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
      translation = self.__set_translation_matrix__(v0)
      rotation = self.__set_rotation_matrix__(v0, v1, v2)

      matrix = translation*rotation

      self.__mat_to_buffer__(matrix)

      return matrix

  def draw(self):
    glBindVertexArray(self.vao)
    glDrawElements(GL_PATCHES, self.indices.size, GL_UNSIGNED_INT, None)

  def set_transformation_buffer(self, shader):
    self.mat_textbuffer.load(shader, 1)

  def set_angle_buffer(self, shader):
    self.angles_textbuffer.load(shader, 2)

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

    id = 0
    while id <= len(self.indices) - 8:
      p0 = glm.vec3(self.__get_point_from_idx__(self.indices[id]))
      p1 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 1]))
      p2 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 2]))
      p3 = glm.vec3(self.__get_point_from_idx__(self.indices[id + 3]))
      self.angles.append(self.__calculate_angle__(p0, p1, p2, p3, id//4))
      id += 4


  def __calculate_angle__(self, p0, p1, p2, p3, id):

    #calculo de dois pontos do toro do ramo atual
    v1 = glm.vec3(p1 - p0)
    v2 = glm.vec3(p2 - p1)
    v3 = glm.vec3(p3 - p2)

    theta = 0
    in_radius = 0.05

    d2 = min(0.15*glm.length(v2), 0.15*glm.length(v3))
    height = glm.length(v2)

    torus_angle = self.__calculate_torus_angle__(v2,v3)
    R = d2*(1/math.tan(torus_angle/2))

    phi = torus_angle

    x = -(-R + (R + in_radius*math.cos(theta))*math.cos(phi))
    y = height - d2 + (R + in_radius*math.cos(theta))*math.sin(phi)
    z = in_radius * math.sin(theta)
    w = 1.0

    torus_point = self.matrices[id]*glm.vec4(x,y,z,w)

    x = -(-R + (R)*math.cos(phi))
    y = height - d2 + (R)*math.sin(phi)
    z = 0
    w = 1.0

    torus_center = self.matrices[id]*glm.vec4(x,y,z,w)

    #calculo de dois pontos do inicio do tramo seguinte

    cylinder_point = self.matrices[id+1]*glm.vec4(-in_radius, d2, 0, 1)
    cylinder_center = self.matrices[id+1]*glm.vec4(0,d2,0,1)

    vec1 = torus_point - torus_center
    vec2 = cylinder_point - cylinder_center

    angle = self.__calculate_torus_angle__(vec1, vec2)
    
    x = -(-R + (R + in_radius*math.cos(theta+angle))*math.cos(phi))
    y = height - d2 + (R + in_radius*math.cos(theta+angle))*math.sin(phi)
    z = in_radius * math.sin(theta+angle)
    w = 1.0

    new_torus_point = self.matrices[id]*glm.vec4(x,y,z,w)

    if self.__is_vertix_equal__(cylinder_point, new_torus_point):
      return angle
    else:
      return -angle
  

  def __calculate_torus_angle__(self, c1, c2):

    c1 = glm.normalize(c1)
    c2 = glm.normalize(c2)

    angle = math.acos(glm.dot(c1, c2))
    return angle
  
  def __is_vertix_equal__(self, v1, v2):
    if abs(v1.x - v2.x) > 0.0001:
      return False
    if abs(v1.y - v2.y)> 0.0001:
      return False
    if abs(v1.z - v2.z)> 0.0001:
      return False
    return True
  