import rclpy
from .topicService import TopicService


class RosHandler:
    def __init__(self):
        self.rate = 1
        self.connected = False

    def connect(self, node: str, rate: int):
        """
        Create and connect to node

        Parameters
        ----------
        node: str
            The name of the ROS2 Node to be created, run, and shut down (after running)
        rate: int
            The name 
        """
        rclpy.init()
        self.node = rclpy.create_node(node)
        self.rate = rclpy.rate.Rate(rate)
        self.connected = True
        self.node.get_logger().info("ROS 2 Node is up ...")
        try:
            rclpy.spin(self.node)
        finally:
            self.node.destroy_node()


    def disconnect(self):
        if self.connected:
            self.node.get_logger.info("shutting down ROS2 Node ...")
            rclpy.shutdown()
            self.connected = False

    @staticmethod
    def topic_publisher(topic: TopicService):
        node = rclpy.create_node(topic.get_name())
        pub = node.create_publisher(topic.get_type(), topic.get_name, 10)
        pub.publish(topic.get_data())
        # print("published to " + topic.get_name())

    @staticmethod
    def topic_subscriber(topic: TopicService, callback=None):
        node = rclpy.create_node(topic.get_name())
        if function == None:
            function = topic.set_data
        node.create_subscription(topic.get_type(), topic.get_name(), callback, 10)

    @staticmethod
    def service_caller(service: TopicService, timeout=30):
        # https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html#writing-a-simple-service-and-client-python
        node = rclpy.create_node(service.get_name())
        try:
            srv = service.get_name()
            typ = service.get_type()
            data = service.get_data()

            node.get_logger.info(f"waiting for ROS2 service: {srv}")
            srv_client = node.create_client(typ, srv)

            while not srv_client.wait_for_service(timeout_sec=1.0):
                node.get_logger().info('service not available, waiting again...')

            node.get_logger.info(f"ROS service is up:{srv}")
            
            resp = srv_client.call_async(data)
            return resp
        
        except rclpy.KeyError as e:
            node.get_logger.info(f"error: {e}")
        except Exception as e:
            node.get_logger().info("Service call failed %r" % (e, ))
        except KeyError as e:
            node.get_logger().info("ERROR:", e)
        return None
    # do we need something like spin_until_future_complete()
