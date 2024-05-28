import math
from OpenGL.GL import *
import numpy as np

class Preferences:
    thickness = 0.1
    subdivision = 0.1

    def set_curve_thickness(self, shader, value):
        shader.set_uniform("thickness",value)
        Preferences.thickness = value

    def set_subdivision(self, shader, value):
        shader.set_uniform("subdivision",value)
        Preferences.subdivision = value
    

