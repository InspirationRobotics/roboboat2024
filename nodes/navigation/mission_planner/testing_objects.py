#testing functionality of the classes within "floating_objects"

from floating_objects import Object_Colors, Object_Types, Floating_Object
import matplotlib.pyplot as plt
import numpy as np
#import rospy
#from std_msgs.msg import Float32MultiArray

def create_list(bouyes_loc):
    item_list = []
    for i in range(np.shape(bouyes_loc)[1]):
        item_list.append(Floating_Object(Object_Colors.RED,bouyes_loc[0,i],Object_Types.BOUY))
        item_list.append(Floating_Object(Object_Colors.GREEN,bouyes_loc[1,i],Object_Types.BOUY))
    
    return item_list

def create_list_color(bouyes_loc, an_object_color):
    item_list = []
    for i in range(np.shape(bouyes_loc)[0]):
        item_list.append(Floating_Object(an_object_color,bouyes_loc[i],Object_Types.BOUY))
    return item_list    
