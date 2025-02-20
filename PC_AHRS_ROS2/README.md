# PC_AHRS_ROS2
GitHub -> [ntrexlab/PC_AHRS_ROS2](https://github.com/ntrexlab/PC_AHRS_ROS2)
***
## **Manual**
***
* ### 1.HardWare
    * #### 사용모델
         - AHRS - [MW_AHRSv1](http://www.devicemart.co.kr/goods/view?no=1310790)
         - RS232_USB_커넥터 - [USB2CAN(FIFO) v2](http://www.devicemart.co.kr/goods/view?no=1323536)
        

* ### 2.Tool
    * #### 사용버전
        - Ubuntu20.04 [설치메뉴얼](https://ubuntu.com/download/desktop)
        - ROS2_FOXY [설치메뉴얼](https://docs.ros.org/en/foxy/Installation.html)
   
***

* ### 3. 작동
 
    #### 1. Ubuntu 터미널에 명령어를 입력하여 AHRS 패키지 설치합니다.
    ```
    git clone https://github.com/ntrexlab/PC_AHRS_ROS2.git
    ```
    #### 2. RS232_USB_커넥터를 사용하여 AHRS와 Ubuntu 설치된 PC와 연결한다.
    #### 3. USB 통신 컨버터 이름을 명렁어를 통해 알아낸다(EX-ttyUSB0).
    ```
    ls /dev/tty*
    ```
    #### 4. USB 통신 컨버터에 실행 권한을 부여한다.
    ```
    sudo chmod +x /dev/ttyUSB0
    ```
    #### 5. MW-AHRSv2 ROS2 드라이버를 실행한다.
    ```
    ros2 launch stella_ahrs stella_ahrs_launch.py
    ```
***
    
* ### 4. 파일 설명 

    [stella_ahrs/src/MwAHRS.cpp] </br>
    bool Mw_AHRS_init(int ID) 함수는 AHRS 초기설정을 할 수 있도록 지원합니다. 기본적으로 바이너리, 통신주기, 출력데이터를 설정하여 ROS2에서 바로 사용 할 수 있도록 하였습니다.
 
  [stella_ahrs/src/listener.cpp]</br>
52번째 줄에 있는 if(MW_SerialOpen("/dev/ttyUSB0", 115200) < 0) 코드에서 ttyUSB0은 위 작동 카테고리 항목을 참고하여 변경하시거나 그대로 사용하시면 됩니다.


***

* ### 5. 동작 확인
    #### 1.명령어를 사용하면 아래의 사진과 같이 정상적으로 동작하는 모습을 보실 수 있습니다.
    ```
    ros2 topic echo imu
    ```

    ![noname01](https://user-images.githubusercontent.com/85467544/154200371-bf6a66c2-7395-4ec2-813b-7ee13a8d0c79.png)


***
