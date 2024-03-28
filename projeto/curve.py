from OpenGL.GL import *
import numpy as np

from cylinder import *

class Curve ():
  def __init__(self, points):
    self.cylinders = []
    self.points = points
    i = 0
    while i < len(self.points) - 8:
      cylinder = Cylinder(np.array([self.points[i], self.points[i+1], self.points[i+2],
         self.points[i+3], self.points[i+4], self.points[i+5],
         self.points[i+6], self.points[i+7], self.points[i+8]], dtype = 'float32'))
      # cylinder = Cylinder(np.array([self.points[i], self.points[i+1], self.points[i+2],
      #    self.points[i+3], self.points[i+4], self.points[i+5]], dtype = 'float32'))
      # print(np.array([self.points[i], self.points[i+1], self.points[i+2],
      #    self.points[i+3], self.points[i+4], self.points[i+5],
      #    self.points[i+6], self.points[i+7], self.points[i+8]], dtype = 'float32'))
      self.cylinders.append(cylinder)
      i = i + 3

  def draw(self):
    for c in self.cylinders:
      c.draw()