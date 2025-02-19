# Sensor_drivers
drivers of sensors in 108
/ROS 1 noetic

<작성 규칙>
잘못된 merge로 디버깅이 어려울 수 있으니 각자의 브랜치를 생성해 관리 부탁드립니다 ! (main에 push 조심)



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
