from OpenGL.GL import *
import glfw
import numpy as np

from camera import *
from shader import *
from curve import*

def initialize ():
  glClearColor(0,0,0,1)
  glEnable(GL_DEPTH_TEST)

  global curve
  curve = Curve([1.0, -1.0, 1.0,
     2.0, 0.0, 0.0,
     4.0, 3.0, 0.0,
     3.0, 3.0, 0.0,
     -2.0, 1.0, 1.0])
  global camera
  camera = Camera(1.0, 0.0, 16.0)
  global shader
  shader = Shader()
  shader.attach_vertex_shader("shader/vertex.glsl")
  shader.attach_tesselation_shader("shader/control.glsl", "shader/evaluation.glsl")
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

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)

    win = glfw.create_window(600, 800, "Cilindro Básico", None, None)

    if not win:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(win)

    
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize()

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