import requests
import json

# Flask 서버의 URL 설정
server_url = "http://54.180.126.168:5001"  # 서버의 주소로 변경해야 합니다.

# 보낼 JSON 데이터 생성
data = {
    "latitude": 37.1234,
    "longitude": -122.5678,
    "total_people": 100
}

# JSON 데이터를 POST 요청으로 서버에 보내기
try:
    response = requests.post(server_url, json=data)

    if response.status_code == 200:
        # 서버에서 받은 응답 출력
        print("서버 응답:", response.json())
    else:
        print("서버 요청 실패:", response.status_code)

except requests.exceptions.RequestException as e:
    print("서버 요청 중 오류 발생:", e)
