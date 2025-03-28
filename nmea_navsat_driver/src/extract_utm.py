#!/usr/bin/env python3
import numpy as np
import pandas as pd
from math import sqrt, floor
import pyproj
import os

def lat_lon_to_utm(lat, lon):
    """위도/경도를 UTM 좌표로 변환"""
    # WGS84 좌표계 사용 (EPSG:4326)
    proj = pyproj.Transformer.from_crs(
        "epsg:4326",  # WGS84 (위도/경도)
        "epsg:32652", # UTM 52N (대전 지역 기준)
        always_xy=True
    )
    
    # 변환 (경도, 위도) 순서로 입력해야 함
    easting, northing = proj.transform(lon, lat)
    return easting, northing

def load_fix_file(filepath):
    """fix.txt 파일을 저수준 파싱으로 로드"""
    try:
        # 파일 열기
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # 헤더 처리
        header = lines[0].strip().split('\t')
        
        # 필요한 열 인덱스 찾기
        try:
            lat_idx = header.index('latitude')
            lon_idx = header.index('longitude')
            alt_idx = header.index('altitude (m)')
            dist_idx = header.index('distance (km)')
        except ValueError as e:
            print(f"필요한 열을 찾을 수 없습니다: {e}")
            # 열 이름 추측
            lat_idx = next((i for i, h in enumerate(header) if 'lat' in h.lower()), 1)
            lon_idx = next((i for i, h in enumerate(header) if 'lon' in h.lower()), 2)
            alt_idx = next((i for i, h in enumerate(header) if 'alt' in h.lower()), 6)
            dist_idx = next((i for i, h in enumerate(header) if 'dist' in h.lower() and 'km' in h.lower()), 9)
            print(f"추정된 열 인덱스: lat={lat_idx}, lon={lon_idx}, alt={alt_idx}, dist={dist_idx}")
        
        # 데이터 파싱
        data = []
        for i, line in enumerate(lines[1:], 1):
            try:
                fields = line.strip().split('\t')
                if len(fields) >= max(lat_idx, lon_idx, alt_idx, dist_idx) + 1:
                    # 행의 필드 수가 충분한 경우에만 처리
                    lat = float(fields[lat_idx])
                    lon = float(fields[lon_idx])
                    
                    # 고도가 비어있거나 숫자가 아닌 경우 처리
                    try:
                        alt = float(fields[alt_idx]) if fields[alt_idx].strip() else 0.0
                    except ValueError:
                        alt = 0.0
                    
                    # 거리 처리
                    try:
                        dist = float(fields[dist_idx]) if fields[dist_idx].strip() else 0.0
                    except ValueError:
                        dist = 0.0
                    
                    data.append({
                        'latitude': lat,
                        'longitude': lon,
                        'altitude (m)': alt,
                        'distance (km)': dist
                    })
            except Exception as e:
                print(f"줄 {i+1} 파싱 중 오류 무시: {e}")
                continue
        
        # 데이터프레임 생성
        df = pd.DataFrame(data)
        print(f"파일 로드 성공: {len(df)}개 데이터 (총 {len(lines)-1}개 중)")
        return df
    except Exception as e:
        print(f"파일 로드 중 오류 발생: {str(e)}")
        return None

def convert_to_utm(df):
    """위도/경도 데이터를 UTM 좌표로 변환"""
    # UTM 좌표를 저장할 빈 리스트
    utm_easting = []
    utm_northing = []
    
    # 각 행에 대해 변환 수행
    for idx, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        
        # UTM 좌표로 변환
        easting, northing = lat_lon_to_utm(lat, lon)
        
        # 결과 저장
        utm_easting.append(easting)
        utm_northing.append(northing)
    
    # 데이터프레임에 UTM 좌표 추가
    df['utm_easting'] = utm_easting
    df['utm_northing'] = utm_northing
    
    return df

def main():
    # 입력 파일 경로
    input_file = '/home/wonseo/Downloads/fix.txt'
    
    # 출력 파일 경로
    output_dir = '/home/wonseo/traxxas_ws/src/Sensor_drivers/nmea_navsat_driver/map'
    output_file = os.path.join(output_dir, 'utm_converted.txt')
    
    # 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 파일 로드
    df = load_fix_file(input_file)
    if df is None:
        return
    
    # 데이터 확인
    print("데이터 샘플:")
    print(df.head())
    
    # UTM 변환
    df_with_utm = convert_to_utm(df)
    
    # 두 점 사이의 거리 계산을 위한 함수
    def distance(p1_east, p1_north, p2_east, p2_north):
        return sqrt((p2_east - p1_east)**2 + (p2_north - p1_north)**2)
    
    # 누적 거리 계산
    distances = [0]  # 첫 번째 점의 거리는 0
    for i in range(1, len(df_with_utm)):
        prev_east = df_with_utm.iloc[i-1]['utm_easting']
        prev_north = df_with_utm.iloc[i-1]['utm_northing']
        curr_east = df_with_utm.iloc[i]['utm_easting']
        curr_north = df_with_utm.iloc[i]['utm_northing']
        
        dist = distance(prev_east, prev_north, curr_east, curr_north)
        distances.append(distances[-1] + dist)
    
    df_with_utm['utm_distance'] = distances
    
    # 결과 저장
    # 간단한 형식으로 utm.x와 utm.y 좌표만 저장
    with open(output_file, 'w') as f:
        for i in range(len(df_with_utm)):
            easting = df_with_utm.iloc[i]['utm_easting']
            northing = df_with_utm.iloc[i]['utm_northing']
            f.write(f"{easting:.6f} {northing:.6f}\n")
    
    print(f"변환 완료: {output_file}에 저장됨")
    
    # 변환된 결과 확인
    print("\nUTM 변환 결과 샘플:")
    print("첫 5개 UTM 좌표:")
    for i in range(min(5, len(df_with_utm))):
        easting = df_with_utm.iloc[i]['utm_easting']
        northing = df_with_utm.iloc[i]['utm_northing']
        print(f"{easting:.6f} {northing:.6f}")

if __name__ == '__main__':
    main() 