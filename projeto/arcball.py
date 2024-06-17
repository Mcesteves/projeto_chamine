import math
import glm
from OpenGL.GL import *
import glfw

class Arcball:
  def __init__ (self, distance):
    self.distance = distance
    self.x0 = 0
    self.y0 = 0
    self.mat = glm.mat4(1)

  def attach (self, win):
    def cursorpos (win, x, y):
      win_w, win_h = glfw.get_window_size(win)
      fb_w, fb_h = glfw.get_framebuffer_size(win)
      x = x * fb_w / win_w
      y = (win_h - y) * fb_h / win_h
      self.accumulate_mouse_motion(x,y)
    def cursorinit (win, x, y):
      win_w, win_h = glfw.get_window_size(win)
      fb_w, fb_h = glfw.get_framebuffer_size(win)
      x = x * fb_w / win_w
      y = (win_h - y) * fb_h / win_h
      self.init_mouse_motion(x,y)
      glfw.set_cursor_pos_callback(win,cursorpos)
    def dummy (win, x, y):
      pass
    def mousebutton (win, button, action, mods):
      if action == glfw.PRESS:
        glfw.set_cursor_pos_callback(win,cursorinit)  # cursor position callback
      else:
        glfw.set_cursor_pos_callback(win,dummy)        # callback disabled
    def mousewheel(win, xoffset, yoffset):
      if yoffset > 0:
        self.__zoom(1.02)
      elif yoffset < 0:
        self.__zoom(1.0/1.02)

    glfw.set_mouse_button_callback(win,mousebutton)
    glfw.set_scroll_callback(win, mousewheel)

  def init_mouse_motion (self, x0, y0):
    self.x0 = x0
    self.y0 = y0

  def accumulate_mouse_motion (self, x, y):
    vp = glGetIntegerv(GL_VIEWPORT)
    if x==self.x0 and y==self.y0:
      return
    ux, uy, uz = self.__map(vp[2], vp[3], self.x0, self.y0)
    vx, vy, vz = self.__map(vp[2], vp[3], x, y)
    self.x0 = x
    self.y0 = y
    ax = uy*vz - uz*vy
    ay = uz*vx - ux*vz
    az = ux*vy - uy*vx
    theta = 2*math.asin(math.sqrt(ax*ax+ay*ay+az*az)) 
    m = glm.mat4(1)
    m = glm.translate(m,glm.vec3(0,0,-self.distance))
    m = glm.rotate(m,theta,glm.vec3(ax,ay,az))
    m = glm.translate(m,glm.vec3(0,0,self.distance))
    self.mat = m * self.mat

  def get_matrix (self):
    return self.mat
  
  def translate (self, dx, dy, dz):
    m = glm.mat4(1)
    m = glm.translate(m,glm.vec3(dx*self.distance,dy*self.distance,dz*self.distance))
    self.mat = m * self.mat

   # Map function: from screen (x,y) to unit sphere (px,py,pz)
  def __map (self, width, height, x, y):
    if width < height:
      r = width/2
    else:
      r = height/2
    X = (x - width/2) / r
    Y = (y - height/2) / r
    l = math.sqrt(X*X + Y*Y)
    if l <= 1:
      Z = math.sqrt(1 - l*l)
    else:
      X /= l
      Y /= l
      Z = 0
    return (X,Y,Z)
  
  def __zoom(self, scale):
    m = glm.mat4(1)
    m = glm.translate(m,glm.vec3(0,0,-self.distance))
    m = glm.scale(m,glm.vec3(scale, scale, scale))
    m = glm.translate(m,glm.vec3(0,0,self.distance))
    self.mat = m * self.mat
