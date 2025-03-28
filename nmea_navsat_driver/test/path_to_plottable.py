#!/usr/bin/env python3
import rospy
import numpy as np
import os
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Vector3
from std_msgs.msg import Header

class UTMCoordinatePublisher:
    def __init__(self):
        rospy.init_node('utm_coordinate_publisher', anonymous=True)
        
        # Vector3 메시지를 사용하여 단일 토픽으로 발행 (PlotJuggler용)
        # Vector3에서는 x, y, z 필드를 사용할 수 있음
        self.vector_pub = rospy.Publisher('/utm_map/point', Vector3, queue_size=10)
        
        # # Path 메시지 발행자 설정 (RViz용)
        self.path_pub = rospy.Publisher('/utm_map/path', Path, queue_size=10)
        
        # 파일 경로 매개변수 설정
        self.file_path = rospy.get_param('~file_path', 
                         '/home/wonseo/traxxas_ws/src/Sensor_drivers/nmea_navsat_driver/map/utm_converted.txt')
        
        # 발행 속도 매개변수 (기본값: 10Hz)
        self.publish_rate = rospy.get_param('~rate', 10)
        
        # 한 번에 몇 개의 좌표를 발행할지 설정 (기본값: 모든 좌표)
        self.points_per_publish = rospy.get_param('~points_per_publish', 0)  # 0은 모든 좌표
        
        # 파일 존재 확인
        if not os.path.exists(self.file_path):
            rospy.logerr(f"파일을 찾을 수 없습니다: {self.file_path}")
            return
        
        # UTM 좌표 로드
        self.load_utm_coordinates()
        
        # Path 메시지 생성
        self.create_path_msg()
        
    def load_utm_coordinates(self):
        """UTM 좌표 파일 로드"""
        try:
            # 공백으로 구분된 파일 읽기 (열 이름 없음)
            utm_coords = np.loadtxt(self.file_path)
            
            # 열이 2개인지 확인
            if utm_coords.shape[1] != 2:
                rospy.logerr(f"잘못된 파일 형식: {self.file_path}. 각 줄에 2개의 숫자(easting northing)가 필요합니다.")
                return
            
            # 분리하여 저장
            self.eastings = utm_coords[:, 0]
            self.northings = utm_coords[:, 1]
            
            rospy.loginfo(f"UTM 좌표 {len(self.eastings)}개 로드 완료")
            rospy.loginfo(f"첫 3개 좌표: {list(zip(self.eastings[:3], self.northings[:3]))}")
            
        except Exception as e:
            rospy.logerr(f"UTM 좌표 로드 중 오류 발생: {str(e)}")
            self.eastings = []
            self.northings = []
    
    def create_path_msg(self):
        """UTM 좌표를 Path 메시지로 변환"""
        self.path_msg = Path()
        self.path_msg.header.frame_id = "utm"
        
        for i in range(len(self.eastings)):
            pose = PoseStamped()
            pose.header.frame_id = "utm"
            
            # UTM 좌표 설정
            pose.pose.position.x = float(self.eastings[i])
            pose.pose.position.y = float(self.northings[i])
            pose.pose.position.z = 0.0
            
            # 기본 방향 설정 (회전 없음)
            pose.pose.orientation.w = 1.0
            
            self.path_msg.poses.append(pose)
        
        rospy.loginfo(f"Path 메시지 생성 완료 ({len(self.path_msg.poses)}개 포즈)")
    
    def publish_data(self):
        """UTM 좌표를 발행"""
        if len(self.eastings) == 0 or len(self.northings) == 0:
            rospy.logerr("발행할 UTM 좌표가 없습니다.")
            return
        
        rate = rospy.Rate(self.publish_rate)
        total_points = len(self.eastings)
        
        # 한 번에 발행할 포인트 수 결정
        points_per_publish = total_points if self.points_per_publish <= 0 else min(self.points_per_publish, total_points)
        
        rospy.loginfo(f"UTM 좌표 발행 시작 (한 번에 {points_per_publish}개 좌표 발행)")
        
        while not rospy.is_shutdown():
            # Path 메시지 타임스탬프 업데이트
            self.path_msg.header.stamp = rospy.Time.now()
            for pose in self.path_msg.poses:
                pose.header.stamp = self.path_msg.header.stamp
            
            # Path 메시지 발행 (RViz용)
            self.path_pub.publish(self.path_msg)
            
            # 개별 좌표 발행 (PlotJuggler용) - 이제 단일 Vector3 메시지로 발행
            for i in range(points_per_publish):
                # 하나의 Vector3 메시지에 x, y 좌표를 담음
                point_msg = Vector3()
                point_msg.x = float(self.eastings[i])
                point_msg.y = float(self.northings[i])
                point_msg.z = 0.0  # z 좌표는 필요 없지만 Vector3 형식에 필요함
                
                # 단일 메시지로 발행
                self.vector_pub.publish(point_msg)
                
                # 간격을 두어 데이터가 잘 전달되도록 함
                rospy.sleep(0.001)
            
            rospy.loginfo(f"UTM 좌표 {points_per_publish}개 발행 완료")
            
            # 발행 주기 조절
            rate.sleep()

if __name__ == '__main__':
    try:
        node = UTMCoordinatePublisher()
        node.publish_data()
    except rospy.ROSInterruptException:
        pass
