import requests
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_static_map_image(api_key, latitude, longitude, zoom=15, size="400x400"):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{latitude},{longitude}",
        "zoom": zoom,
        "size": size,
        "key": api_key,
    }
    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Failed to fetch map image.")
        return None

def highlight_color(image, target_color, tolerance):
    rgb_image = image.convert("RGB")
    width, height = image.size
    highlighted_pixels = []

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            if color_within_range((r, g, b), target_color, tolerance):
                highlighted_pixels.append((x, y))
                image.putpixel((x, y), (255, 0, 0))

    return image, highlighted_pixels

def color_within_range(pixel_color, target_color, tolerance):
    r1, g1, b1 = pixel_color
    r2, g2, b2 = target_color

    if abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance:
        return True

    return False

def get_weather_info(latitude, longitude):
    api_key = "ba20a43caf4fd585232c2b3c0bb2e396"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    weather_condition = weather_data.get("weather")[0].get("main")
    if weather_condition in ["Clear", "Clouds"]:
        return "good"
    else:
        return "bad"
@app.route("/", methods=["POST"])
def calculate_accident():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    total_people = data.get("total_people")

    api_key = "AIzaSyDdrlQo7Gkuap-hK9c3WGUe7dyQ526hGqA"
    zoom_level = 17
    image_size = "400x400"
    map_image = get_static_map_image(api_key, latitude, longitude, zoom_level, image_size)

    if map_image:
        highlighted_image, highlighted_pixels = highlight_color(map_image, (255, 255, 255), 3)
        pixel_area_cm_sq = 0.3494371482
        highlighted_area_cm_sq = len(highlighted_pixels) * pixel_area_cm_sq

        min_distance = 0.4 
        min_distance_sq = min_distance ** 2
        required_area = total_people * min_distance_sq

        area_difference = required_area - highlighted_area_cm_sq

        
        accident_rate = min(99.9, max(0.1, 100.0 * area_difference / required_area))

        weather_info = get_weather_info(latitude, longitude)

        if weather_info == "good":
            accident_rate += 10
        elif weather_info == "bad":
            accident_rate -= 10

        accident_rate = min(99.9, max(0.1, 100.0 * area_difference / required_area))

        if accident_rate > 50:
            predicted_victims = int(total_people * (accident_rate - 50) / 70)
        else:
            predicted_victims = 0
            

        response_data = {"accident_rate": round(accident_rate, 2), "predicted_victims": predicted_victims}
        return jsonify(response_data)

    return jsonify({"error": "Failed to fetch map image."})

if __name__ == "__main__":
    app.run(port=5001)




import requests
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

# Load YOLOv5 model
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
yolo_model.eval()

def get_static_map_image(api_key, latitude, longitude, zoom=15, size="400x400"):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{latitude},{longitude}",
        "zoom": zoom,
        "size": size,
        "key": api_key,
    }
    
def process_yolo_results(results):
    bboxes = results[:, :4] 
    conf_scores = results[:, 4] 
    confidence_threshold = 0.5
    road_mask = torch.zeros_like(bboxes[:, 0], dtype=torch.uint8) 

    road_class = 0

    for i, bbox in enumerate(bboxes):
        if conf_scores[i] >= confidence_threshold and results[i, 5] == road_class:
            xmin, ymin, xmax, ymax = bbox.cpu().numpy().astype(int)
            road_mask[ymin:ymax, xmin:xmax] = 1

    return road_mask


def highlight_road(image, yolo_model):
    results = yolo_model(image)
    road_mask = process_yolo_results(results)
    road_image = image.copy()
    road_image[~road_mask] = (255, 255, 255)

    return road_image, road_mask

def get_weather_info(latitude, longitude):
    api_key = "ba20a43caf4fd585232c2b3c0bb2e396"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    weather_condition = weather_data.get("weather")[0].get("main")
    if weather_condition in ["Clear", "Clouds"]:
        return "good"
    else:
        return "bad"

@app.route("/", methods=["POST"])
def calculate_accident():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    total_people = data.get("total_people")

    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    zoom_level = 17
    image_size = "400x400"
    map_image = get_static_map_image(api_key, latitude, longitude, zoom_level, image_size)

    if map_image:
        highlighted_image, road_mask = highlight_road(map_image, yolo_model)

        highlighted_image, highlighted_pixels = highlight_color(map_image, (255, 255, 255), 3)
        pixel_area_cm_sq = 0.3494371482
        highlighted_area_cm_sq = len(highlighted_pixels) * pixel_area_cm_sq

        min_distance = 0.4 
        min_distance_sq = min_distance ** 2
        required_area = total_people * min_distance_sq

        area_difference = required_area - highlighted_area_cm_sq

        
        accident_rate = min(99.9, max(0.1, 100.0 * area_difference / required_area))

        weather_info = get_weather_info(latitude, longitude)

        if weather_info == "good":
            accident_rate += 10
        elif weather_info == "bad":
            accident_rate -= 10

        accident_rate = min(99.9, max(0.1, 100.0 * area_difference / required_area))

        if accident_rate > 50:
            predicted_victims = int(total_people * (accident_rate - 50) / 70)
        else:
            predicted_victims = 0

        
        response_data = {"accident_rate": round(accident_rate, 2), "predicted_victims": predicted_victims}
        return jsonify(response_data)

    return jsonify({"error": "Failed to fetch map image."})

if __name__ == "__main__":
    app.run(port=5001)
