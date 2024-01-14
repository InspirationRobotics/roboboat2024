import sys
from floating_objects import Object_Colors, Object_Types, Floating_Object

class mission_template():
    def __init__(self, floating_objects, envmap):
        self.floating_objects = floating_objects
        self.envmap = envmap
    
    def ready_for_mission(self, floating_objects = None, envmap = None):
        pass
    
    def estimate_path(self, start_point):
        pass

    def update_floating_objects(self, floating_objects):
        pass
    
    def update_map(self, envmap):
        pass
    
    def update_path(self, start_point, floating_objects, envmap):
        pass

    def check_done(self, start_point):
        pass