# Folder Structure
```
.
├── Livox-SDK
│   ├── sample
│   │   └── lidar_lvx_file
│   │       └── third_party
│   │           └── rapidxml
│   ├── sdk_core
│   │   └── src
│   │       ├── base
│   │       │   ├── multiple_io
│   │       │   ├── network
│   │       │   │   ├── unix
│   │       │   │   └── win
│   │       │   └── wake_up
│   │       │       ├── unix
│   │       │       └── win
│   │       ├── comm
│   │       ├── command_handler
│   │       ├── data_handler
│   │       └── third_party
│   │           └── FastCRC
│   └── ws_livox
│       ├── devel
│       │   ├── lib
│       │   │   └── camera_lidar_calibration
│       │   └── share
│       │       ├── camera_lidar_calibration
│       │       │   └── cmake
│       │       ├── common-lisp
│       │       │   └── ros
│       │       │       └── livox_ros_driver
│       │       │           └── msg
│       │       ├── cv_bridge
│       │       │   └── cmake
│       │       └── livox_ros_driver
│       │           └── cmake
│       └── src
│           ├── images
│           ├── livox_camera_lidar_calibration
│           │   ├── doc_resources
│           │   ├── launch
│           │   └── src
│           └── livox_ros_driver
│               ├── Livox-SDK
│               │   ├── doc
│               │   │   └── images
│               │   ├── sample
│               │   │   ├── hub
│               │   │   ├── hub_lvx_file
│               │   │   ├── lidar
│               │   │   └── lidar_lvx_file
│               │   │       └── third_party
│               │   │           └── rapidxml
│               │   ├── sample_cc
│               │   │   ├── hub
│               │   │   ├── lidar
│               │   │   ├── lidar_utc_sync
│               │   │   └── trouble_shooting
│               │   └── sdk_core
│               │       ├── include
│               │       │   └── third_party
│               │       │       ├── cmdline
│               │       │       └── spdlog
│               │       │           └── spdlog
│               │       │               ├── details
│               │       │               ├── fmt
│               │       │               │   └── bundled
│               │       │               └── sinks
│               │       └── src
│               │           ├── base
│               │           │   ├── multiple_io
│               │           │   ├── network
│               │           │   │   ├── unix
│               │           │   │   └── win
│               │           │   └── wake_up
│               │           │       └── win
│               │           ├── comm
│               │           ├── command_handler
│               │           ├── data_handler
│               │           └── third_party
│               │               └── FastCRC
│               ├── cmake
│               ├── common
│               │   ├── FastCRC
│               │   ├── comm
│               │   ├── rapidjson
│               │   │   ├── error
│               │   │   ├── internal
│               │   │   └── msinttypes
│               │   └── rapidxml
│               ├── config
│               ├── launch
│               ├── livox_ros_driver
│               │   └── include
│               ├── msg
│               └── timesync
│                   └── user_uart
├── david_code
│   ├── object_detection_projection
│   │   └── src
│   │       ├── dist_msg
│   │       │   └── msg
│   │       └── livox_pcd_projection
│   │           ├── config
│   │           └── livox_pcd_projection
│   ├── rosboard
│   │   └── rosboard
│   │       └── subscribers
│   └── slam
│       └── include
│           └── slam
├── livox_projection
│   └── src
│       ├── dist_msg
│       │   └── include
│       │       └── dist_msg
│       └── livox_pcd_projection
│           ├── livox_pcd_projection
│           └── test
├── livox_ros2_driver
│   └── livox_ros2_driver
│       ├── common
│       │   ├── FastCRC
│       │   └── rapidjson
│       │       └── error
│       ├── launch
│       └── timesync
│           └── user_uart
├── mapper
│   ├── devel
│   │   ├── lib
│   │   │   └── python3
│   │   │       └── dist-packages
│   │   │           └── mapper
│   │   │               └── msg
│   │   └── share
│   │       ├── gennodejs
│   │       │   └── ros
│   │       │       └── mapper
│   │       │           └── msg
│   │       ├── mapper
│   │       │   └── cmake
│   │       └── mission_planner
│   │           └── cmake
│   └── src
│       ├── mapper
│       │   └── msg
│       └── mission_planner
│           └── include
│               └── mission_planner
├── multi_cam_detection
│   └── src
│       └── multi_cam_obj_detection
│           ├── launch
│           ├── multi_cam_obj_detection
│           │   ├── models
│           │   │   └── hub
│           │   └── utils
│           │       ├── aws
│           │       ├── docker
│           │       ├── flask_rest_api
│           │       ├── google_app_engine
│           │       └── loggers
│           │           └── wandb
│           ├── resource
│           └── test
├── project_cloud
│   └── src
│       └── project_cloud
│           ├── project_cloud
│           └── resource
├── pynmeagps-master
│   └── pynmeagps-master
│       ├── examples
│       │   └── webserver
│       └── pynmeagps
├── ros2_mapper
│   └── src
│       ├── mapper
│       │   └── src
│       │       └── redo
│       └── obj_msg
├── vision
│   ├── android
│   │   ├── ops
│   │   │   └── src
│   │   │       └── main
│   │   └── test_app
│   │       └── app
│   │           └── src
│   │               └── main
│   │                   ├── java
│   │                   │   └── org
│   │                   │       └── pytorch
│   │                   │           └── testapp
│   │                   └── res
│   │                       ├── layout
│   │                       ├── mipmap-mdpi
│   │                       └── values
│   ├── docs
│   │   └── source
│   │       ├── _static
│   │       │   ├── css
│   │       │   └── img
│   │       └── models
│   ├── examples
│   │   └── cpp
│   │       └── hello_world
│   ├── ios
│   │   └── VisionTestApp
│   │       ├── VisionTestApp
│   │       └── VisionTestApp.xcodeproj
│   │           └── project.xcworkspace
│   │               └── xcshareddata
│   ├── packaging
│   │   ├── vs2017
│   │   ├── wheel
│   │   └── windows
│   │       └── internal
│   ├── test
│   │   ├── expect
│   │   └── tracing
│   │       └── frcnn
│   └── torchvision
│       ├── csrc
│       │   ├── io
│       │   │   ├── decoder
│       │   │   │   └── gpu
│       │   │   ├── image
│       │   │   │   ├── cpu
│       │   │   │   └── cuda
│       │   │   ├── video
│       │   │   └── video_reader
│       │   ├── models
│       │   └── ops
│       │       ├── autocast
│       │       ├── autograd
│       │       ├── cpu
│       │       ├── cuda
│       │       └── quantized
│       │           └── cpu
│       ├── datasets
│       │   └── samplers
│       ├── io
│       ├── models
│       │   ├── detection
│       │   ├── optical_flow
│       │   ├── quantization
│       │   ├── segmentation
│       │   └── video
│       ├── ops
│       └── transforms
├── vision_opencv
│   └── image_geometry
│       ├── include
│       │   └── image_geometry
│       └── src
│           └── image_geometry
└── ws_perception
    └── multi_cam_oak_lite
```