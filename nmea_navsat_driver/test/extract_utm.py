#!/usr/bin/env python3
import numpy as np
import pandas as pd
from math import sqrt, floor

# 원본 UTM 좌표 추출 (9~13번 좌표)
utm_points = [
    (353858.4, 4032298.4, 71.7),  # 9번 좌표 (easting, northing, elevation)
    (353910.1, 4032306.8, 70.3),  # 10번 좌표
    (353907.8, 4032269.9, 68.7),  # 11번 좌표
    (353896.6, 4032264.6, 68.7),  # 12번 좌표
    (353886.9, 4032264.9, 69.4)   # 13번 좌표
]

# 결과 저장할 리스트
resampled_points = []

# 두 점 사이의 거리 계산 함수
def distance(p1, p2):
    return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

# 0.001m 간격으로 두 점 사이 재샘플링
def resample_segment(p1, p2, interval=0.001):
    d = distance(p1, p2)
    num_points = max(floor(d / interval), 1)
    points = []
    
    for i in range(num_points + 1):
        t = i / num_points if num_points > 0 else 0
        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])
        z = p1[2] + t * (p2[2] - p1[2])
        points.append((x, y, z))
    
    return points

def main():
    # 첫 번째 점 추가
    resampled_points.append(utm_points[0])

    # 각 세그먼트 재샘플링
    for i in range(len(utm_points) - 1):
        # 각 세그먼트의 시작점은 이미 추가되었으므로 첫 점은 건너뛰기
        segment_points = resample_segment(utm_points[i], utm_points[i+1])[1:]
        resampled_points.extend(segment_points)

    # 결과 출력
    print(f"원본 좌표: {len(utm_points)}개")
    print(f"재샘플링된 좌표: {len(resampled_points)}개")

    # 결과를 데이터프레임으로 변환
    df = pd.DataFrame(resampled_points, columns=['utm_easting', 'utm_northing', 'elevation'])

    # 거리 열 추가 (시작점으로부터 누적 거리)
    distances = [0]
    for i in range(1, len(resampled_points)):
        prev = resampled_points[i-1]
        curr = resampled_points[i]
        d = distance(prev, curr)
        distances.append(distances[-1] + d)
    df['distance'] = distances

    # 파일로 저장 (탭으로 구분된 텍스트 파일)
    df.to_csv('/home/wonseo/traxxas_ws/src/Sensor_drivers/nmea_navsat_driver/map/utm_resampled_1mm.txt', sep='\t', index=False)

    # 처음 10개 점 출력 예시
    print("\n처음 10개 재샘플링 좌표:")
    print(df.head(10).to_string(index=False))

if __name__ == '__main__':
    main()