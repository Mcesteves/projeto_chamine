import math
from OpenGL.GL import *
import numpy as np
import glm

from shader import Shader
from utils import *

class Line ():
  def __init__(self, points, colors, camera, thickness = 0.05, subdivision = 4, curve_percent = 0.15, cylinder_percent = 0.1):
    
    if camera == None:
       print("Erro")
       return
    
    self.camera = camera
    self.__set_shader__()
    self.set_line_thickness(thickness)
    self.set_percent(curve_percent)
    self.set_subdivision(subdivision)
    self.set_cylinder_percent(cylinder_percent)

    self.indices = []
    self.points = []
    self.angles = []
    # results = Utils.get_m_and_mins(points)
    # Utils.normalize_line(results, points)
    self.points = points
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

  def set_line_thickness(self, value):
        if self.sh:
            self.sh.set_uniform("thickness",value)
            self.thickness = value

  def set_subdivision(self,value):
      if self.sh:
          self.sh.set_uniform("subdivision",value)
          self.subdivision = value

  def set_percent(self, value):
      if self.sh:
          if value > 0.5:
              value = 0.5
          if value < 0.05:
              value = 0.05
          self.sh.set_uniform("curve_percent", value)
          self.curve_percent = value
  
  def set_cylinder_percent(self, value):
      if self.sh:
          if value > 0.9:
              value = 0.9
          if value < 0.01:
              value = 0.01
          self.sh.set_uniform("cylinder_percent", value)
          self.cylinder_percent = value

  def get_line_thickness(self):
      return self.thickness
    
  def get_subdivision(self):
      return self.subdivision
  
  def get_shader(self):
      return self.sh
  
  def get_percent(self):
      return self.curve_percent
  
  def draw(self):
    self.sh.use_program()
    stack = [glm.mat4(1.0)]  
    mv = stack[-1]
    if self.sh.get_lightning_space() == "camera":
      mv = self.camera.get_view_matrix() * mv
    mn = glm.transpose(glm.inverse(mv))
    mvp = self.camera.get_projection_matrix() * mv * stack[-1]
    self.sh.set_uniform("mvp", mvp)
    self.sh.set_uniform("mv", mv)
    self.sh.set_uniform("mn", mn)

    glBindVertexArray(self.vao)
    glDrawElements(GL_PATCHES, self.indices.size, GL_UNSIGNED_INT, None)

  ######################## Private methods ########################
  def __set_shader__(self):
    self.sh = Shader()
    self.sh.attach_vertex_shader("shader/vertex.glsl")
    self.sh.attach_tesselation_shader("shader/control_5.glsl", "shader/evaluation_4.glsl")
    self.sh.attach_fragment_shader("shader/fragment.glsl")
    self.sh.link() 
    self.sh.use_program()

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
        if id == len(self.points)/3 - 4:
          self.indices.append(id+3)
          self.indices.append(id+3)
        elif id == len(self.points)/3 - 3:
          self.indices.append(id+2)
          self.indices.append(id+2)
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

    id = 0
    angle_sum = 0
    while id <= len(self.indices)//5 - 2:
      p0 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5]))
      p1 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 1]))
      p2 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 2]))
      p3 = glm.vec3(self.__get_point_from_idx__(self.indices[id*5 + 3]))
      angle = self.__calculate_angle__(p0, p1, p2, p3, id)
      angle_sum += angle
      self.angles.append(angle_sum)
      id += 1

    self.matrices.clear()

  def __calculate_angle__(self, p0, p1, p2, p3, id):

    #calculo de dois pontos do toro do ramo atual
    v1 = glm.vec3(p1 - p0)
    v2 = glm.vec3(p2 - p1)
    v3 = glm.vec3(p3 - p2)

    theta = 0
    in_radius = self.thickness

    d2 = min(self.curve_percent*glm.length(v2), self.curve_percent*glm.length(v3))
    height = glm.length(v2)

    torus_angle = Utils.calculate_torus_angle(v2,v3)
    torus_point = 0 
    torus_center = 0
    if torus_angle == 0:
      torus_point = self.matrices[id]*glm.vec4(-in_radius, height, 0, 1)
      torus_center = self.matrices[id]*glm.vec4(0,height,0,1)
    else:

      R = d2*(1/math.tan(torus_angle/2))

      phi = (1/(1.0-0.1))*torus_angle*(1.0 - 0.1)

      x = -(-R + (R + in_radius)*math.cos(phi))
      y = height - d2 + (R + in_radius)*math.sin(phi)
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
    cylinder_top = self.matrices[id+1]*glm.vec4(0,glm.length(v3),0,1)

    vec1 = torus_point - torus_center
    vec2 = cylinder_point - cylinder_center

    angle = Utils.calculate_torus_angle(vec1, vec2)
 
    # x = -in_radius * math.cos(angle)
    # y = d2
    # z = in_radius * math.sin(angle)
    # w = 1.0

    # new_point = self.matrices[id+1]*glm.vec4(x,y,z,w)
    
    # print("torus_point")
    # print(torus_point)
    # print("torus_center")
    # print(torus_center)
    # print("cylinder_point")
    # print(cylinder_point)
    # print("cylinder_center")
    # print(cylinder_center)
    # print("new_point_positivo")
    # print(new_point)
    # x = -in_radius * math.cos(-angle)
    # y = d2
    # z = in_radius * math.sin(-angle)
    # w = 1.0

    # new_point = self.matrices[id+1]*glm.vec4(x,y,z,w)
    # print("new_point_negativo")
    # print(new_point)
    # print("\n")

    cross = glm.cross(glm.normalize(glm.vec3(vec2)),glm.normalize(glm.vec3(vec1)))
    cylinder_dir = cylinder_top - cylinder_point
    signal = glm.dot(glm.normalize(glm.vec3(cylinder_dir)), cross)
    if signal >= 0:
      # print("positivo")
      # print("\n")
      return angle
    else:  
      # print("negativo")
      # print("\n")
      return -angle
    
  def __add_coord_to_point__(self, point, angle):
    return (point.x, point.y, point.z, angle)
  
  def __build_points_array__(self):
    i = 0
    while i < len(self.indices)/5 - 1:
      index = self.indices[5*i+2]
      self.points[index*4+3] = self.angles[i]
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

  
  
