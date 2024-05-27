import math
from OpenGL.GL import *
import glm
import numpy as np

class Utils:
  @staticmethod
  def is_vertix_equal(v1, v2):
    if abs(v1.x - v2.x) > 0.0001:
      return False
    if abs(v1.y - v2.y)> 0.0001:
      return False
    if abs(v1.z - v2.z)> 0.0001:
      return False
    return True
    
  @staticmethod
  def calculate_torus_angle(c1, c2):  
      c1 = glm.normalize(c1)
      c2 = glm.normalize(c2)  
      angle = math.acos(glm.dot(c1, c2))
      return angle
  
  #Remove pontos adjacentes iguais
  @staticmethod 
  def remove_repeated_sequence(points):
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
  @staticmethod
  def set_translation_matrix(v0):
    return glm.mat4x4(
      glm.vec4(1.0, 0.0, 0.0, 0.0),
	  glm.vec4(0.0, 1.0, 0.0, 0.0),
	  glm.vec4(0.0, 0.0, 1.0, 0.0),
	  glm.vec4(v0.x, v0.y, v0.z, 1.0)
    )
  
  #calcula matriz de rotacao
  @staticmethod
  def set_rotation_matrix(v0, v1, v2):

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
  