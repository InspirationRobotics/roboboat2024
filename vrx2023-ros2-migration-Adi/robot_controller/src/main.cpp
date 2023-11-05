#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include "sensor_msgs/Image.h"

// #define STB_IMAGE_WRITE_IMPLEMENTATION
// #include "stb_image_write.h"

#include "pathnavigator.h"
#include <stdio.h>


int main(int argc, char* argv[])
{
	printf("Starting Robot...\n");

	// create node called talker
	ros::init(argc, argv, "talker");
	ros::NodeHandle n;
		
	ros::Rate loopRate(10);

	Path_Navigator navigator;

	init_path_navigator(&navigator, n);


	float m_x, m_y, rot;
	printf("input (x,y,rot): ");
	scanf("%f,%f,%f", &m_x, &m_y, &rot);

	while (ros::ok())
	{
		// std_msgs::Float32 msg;
		// msg.data = 1.0;

		// publisher.publish(msg);

		write_motion_vector(&navigator, m_x, m_y, rot);



		// dont touch this unless u know what ur doing
		ros::spinOnce();
		loopRate.sleep(); // limit while loop speed
	}


	printf("Stopping Robot...\n");

	return 0;
}
