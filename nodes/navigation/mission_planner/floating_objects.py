# contains classes for the mapping of mission models
from enum import IntEnum, Enum
class Object_Colors(IntEnum):
    # used in the coloring of the matplotlib
    RED = 15
    GREEN = 80
    WHITE = 3
    BLACK = 4
    PURPLE = 33

class Object_Types(IntEnum):
    BOUY = 1
    OBSTACLE = 2    
    LIGHT_TOWER = 3
    DRONE_LANDING_PAD = 4
    RACQUET_BALL_TARGET = 5
    WILDLIFE_PLATYPUS = 6
    WILDLIFE_CROCODILE = 7
    WILDLIFE_TURTLE = 8
    BEACON = 9


class Floating_Object:
    def __init__(self, color, location, type):
        self.id = None
        self.color = color
        self.location = location #x,y 
        self.seen_flag = False
        self.confidence = 0.1
        self.type = type #from object_types

    def set_id(self, id):
        self.id = id

    def get_json(self):
        ret = '{'
        ret += '"id":"' + str(self.id) + '"'
        ret += ', "cl":"' + str(self.color.name) +'"'
        ret += ', "x":' + str(self.location[0]) 
        ret += ', "y":' + str(self.location[1])
        ret += ', "sf":"' + str(self.seen_flag)+'"'
        ret += ', "conf":' + str(self.confidence)
        ret += ', "type":"' + str(self.type.name) +'"'
        ret += '}'
        return ret


    def output(self):
        return self.id, self.color, self.location, self.seen_flag, self.confidence, self.type

    

