from OpenGL.GL import *
import numpy as np

from cylinder import *

class Curve ():
  def __init__(self, points):
    points = self.__remove_repeated_sequence__(points)
    self.__add_begin_end__(points)
    self.cylinders = []
    self.points = points
    print(self.points)
    i = 0
    while i < len(self.points) - 11:
      cylinder = Cylinder(np.array([self.points[i], self.points[i+1], self.points[i+2],
         self.points[i+3], self.points[i+4], self.points[i+5],
         self.points[i+6], self.points[i+7], self.points[i+8],
         self.points[i+9], self.points[i+10], self.points[i+11]], dtype = 'float32'))
      self.cylinders.append(cylinder)
      i = i + 3

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
  
  def __add_begin_end__(self, points):
    points.insert(0, points[0])
    points.insert(1, points[2])
    points.insert(2, points[4])
    points.append(points[len(points) - 3])
    points.append(points[len(points) - 3])
    points.append(points[len(points) - 3])
  

  def draw(self):
    for c in self.cylinders:
      c.draw()