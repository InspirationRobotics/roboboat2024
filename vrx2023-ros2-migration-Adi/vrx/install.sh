echo "VRX Gazebo Installer"
echo "> contact Sean if u have issues using this"

printf "Continue with installation? (y/n) "
read CONTINUE

if [ $CONTINUE == "y" ]; then

	echo "Installing..."

	if [ -d vrx_ws ]; then
		rm -rf vrx_ws
	fi

	mkdir -p vrx_ws/src/
	git clone https://github.com/osrf/vrx.git vrx_ws/src/vrx

	cd vrx_ws/
	source /opt/ros/noetic/setup.bash
	catkin_make
	cd ..

	echo "Complete"


else

	echo "Cancelling installation"

fi
