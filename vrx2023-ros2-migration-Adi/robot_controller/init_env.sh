echo "=== init_env tool ==="
echo ">> Configuring ROS development environment"
echo ">> If this script fails, message Sean"

if [ ! -d /opt/ros/noetic ]; then
	echo "ROS Noetic installation not found!"
	echo "Exiting..."
	exit
fi

# setup ros environment
echo "Setting up ROS..."
source /opt/ros/noetic/setup.bash

echo "Setting up ROS package path"
if [ ! -d ./pkg ]; then
	echo "\"pkg\" folder not found. Creating..."
	mkdir pkg
fi
ROS_PACKAGE_PATH="$PWD/pkg/"

echo "Finished! :D"
