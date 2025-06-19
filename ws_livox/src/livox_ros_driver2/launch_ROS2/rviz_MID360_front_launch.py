import sys
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import launch

from math import radians
from scipy.spatial.transform import Rotation as R

################### user configure parameters for ros2 start ###################
xfer_format   = 0    # 0-Pointcloud2(PointXYZRTL), 1-customized pointcloud format
multi_topic   = 1    # 0-All LiDARs share the same topic, 1-One LiDAR one topic
data_src      = 0    # 0-lidar, others-Invalid data src
publish_freq  = 10.0 # freqency of publish, 5.0, 10.0, 20.0, 50.0, etc.
output_type   = 0
frame_id      = 'livox_frame_front'
lvx_file_path = '/home/livox/livox_test.lvx'
cmdline_bd_code = 'livox0000000001'

# cur_path = os.path.split(os.path.realpath(__file__))[0] 
cur_config_path = '/home/talon/ros2_ws/src/Sensor_drivers/ws_livox/src/livox_ros_driver2/config'
rviz_config_path = os.path.join(cur_config_path, 'display_point_cloud_ROS2_front.rviz')
user_config_path = os.path.join(cur_config_path, 'MID360_front_config.json')
################### user configure parameters for ros2 end #####################

livox_ros2_params = [
    {"xfer_format": xfer_format},
    {"multi_topic": multi_topic},
    {"data_src": data_src},
    {"publish_freq": publish_freq},
    {"output_data_type": output_type},
    {"frame_id": frame_id},
    {"lvx_file_path": lvx_file_path},
    {"user_config_path": user_config_path},
    {"cmdline_input_bd_code": cmdline_bd_code}
]


def generate_launch_description():
    
    # # roll, pitch, yaw in deg
    # rotations = [
    #     [0.0, 0.0, -90.0]]   # roll, pitch, yaw [deg]    
    
    # # X, Y, Z(m)
    # translations = [
    #     [0.36311, 0.0, 0.52023]]   # X, Y, Z(m)    
    
    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_front_publisher',
        output='screen',
        parameters=livox_ros2_params
        )

    livox_rviz = Node(
            package='rviz2',
            executable='rviz2',
            name='livox_rviz_front',
            output='screen',
            arguments=['--display-config', rviz_config_path]
        )
    
    # # static_transform_publisher 노드 추가 (TF 등록)
    # roll = radians(rotations[0][0])sss
    # pitch = radians(rotations[0][1])
    # yaw = radians(rotations[0][2])
    # r = R.from_euler('xyz', [roll, pitch, yaw])  # rad 단위
    # q = r.as_quat()  # [x, y, z, w]    

    # livox_tf = Node(
    #         package='tf2_ros',
    #         executable='static_transform_publisher',
    #         name='static_tf_mid360_1',
    #         arguments=[
    #             str(translations[0][0]),  # x
    #             str(translations[0][1]),  # y
    #             str(translations[0][2]),  # z
    #             str(q[0]),                # qx
    #             str(q[1]),                # qy
    #             str(q[2]),                # qz
    #             str(q[3]),                # qw
    #             'base_link',              # parent frame
    #             'livox1_frame'   # child frame: 카메라 frame 이름에 맞게!
    #         ],
    #         output='screen'
    #     )
    

    return LaunchDescription([
        livox_driver,
        livox_rviz,
        # livox_tf,        
    ])
