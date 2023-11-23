# Roboboat Jetson Xavier NX Docker Guide
### Running the docker

```bash
sudo docker run --runtime nvidia -it --rm --network=host roboboat_humble:l4t-r35.4.1
```

View installed packages:

```bash
# need to be inside the docker
apt list
```


Source `ros2` everytime before you're using it.

```bash
source /opt/ros/humble/install/setup.bash
```