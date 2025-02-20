# Sensor_drivers
drivers of sensors in 108
/ROS 1 noetic

### 작성 규칙

- main에 잘못 merge될 경우 디버깅이 어려울 수 있어 각자의 브랜치 생성 후 관리 부탁드립니다 !



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
