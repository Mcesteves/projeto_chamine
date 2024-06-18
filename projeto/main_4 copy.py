from OpenGL.GL import *
import glfw

from camera import *
from line import *

def initialize (win):
  glClearColor(0,0,0,1)
  glEnable(GL_DEPTH_TEST)
  glPolygonMode(GL_FRONT, GL_LINE)
  #glEnable(GL_CULL_FACE)
  #glCullFace(GL_FRONT); 

  Utils.read_file()

  global camera
  camera = Camera(0, 0, 15)
  arcball = camera.create_arcball()
  arcball.attach(win)

  global curve
  curve = Line([     
     0.0, 0.0, 0.0,
     0.0, 0.0, 2.0,
     0.0, 0.0, 5.0,
     0.0, 0.0, 7.0,
     8.0, 1.0, 3.0,
     8.0, 4.0, 0.0,
     -5.0, 8.0, 0.0,
    #  -10.0, 8.0, -5.0,
    #  2.0, 4.0, 0.0,
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
     1.0, 0.0, 0.0, 1.0,
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
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0,
    #  1.0, 0.0, 0.0, 1.0
     ], camera, subdivision=8, thickness=0.2, cylinder_percent=0.9)
  
  

def display ():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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

    
    print("OpenGL version: ", glGetString(GL_VERSION))

    initialize(win)

    prev_time = 0.0
    crnt_time = 0.0
    time_diff = 0.0
    counter = 0

    # Loop until the user closes the window
    while not glfw.window_should_close(win):
        crnt_time = glfw.get_time()
        time_diff = crnt_time - prev_time
        counter += 1
        if time_diff >= 1.0/30.0:
           fps = str((1.0/time_diff)*counter)
           new_title = "Projeto Final - FPS "+ fps
           glfw.set_window_title(win, new_title)
           prev_time = crnt_time
           counter = 0
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        curve.draw()

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()