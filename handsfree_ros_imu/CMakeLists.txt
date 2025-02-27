cmake_minimum_required(VERSION 2.8.3)
project(handsfree_ros_imu)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  scripts/hfi_a9_ros.py
  scripts/hfi_b9_ros.py
  scripts/hfi_b6_ros.py
  scripts/hfi_d6_ros.py
  scripts/display_3D_visualization.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

