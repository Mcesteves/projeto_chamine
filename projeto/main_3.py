from OpenGL.GL import *
import glfw
#import numpy as np

from camera import *
from shader import *
from curve import*

def initialize (win):
  glClearColor(0,0,0,1)
  glEnable(GL_DEPTH_TEST)
  #glEnable(GL_CULL_FACE)

  global curve
  curve = Curve([
     0.0, 0.0, 0.0,
     0.0, 0.0, 0.0,
     2.0, 2.0, 0.0,
     2.0, 5.0, 0.0,
     5.0, 6.0, 2.0,
     3.0, 3.0, 0.0,
     1.0, 1.0, 0.0,
     1.0, 1.0, 0.0])
  global camera
  camera = Camera(0.0, 0.0, 17.0)
  arcball = camera.create_arcball()
  arcball.attach(win)

  global shader
  shader = Shader()
  shader.attach_vertex_shader("shader/vertex.glsl")
  shader.attach_tesselation_shader("shader/control_4.glsl", "shader/evaluation_3.glsl")
  shader.attach_fragment_shader("shader/fragment.glsl")
  shader.link()  

def display ():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  shader.use_program()
  global stack
  stack = [glm.mat4(1.0)]  
  mv = stack[-1]
  if shader.get_lightning_space() == "camera":
     mv = camera.get_view_matrix() * mv
  mn = glm.transpose(glm.inverse(mv))
  mvp = camera.get_projection_matrix() * mv * stack[-1]
  shader.set_uniform("mvp",mvp)
  shader.set_uniform("mv",mv)
  shader.set_uniform("mn",mn)

  curve.draw()

def resize(win, width, height):
   glViewport(0, 0, width, height)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)

    win = glfw.create_window(800, 600, "Projeto Final", None, None)
    glfw.set_framebuffer_size_callback(win, resize)

    if not win:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(win)

    
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize(win)

    # Loop until the user closes the window
    while not glfw.window_should_close(win):
        # Render here, e.g. using pyOpenGL
        display()

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()