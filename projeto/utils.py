import math
from OpenGL.GL import *
import glm
import numpy as np

from line import Line

class Utils:
  @staticmethod
  def is_vertix_equal(v1, v2):
    if abs(v1.x - v2.x) > 0.000000001:
      return False
    if abs(v1.y - v2.y)> 0.0000000001:
      return False
    if abs(v1.z - v2.z)> 0.0000000001:
      return False
    return True
    
  @staticmethod
  def calculate_torus_angle(c1, c2):  
      c1 = glm.normalize(c1)
      c2 = glm.normalize(c2)  
      dot = glm.dot(c1, c2)
      if dot > 1:
        dot = 1
      if dot < -1:
        dot = -1
      angle = math.acos(dot)
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
    if(x == glm.vec3(0)):
      x = glm.vec3(1.0, 0.0, 0.0)
    z = glm.cross(glm.normalize(x), y)

    if math.isnan(z.x) or z == glm.vec3(0):
      z = glm.cross(glm.normalize(y), glm.vec3(-y.y, y.x, 0))
      if math.isnan(z.x) or z == glm.vec3(0):
        z = glm.cross(glm.normalize(y), glm.vec3(-y.z, 0, y.x))
        if math.isnan(z.x) or z == glm.vec3(0):
          z = glm.cross(glm.normalize(y), glm.vec3(0, -y.z, y.y))
      
    x = glm.cross(glm.normalize(y), glm.normalize(z))

    return glm.mat4x4(
      glm.vec4(glm.normalize(x), 0.0),
      glm.vec4(glm.normalize(y), 0.0),
      glm.vec4(glm.normalize(z), 0.0),
      glm.vec4(0.0, 0.0, 0.0, 1.0)
    )
  
  @staticmethod
  def vec3_to_vec4(points):
    l = []
    i = 0
    while i < len(points):
      l.append(points[i])
      l.append(points[i+1])
      l.append(points[i+2])
      l.append(0.0)
      i = i + 3    
    return l
  
  @staticmethod
  def get_m_and_mins(points):
    lx = []
    ly = []
    lz = []
    i = 0
    while i < len(points)/3:
      lx.append(points[3*i])
      ly.append(points[3*i+1])
      lz.append(points[3*i+2])
      i +=1
    Mx = max(lx) - min(lx)
    My = max(ly) - min(ly)
    Mz = max(lz) - min(lz)

    return (max([Mx, My, Mz]), min(lx), min(ly), min(lz))
  
  @staticmethod
  def normalize_line(params, points):
    i = 0
    while i < len(points)/3:
      points[3*i] = (points[3*i] - params[1])/params[0]
      points[3*i+1] = (points[3*i + 1] - params[2])/params[0]
      points[3*i+2] = (points[3*i + 2] - params[3])/params[0]
      i +=1

  @staticmethod
  def read_file(camera, thickness):
    lines = []
    coords = []
    props = []
    f = open("PITUBA_IMEX_STRMLN_120.txt", "r")
    while(True):
      c = f.readline()
      if not c:
        break
      l = c.split()
      if l and l[0] == "VCOUNT":
        i = 0
        while i < int(l[1]):
          line = f.readline()
          nums = line.split()
          coords.append(float(nums[0].strip(',')))
          coords.append(float(nums[1].strip(',')))
          coords.append(float(nums[2].strip(',')))
          i +=1
        c = f.readline()
        l = c.split()
        if l and l[0] == "PROP":
          i = 0
          while i < int(l[2]):
            line = f.readline()
            num = line.split()
            props.append(float(num[0].strip(',')))
            i +=1
          lines.append(Line(coords, props, camera, thickness=thickness))
    f.close()
    return lines


    

  