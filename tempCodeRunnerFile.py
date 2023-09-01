@app.route("/", methods=["GET", "POST"])
def calculate_accident():
    if request.method == "POST":
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        total_people = data.get("total_people")

        # 위도, 경도, 사람 수를 사용하여 사고 발생율 계산
        accident_rate = calculate_accident_rate(latitude, longitude, total_people)

        # JSON 응답으로 사고 발생율 반환
        response_data = {"accident_rate": accident_rate}
        return jsonify(response_data)

    # GET 요청에 대한 기본 응답
    return "Accident Rate Calculator"

if __name__ == "__main__":
    app.run(debug=True)
