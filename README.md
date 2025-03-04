### MW-AHRS-x1 
![image](https://github.com/user-attachments/assets/c41f6fbe-7794-4180-ba5c-3f22f7489bfc)

```jsx
// 포트 권한 설정
sudo chmod +x /dev/serial/by-id/[PORT_NAME] 
colcon build --symlink-install
ros2 launch ros2 launch stella_ahrs stella_ahrs_launch.py
// hz, port 설정
Sensor_drivers/PC_AHRS_ROS2/stella_ahrs/src/listener.cpp :: 52번째 줄에 baudrate, port 설정
Sensor_drivers/PC_AHRS_ROS2/stella_ahrs/src/listener.cpp :: 84번째 줄에 rate() 괄호 안에 hz 설정
```

### WTGAHRS3-232
![image](https://github.com/user-attachments/assets/0928f529-5a48-4989-b825-a2a8acadfd58)
현재 driver 확인 중,,,

### MRP-2000
![image](https://github.com/user-attachments/assets/3b032baf-9125-4818-b078-4c45b568a263)
```jsx
sudo chmod +x /dev/serial/by-id/[PORT_NAME]
// /Sensor_drivers/nmea_navsat_driver/config/nmea_serial_driver.yaml 경로에 [PORT_NAME]과 baudrate 설정 확인,
// /Sensor_drivers/nmea_navsat_driver/src/libnmea_navsat_driver/nodes/nmea_serial_driver.py 에서 [PORT_NAME]과 baudrate 설정 확인
colcon build --symlink-install
ros2 run nmea_navsat_driver nmea_serial_driver 
```

### MID-360
![image](https://github.com/user-attachments/assets/f5b754a3-70b4-4a51-9790-e6762739133d)
```jsx
// 포트 권한 설정 (232-USB컨버터에 따라 이름이 달라질 수 있음)
sudo chmod +x /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
colcon build --symlink-install

Sensor_drivers/wit
```

```jsx
// git clone
https://github.com/wonyunjae/Sensor_drivers.git 
// 브랜치 확인 
git branch -a 
git checkotut ros2 // ros2 브랜치가 아닐경우에
cd /Sensor_drivers/ws_livox/src/livox_ros_driver2/
./build.sh HUMBLE

```

/Sensor_drivers/ws_livox/src/livox_ros_driver2/config/MID360_config.json을 보면

lidar_configs가 있고, host_net_info가 있는데, 

host_net_info —> 192.168.1.2로 변경

lidar_config_ip —> 192.168.1.133 로 변경 후 재 빌드

```jsx
cd /Sensor_drivers/ws_livox/src/livox_ros_driver2/
./build.sh HUMBLE
cd /Sensor_drivers/ws_livox
source ./install/setup.bash
//MID360 라이다 실행
ros2 launch livox_ros_driver2 rviz_MID360_launch.py 

```

