# from OpenGL.GL import *
# import numpy as np
# import glm

# from cylinder import *

# class Curve ():
#   def __init__(self, points):
#     #self.cylinders = []
#     self.matrices = []
#     #tratamento dos pontos
#     points = self.__remove_repeated_sequence__(points)
#     self.__add_begin_end__(points)
#     self.points = points

#     i = 0
#     id = 0
#     while i < len(self.points) - 11:
#       v0 = glm.vec3(self.points[i+3], self.points[i+4], self.points[i+5])
#       v1 = glm.vec3(self.points[i+6], self.points[i+7], self.points[i+8])
#       v2 = glm.vec3(self.points[i+6], self.points[i+7], self.points[i+8])
#       self.matrices.append(self.__set_transformation__(v0, v1, v2, id))

#     #Forma anterior utilizando a Classe cilindro
#     #   cylinder = Cylinder(np.array([self.points[i], self.points[i+1], self.points[i+2],
#     #      self.points[i+3], self.points[i+4], self.points[i+5],
#     #      self.points[i+6], self.points[i+7], self.points[i+8],
#     #      self.points[i+9], self.points[i+10], self.points[i+11]], dtype = 'float32'))
#     #   self.cylinders.append(cylinder)
#       i = i + 3
#       id += 1

#   #Remove pontos adjacentes iguais
#   def __remove_repeated_sequence__(self, points):
#     l = []
#     i = 0
#     while i < len(points) - 3:
#       if((points[i], points[i+1], points[i+2]) != (points[i+3], points[i+4], points[i+5])):
#         l.append(points[i])
#         l.append(points[i+1])
#         l.append(points[i+2])
#       i = i + 3    
#     l.append(points[i])
#     l.append(points[i+1])
#     l.append(points[i+2])
#     return l
  
#   #Repete os pontos de inicio e fim na sequencia
#   def __add_begin_end__(self, points):
#     points.insert(0, points[0])
#     points.insert(1, points[2])
#     points.insert(2, points[4])
#     points.append(points[len(points) - 3])
#     points.append(points[len(points) - 3])
#     points.append(points[len(points) - 3])

#   #calcula matriz de translacao
#   def __set_translation_matrix__(self, v0, v1, id):
#     t = v1
#     if id != 0:
#       t = v1 - v0

#     return glm.mat4x4(
#         glm.vec4(1.0, 0.0, 0.0, 0.0),
# 		    glm.vec4(0.0, 1.0, 0.0, 0.0),
# 		    glm.vec4(0.0, 0.0, 1.0, 0.0),
# 		    glm.vec4(t.x, t.y, t.z, 1.0)
#       )

#   #calcula matriz de rotacao
#   def __set_rotation_matrix__(self, v0, v1, v2):

#       y = v1 - v0
#       x = v2 - v1

#       z = glm.cross(glm.normalize(x), glm.normalize(y))
#       if glm.equal(glm.vec3(0.0), z):
#         z = glm.cross(glm.normalize(x), glm.normalize(glm.vec3(-x.y, x.x, 0)))
      
#       x = glm.cross(glm.normalize(y), z)

#       return glm.mat4x4(
#         glm.vec4(glm.normalize(x), 0.0),
#         glm.vec4(glm.normalize(y), 0.0),
#         glm.vec4(glm.normalize(z), 0.0),
#         glm.vec4(0.0, 0.0, 0.0, 1.0)
#       )
  
#   #calcula matriz de transformacao que sera usada no shader
#   def __set_transformation__(self, v0, v1, v2, id):
#     if id == 0:
#       translation = self.__set_translation_matrix__(v0, v1, id)
#       rotation = self.__set_rotation_matrix__(v0, v1, v2)
#       return translation * rotation
#     else:
#       new_v0 = glm.vec3(self.matrices[id-1] * glm.vec4(v0, 0))
#       new_v1 = glm.vec3(self.matrices[id-1] * glm.vec4(v1, 0))
#       new_v2 = glm.vec3(self.matrices[id-1] * glm.vec4(v2, 0))
#       translation = self.__set_translation_matrix__(new_v0, new_v1, id)
#       rotation = self.__set_rotation_matrix__(new_v0, new_v1, new_v2)

#       return translation * rotation * self.matrices[id-1]

#   # def draw(self):
#   #   for c in self.cylinders:
#   #     c.draw()