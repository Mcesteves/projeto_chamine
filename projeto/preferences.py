import math
from OpenGL.GL import *
import numpy as np

class Preferences:
    __instance = None

    def __new__(cls, shader):
        if Preferences.__instance is None:
          Preferences.__instance = super().__new__(cls)
        return Preferences.__instance

    def __init__(self, shader):
        if not shader:
            print("É preciso passar um shader como argumento")
        self.thickness = 0.05
        self.subdivision = 16
        self.sh = shader
        self.sh.set_uniform("thickness",self.thickness)
        self.sh.set_uniform("subdivision",self.subdivision)

    def set_curve_thickness(self, value):
        if self.sh:
            self.sh.set_uniform("thickness",value)
            self.thickness = value

    def set_subdivision(self,value):
        if self.sh:
            self.sh.set_uniform("subdivision",value)
            self.subdivision = value

    def get_curve_thickness(self):
        return self.thickness
    
    def get_subdivision(self):
        return self.subdivision
    
    def get_shader(self):
        return self.sh
    
    def get_instance():
        return Preferences.__instance

    

