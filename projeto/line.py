import math
from OpenGL.GL import *
import numpy as np
import glm

from preferences import Preferences
from utils import *
from texbuffer import *

class Line ():
  def __init__(self, points, colors):
    self.indices = []
    self.points = []
    self.angles = []

    #tratamento dos pontos
    self.points = Utils.remove_repeated_sequence(points)#rever essa para remover as cores dos pontos repetidos
    self.__create_indices__()
    self.__calculate_transformation_matrices__()
    self.points = Utils.vec3_to_vec4(points)
    self.__build_points_array__()
    self.angles.clear()
    self.colors = colors

    self.points = self.__add_colors__()
    
    self.points = np.array(self.points, dtype= "float32")
    self.indices = np.array(self.indices, dtype= "uint32")

    glPatchParameteri(GL_PATCH_VERTICES, 5)
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    self.vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    glBufferData(GL_ARRAY_BUFFER, self.points.nbytes, self.points, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 32, None)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(16))
    glEnableVertexAttribArray(1)
    self.ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

    

  #calcula matriz de transformacao que sera usada no shader
  def __set_transformation__(self, v0, v1, v2):
    translation = Utils.set_translation_matrix(v0)
    rotation = Utils.set_rotation_matrix(v0, v1, v2)

    matrix = translation*rotation

    return matrix

  def __get_point_from_idx__(self, idx):
    return (self.points[3*idx], self.points[3*idx + 1], self.points[3*idx + 2])

  def __create_indices__(self):
    id = 0
    if len(self.points) == 6:
      self.indices.append(0)
      self.indices.append(0)
      self.indices.append(1)
      self.indices.append(1)
      self.indices.append(1)
    else:
      self.indices.append(id)
      self.indices.append(id)
      self.indices.append(id+1)
      self.indices.append(id+2)
      if len(self.points) == 9:
        self.indices.append(id+2)
      else:
        self.indices.append(id+3)
      while id < len(self.points)/3 - 2:
        self.indices.append(id)
        self.indices.append(id+1)
        self.indices.append(id+2)
        if id == len(self.points)/3 - 3:
          self.indices.append(id+2)
          self.indices.append(id+2)
        elif id == len(self.points)/3 - 6:
          self.indices.append(id+3)
          self.indices.append(id+3)
        else:
          self.indices.append(id+3)
          self.indices.append(id+4)
        id +=1

  def __calculate_transformation_matrices__(self):
    self.matrices = []
    i= 0
    while i < len(self.indices)/5:
      p0 = glm.vec3(self.__get_point_from_idx__(self.indices[5*i + 1]))
      p1 = glm.vec3(self.__get_point_from_idx__(self.indices[5*i + 2]))
      p2 = glm.vec3(self.__get_point_from_idx__(self.indices[5*i + 3]))
      self.matrices.append(self.__set_transformation__(p0, p1, p2))
      i += 1

    id = len(self.indices)//5 - 2
    angle_sum = 0

    while id >= 0:
      p0 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5]))
      p1 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 1]))
      p2 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 2]))
      p3 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 3]))
      angle = self.__calculate_angle__(p0, p1, p2, p3, id)
      angle_sum += angle
      self.angles.append(angle_sum)
      id -= 1

    self.matrices.clear()

  def __calculate_angle__(self, p0, p1, p2, p3, id):

    #calculo de dois pontos do toro do ramo atual
    v1 = glm.vec3(p1 - p0)
    v2 = glm.vec3(p2 - p1)
    v3 = glm.vec3(p3 - p2)

    theta = 0
    in_radius = 1

    d2 = min(0.15*glm.length(v2), 0.15*glm.length(v3))
    height = glm.length(v2)

    torus_angle = Utils.calculate_torus_angle(v2,v3)
    if torus_angle == 0:
      return 0.0

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

    angle = Utils.calculate_torus_angle(vec1, vec2)
    
    x = -(-R + (R + in_radius*math.cos(theta+angle))*math.cos(phi))
    y = height - d2 + (R + in_radius*math.cos(theta+angle))*math.sin(phi)
    z = in_radius * math.sin(theta+angle)
    w = 1.0

    new_torus_point = self.matrices[id]*glm.vec4(x,y,z,w)

    if Utils.is_vertix_equal(cylinder_point, new_torus_point):
      return angle
    else:
      return -angle
    
  def __add_coord_to_point__(self, point, angle):
    return (point.x, point.y, point.z, angle)
  
  def __build_points_array__(self):
    i = 0
    while i < len(self.indices)/5 - 1:
      index = self.indices[5*i+2]
      self.points[index*4+3] = self.angles[len(self.angles)- 1 - i]
      i+=1

  def __add_colors__(self):
    l = []
    i = 0
    while i < len(self.points)/4:
      l.append(self.points[4*i])
      l.append(self.points[4*i+1])
      l.append(self.points[4*i+2])
      l.append(self.points[4*i+3])
      l.append(self.colors[4*i])
      l.append(self.colors[4*i+1])
      l.append(self.colors[4*i+2])
      l.append(self.colors[4*i+3])
      i+=1

    return l
  
  def __vec3_to_vec4__(self, points):
    l = []
    i = 0
    while i < len(points):
      l.append(points[i])
      l.append(points[i+1])
      l.append(points[i+2])
      l.append(0.0)
      i = i + 3    
    return l
  
  def draw(self):
    glBindVertexArray(self.vao)
    glDrawElements(GL_PATCHES, self.indices.size, GL_UNSIGNED_INT, None)

  
  
