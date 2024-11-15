from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 위치 정보를 저장할 리스트
locations = []

# 위치 정보를 수신하는 엔드포인트
@app.route('/location', methods=['POST'])
def receive_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is not None and longitude is not None:
        # 위치 정보를 리스트에 저장
        locations.append({'latitude': latitude, 'longitude': longitude})
        print(f"Received location: Latitude={latitude}, Longitude={longitude}")
        return jsonify({"status": "Location received", "data": locations}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

# health 체크 엔드포인트
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# 기본 페이지(/) 및 지도 페이지
@app.route('/')
@app.route('/map', methods=['GET'])
def show_map():
    # HTML 코드 템플릿
    map_html = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>위치 정보 지도</title>
    <style>
        /* 지도와 위치 정보 스타일 설정 */
        #map {
            height: 600px;
            width: 100%;
        }
        #location-list {
            margin-top: 20px;
            font-family: Arial, sans-serif;
        }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDxg42U8tFRwVWAk64COW-x5qfApBV6jLs"></script>
</head>
<body>
    <h1>수신된 위치 정보 지도</h1>
    <div id="map"></div>
    <div id="location-list">
        <h2>수신된 위치 정보</h2>
        <ul>
            {% for location in locations %}
                <li>위도: {{ location.latitude }}, 경도: {{ location.longitude }}</li>
            {% endfor %}
        </ul>
    </div>

    <script>
        function initMap() {
            // 초기 지도 설정 (중심 위치와 줌)
            const map = new google.maps.Map(document.getElementById('map'), {
                center: { lat: 36.5, lng: 127.5 }, // 기본 위치 (한국 중앙)
                zoom: 7
            });

            // 서버에서 받은 위치 정보를 가져와 지도에 마커 추가
            const locations = {{ locations | tojson }};
            locations.forEach((location) => {
                new google.maps.Marker({
                    position: { lat: location.latitude, lng: location.longitude },
                    map: map
                });
            });
        }

        // 페이지 로드 시 지도 초기화
        window.onload = initMap;
    </script>
</body>
</html>
    '''
    return render_template_string(map_html, locations=locations)

# 위치 정보 리스트를 조회하는 엔드포인트
@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify({"locations": locations}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
