import glm
import math
from OpenGL.GL import *

class Camera ():
  def __init__(self, x, y, z):
    self.ortho = False
    self.fov_y = 45
    self.z_near = 0.1
    self.z_far = 1000
    self.center = glm.vec3(0,0,0)
    self.eye = glm.vec3(x,y,z)
    self.up = glm.vec3(0,1,0)
    self.arcball = None
    #self.reference = None

  def set_angle (self, fov_y):
    self.fov_y = fov_y

  def get_angle (self):
    return self.fov_y
  
  def set_z_planes (self, z_near, z_far):
    self.z_near = z_near
    self.z_far = z_far

  def set_center (self, x, y, z):
    self.center = glm.vec3(x, y, z)

  def get_center (self):
    return self.center
  
  def set_eye (self, x, y, z):
    self.eye = glm.vec3(x, y, z)

  def get_eye (self):
    return self.eye
  
  def set_ortho (self, boolean):
    self.ortho = boolean

  def create_arcball (self):
    from arcball import Arcball
    d = glm.length(self.eye-self.center)
    self.arcball = Arcball(d)
    return self.arcball

  def get_arcball (self):
    return self.arcball
  
  def get_projection_matrix (self):
    viewport = glGetIntegerv(GL_VIEWPORT)
    ratio = viewport[2]/viewport[3]
    if not self.ortho:
      return glm.perspective(glm.radians(self.fov_y),ratio,self.z_near,self.z_far)
    else:
      dist = glm.distance(self.eye,self.center)
      height = dist * math.tan(glm.radians(self.fov_y)/2.0)
      width = height / viewport[3] * viewport[2]
      return glm.ortho(-width,width,-height,height,self.z_near,self.z_far)

  def get_view_matrix (self):
    view = glm.mat4(1.0)
    if self.arcball: 
      view = view * self.arcball.get_matrix()
    view = view * glm.lookAt(self.eye,self.center,self.up)
    return view