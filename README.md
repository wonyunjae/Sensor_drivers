# Sensor_drivers
drivers of sensors in 108
/ROS 1 noetic


### Velodyne

```jsx
roscore
roslaunch velodyne_pointcloud VLP16_points.launch
rviz -f velodyne
```

### Xsens

```jsx
roscore
roslaunch xsens_mti_driver xsens_mti_node.launch
rosrun plotjuggler plotjuggler //visualize imu_Data
```
