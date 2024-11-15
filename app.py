from flask import Flask, request, jsonify

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
        return jsonify({"error": "Invalid data"}), 400from flask import Flask, render_template_string, request, jsonify

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
        # 위치 정보를 리스트에 추가
        locations.append({'latitude': latitude, 'longitude': longitude})
        print(f"Received location: Latitude={latitude}, Longitude={longitude}")
        return jsonify({"status": "Location received", "data": locations}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

# 위치 정보를 지도에 표시하는 페이지
@app.route('/map', methods=['GET'])
def show_map():
    # HTML 코드 템플릿을 render_template_string으로 직접 주입
    map_html = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>위치 정보 지도</title>
        <style>
            #map {
                height: 600px;
                width: 100%;
            }
        </style>
        <script type="text/javascript" src="https://oapi.map.naver.com/openapi/v3/maps.js?ncpClientId=C0tZhYvWgxSRYwDxmHiVoaMcp8M4ENxoqLlNKoMA&submodules=geocoder"></script>
    </head>
    <body>
        <h1>수신된 위치 정보 지도</h1>
        <div id="map"></div>
        <script>
            function initMap() {
                const map = new naver.maps.Map('map', {
                    center: new naver.maps.LatLng(36.5, 127.5), // 기본 위치 (한국 중앙)
                    zoom: 7
                });

                // 서버에서 받은 위치 정보를 가져와 지도에 마커 추가
                const locations = {{ locations | tojson }};
                locations.forEach((location) => {
                    new naver.maps.Marker({
                        position: new naver.maps.LatLng(location.latitude, location.longitude),
                        map: map
                    });
                });
            }

            window.onload = initMap;
        </script>
    </body>
    </html>
    '''
    return render_template_string(map_html, locations=locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# 위치 정보 리스트를 조회하는 엔드포인트
@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify({"locations": locations}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)