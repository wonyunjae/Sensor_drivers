#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import binascii
import math
import serial
import struct
import time
import rospy
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField

cov_orientation = [0.0] * 9
cov_angular_velocity = [0.0] * 9
cov_linear_acceleration = [0.0] * 9
cov_magnetic_field = [0.0] * 9


def eul_to_qua(Eular):
    eular_div = [0, 0, 0]
    eular_div[0], eular_div[1], eular_div[2] = Eular[0] / 2.0, Eular[1] / 2.0, Eular[2] / 2.0

    ca, cb, cc = math.cos(eular_div[0]), math.cos(eular_div[1]), math.cos(eular_div[2])
    sa, sb, sc = math.sin(eular_div[0]), math.sin(eular_div[1]), math.sin(eular_div[2])

    x = sa * cb * cc - ca * sb * sc
    y = ca * sb * cc + sa * cb * sc
    z = ca * cb * sc - sa * sb * cc
    w = ca * cb * cc + sa * sb * sc

    orientation = Quaternion()
    orientation.x, orientation.y, orientation.z, orientation.w = x, y, z, w
    return orientation


def receive_split(receive_buffer):
    buff = []
    for i in range(0, len(receive_buffer), 2):
        buff.append(receive_buffer[i:i + 2])
    return buff


def hex_to_ieee(length, buff):
    hex_str = ''
    data = []
    try:
        for i in range(length // 2 - 3, 11, -4):
            for j in range(i, i - 4, -1):
                hex_str += buff[j]
            # Python3에서는 bytes.fromhex() 사용
            data.append(struct.unpack('>f', bytes.fromhex(hex_str))[0])
            hex_str = ''
        data.reverse()
        return data
    except Exception as e:
        rospy.logerr(f"Error in hex_to_ieee: {e}")
        return [0.0] * 3


if __name__ == "__main__":
    rospy.init_node("imu")

    port = rospy.get_param("~port", "/dev/ttyUSB0")
    baudrate = rospy.get_param("~baudrate", 921600)

    try:
        hf_imu = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)
        if hf_imu.isOpen():
            rospy.loginfo("IMU 연결 성공")
        else:
            hf_imu.open()
            rospy.loginfo("IMU 포트 열림")

    except Exception as e:
        rospy.logerr(f"IMU 연결 오류: {e}")
        rospy.logerr("ttyUSB0를 찾을 수 없습니다. IMU 연결을 확인하세요.")
        exit()

    imu_pub = rospy.Publisher("/imu_taobotics_hfi_a9", Imu, queue_size=10)
    mag_pub = rospy.Publisher("/mag_taobotics_hfi_a9", MagneticField, queue_size=10)
    sensor_data = [0.0] * 11

    while not rospy.is_shutdown():
        try:
            count = hf_imu.inWaiting()
            if count > 24:
                raw_data = hf_imu.read(count)
                # Python3에서는 binascii.hexlify()의 결과를 decode해야 함
                receive_buffer = binascii.hexlify(raw_data).decode('utf-8')
                receive_len = len(receive_buffer)
                stamp = rospy.get_rostime()
                buff = receive_split(receive_buffer)

                if ''.join(buff[0:3]) == 'aa552c':
                    sensor_data = hex_to_ieee(receive_len, buff)
                rpy_degree = []

                if ''.join(buff[0:3]) == 'aa5514':
                    rpy = hex_to_ieee(receive_len, buff)
                    rpy_degree = [
                        rpy[0] / 180 * math.pi,
                        rpy[1] / -180 * math.pi,
                        rpy[2] / -180 * math.pi
                    ]

                    imu_msg = Imu()
                    imu_msg.header.stamp = stamp
                    imu_msg.header.frame_id = "base_link"

                    imu_msg.orientation = eul_to_qua(rpy_degree)
                    imu_msg.orientation_covariance = cov_orientation

                    imu_msg.angular_velocity.x = sensor_data[0]
                    imu_msg.angular_velocity.y = sensor_data[1]
                    imu_msg.angular_velocity.z = sensor_data[2]
                    imu_msg.angular_velocity_covariance = cov_angular_velocity

                    imu_msg.linear_acceleration.x = sensor_data[3] * -9.8
                    imu_msg.linear_acceleration.y = sensor_data[4] * -9.8
                    imu_msg.linear_acceleration.z = sensor_data[5] * -9.8
                    imu_msg.linear_acceleration_covariance = cov_linear_acceleration

                    imu_pub.publish(imu_msg)

                    mag_msg = MagneticField()
                    mag_msg.header.stamp = stamp
                    mag_msg.header.frame_id = "base_link"
                    mag_msg.magnetic_field.x = sensor_data[6]
                    mag_msg.magnetic_field.y = sensor_data[7]
                    mag_msg.magnetic_field.z = sensor_data[8]
                    mag_msg.magnetic_field_covariance = cov_magnetic_field

                    mag_pub.publish(mag_msg)

            time.sleep(0.001)
            
        except Exception as e:
            rospy.logerr(f"Loop error: {e}")
            continue
