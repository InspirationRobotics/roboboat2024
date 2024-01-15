import rclpy
from rclpy.node import Node
from grid import *
from transform import *

from obj_msg.msg import Objlst
from obj_msg.msg import Obj
from dist_msg.msg import Dist
from vision_msgs.msg import Detection2DArray

from time import sleep

d = []
bb = []

class Mapper(Node):

    def __init__(self):
        super().__init__('mapper')
        self.dist_subscription = self.create_subscription(
            Dist,
            '/distances',
            self.dist_callback,
            1)
        self.dist_subscription  # prevent unused variable warning

        self.bbox_subscription = self.create_subscription(
            Detection2DArray,
            '/right_set/bbox',
            self.bbox_callback,
            1)
        self.bbox_subscription
        self.dist_subscription

    def dist_callback(self, msg):
        global d
        d = msg
        
    def bbox_callback(self, msg):
        global bb
        bb = msg

def determine_gate_ids():
    buoys = []
    buoys.append(mk_obj("greenbuoy", "nil", "nil", [0, 0], 0))
    buoys.append(mk_obj("greenbuoy", "nil", "nil", [0, 0], 0))
    
    gb1_pose = [0, 0]
    gb2_pose = [0, 0]

    g_sightings1 = 0
    g_sightings2 = 0
    
    for i in grid:
        for j in i:
            pass
    
def main(args=None):
    global d
    global bb
    rclpy.init(args=args)

    mapper = Mapper()
    grid = mk_grid(12, 12)

    gps_origin = [3, 3]
    gps_coords = [5 / 111000 + 3, 5 / 111000 + 3]
    heading = PI / 2
    map_orientation = PI / 4
    
    while (rclpy.ok()):
        if (bb != [] and d != []):
            if d.count == len(bb.detections):
                centers = []
                for i in bb.detections:
                    centers.append(i.bbox.center.x)
                    
                types = []
                for i in d.obj_classes:
                        types.append(i)
                        
                distances = []
                for i in d.distances:
                            distances.append(i)

                print("dist: ")
                print(distances)
                print("type: ")
                print(types)
                print("centers: ")
                print(centers)
                #place_objs_in_map(
                #    find_relative_objs([5], [1080], ["blue"], 2 * PI / 3, 1080),
                #    map_pos(gps_coords, gps_origin, map_orientation),
                #    map_hdg(heading, map_orientation),
                #    grid
                #)
                rel_objs = []
                for i in range(0, len(distances)):
                    pose = calc_rel_pose(distances[i], centers[i], 120, 1080)
                    o = mk_obj(types[i], "nil", "nil", pose, 0)
                    rel_objs.append(o)

                    
                obj_poses = []
                for i in rel_objs:
                    new_p = obj_pos(i.get("pose"), map_hdg(heading, map_orientation),
                                    map_pos(gps_to_m(gps_coords, gps_origin), map_orientation))

                    o = mk_obj(i.get("type"), i.get("id"), i.get("mission"), new_p, 0)
                    obj_poses.append(o)

                print(obj_poses)
                for i in obj_poses:
                    add_obj(i)
                    
                    
                            
                #print(grid)

        #gate_objs = determine_gate_ids()
        # publish(gate_objs)

        rclpy.spin_once(mapper)
        sleep(1)
            
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

