from OpenGL.GL import *
import glfw

from camera import *
from line import *
from preferences import *
from shader import *

def initialize (win):
  glClearColor(0,0,0,1)
  glEnable(GL_DEPTH_TEST)
  #glPolygonMode(GL_FRONT, GL_LINE)
  #glEnable(GL_CULL_FACE)
  #glCullFace(GL_FRONT); 
  
  global camera
  camera = Camera(0.0, 0.0, 15.0)
  arcball = camera.create_arcball()
  arcball.attach(win)

  global shader
  shader = Shader()
  shader.attach_vertex_shader("shader/vertex.glsl")
  shader.attach_tesselation_shader("shader/control_5.glsl", "shader/evaluation_4.glsl")
  shader.attach_fragment_shader("shader/fragment.glsl")
  shader.link() 
  shader.use_program()

  global preferences
  preferences = Preferences(shader)

  global curve
  curve = Line([
     0.0, 0.0, -8.0,
     0.0, 0.0, -4.0,
     0.0, 0.0, 1.0,
     0.0, 0.0, 3.0,
     0.0, 0.0, 4.0,
     0.0, 0.0, 6.0,
     0.0, 2.0, 4.0,
     0.0, 4.0, 3.0,
     2.0, 4.0, 0.0,
    #  6.0, -10.0, 2.0,
    #  0.0, 0.0, 0.0,
    #  -8.0, 1.0, 3.0,
    #  -5.0, 0.0, 0.0,
    #  -10, -6.0, 5.0,
    #  5.0, -3.0, -5.0,
    #  1.0, 7.0, 9.0,
    #  2.0, 1.0, 15.0,
    #  2.0, 5.0, 0.0,
    #  2.0, 8.0, 0.0,
    #  2.0, -2.0, 0.0,
    #  -2.0, -1.0, 0.0,
     ],
     [
     1.0, 0.0, 0.0, 1.0,
     1.0, 1.0, 0.0, 1.0,
     1.0, 0.0, 1.0, 1.0,
     0.0, 1.0, 0.0, 1.0,
     0.0, 0.0, 1.0, 1.0,
     1.0, 0.0, 0.0, 1.0,
     0.2, 0.7, 0.5, 1.0,
     0.4, 1.0, 0.2, 1.0,
     0.0, 0.0, 1.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0
     ])
  
#   global curve1
#   curve1 = Line([
#      0.0, 0.0, 0.0,
#      1.0, 0.0, 0.0,
#      3.0, 3.0, 2.0, 
#      -1.0, 0.0, 0.0,
#      2.0, 1.0, 3.0,
#      2.0, 4.0, 0.0,
#      -9.0, 5.0, 0.0,
#      -14.0, 3.0, -5.0,
#      -5.0, 4.0, 0.0,
#      2.0, -6.0, 2.0
#      ])
  
  preferences.set_line_thickness(0.08)
  preferences.set_subdivision(16)

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
  #curve1.draw()

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