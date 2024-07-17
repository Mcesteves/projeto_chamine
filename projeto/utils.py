import math
from OpenGL.GL import *
import glm
import numpy as np

class Utils:
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
    if(y == glm.vec3(0)):
      y = glm.vec3(0.0, 1.0, 0.0)
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
  def read_file(filename):
    max_prop = None
    min_prop = None
    max_x = None
    min_x = None
    max_y = None
    min_y = None
    max_z = None
    min_z = None
    lines = []
    coords = []
    props = []
    inj_lines = 0
    f = open(filename, "r")
    while(True):
      c = f.readline()
      if not c:
        break
      l = c.split()
      if l and l[0] == "INJ_LINES":
        inj_lines = int(l[1])
      elif l and l[0] == "LINE" and int(l[1]) < inj_lines:
        c = f.readline()
        l = c.split()
        coords = []
        props = []
        i = 0
        while i < int(l[1]):
          line = f.readline()
          nums = line.split()
          coords.append(float(nums[1]))
          max_x = Utils.return_max(max_x, float(nums[1]))
          min_x = Utils.return_min(min_x, float(nums[1]))
          coords.append(float(nums[2]))
          max_y = Utils.return_max(max_y, float(nums[2]))
          min_y = Utils.return_min(min_y, float(nums[2]))
          coords.append(float(nums[3]))
          max_z = Utils.return_max(max_z, float(nums[3]))
          min_z = Utils.return_min(min_z, float(nums[3]))
          i +=1
        c = f.readline()
        l = c.split()
        if l and l[0] == "PROP":
          i = 0
          while i < int(l[2]):
            line = f.readline()
            num = line.split()
            props.append(float(num[1]))
            max_prop = Utils.return_max(max_prop, float(num[1]))
            min_prop = Utils.return_min(min_prop, float(num[1]))
            i +=1
          lines.append([coords, props])
    f.close()
    norm_x = max_x - min_x
    norm_y = max_y - min_y
    norm_z = max_z - min_z
    return (lines, min_prop, max_prop, norm_x, norm_y, norm_z, min_x, min_y, min_z)
  
  @staticmethod
  def normalize_data(data, max_limit):
    lines = data[0]  
    for line_data in lines:
      i = 0
      points = line_data[0]
      props = line_data[1]
      while i < len(points)/3:
        points[3*i] = (points[3*i] - data[6])/data[3]
        points[3*i+1] = (points[3*i + 1] - data[7])/data[4]
        points[3*i+2] = (points[3*i + 2] - data[8])/data[5]
        props[i] = (props[i])/(max_limit)
        i +=1
    return lines
  
  @staticmethod
  def create_color_scale():
    scale = []
    scale.append(0.0)
    scale.append(2.0/255.0)
    scale.append(96.0/255.0)
    scale.append(203.0/255.0)

    scale.append(0.12)
    scale.append(0.0/255.0)
    scale.append(150.0/255.0)
    scale.append(196.0/255.0)

    scale.append(0.26)
    scale.append(67.0/255.0)
    scale.append(174.0/255.0)
    scale.append(57.0/255.0)

    scale.append(0.39)
    scale.append(155.0/255.0)
    scale.append(181.0/255.0)
    scale.append(0.0/255.0)
    
    scale.append(0.50)
    scale.append(207.0/255.0)
    scale.append(184.0/255.0)
    scale.append(42.0/255.0)

    scale.append(0.68)
    scale.append(245.0/255.0)
    scale.append(184.0/255.0)
    scale.append(0.0/255.0)

    scale.append(0.75)
    scale.append(255.0/255.0)
    scale.append(158.0/255.0)
    scale.append(0.0/255.0)

    scale.append(0.83)
    scale.append(255.0/255.0)
    scale.append(128.0/255.0)
    scale.append(0.0/255.0)

    scale.append(0.9)
    scale.append(255.0/255.0)
    scale.append(87.0/255.0)
    scale.append(0.0/255.0)

    scale.append(1.0)
    scale.append(255.0/255.0)
    scale.append(40.0/255.0)
    scale.append(40.0/255.0)

    scale.append(1.5)
    scale.append(200.0/255.0)
    scale.append(200.0/255.0)
    scale.append(200.0/255.0)
    return scale
  
  def return_max(current_max, value):
    if current_max == None:
      return value
    elif current_max < value:
      return value
    else:
      return current_max
    
  def return_min(current_min, value):
    if current_min == None:
      return value
    elif current_min > value:
      return value
    else:
      return current_min
    


    

  