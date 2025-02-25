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
