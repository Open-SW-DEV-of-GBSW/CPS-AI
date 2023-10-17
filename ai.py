import requests
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

model_path = 'my_project/exp6/weights/best.pt'

from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device

device = select_device('cpu')
yolo_model = attempt_load(model_path)
yolo_model.eval()

def calculate_road_area(image, yolo_model):
    results = yolo_model(image)
    road_area = 0
    for det in results.pred[0]:
        if det is not None and len(det) > 0:
            for *xyxy, conf, cls in det:
                area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])
                road_area += area
    return road_area

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

def calculate_object_area(object):
    x1, y1, x2, y2 = object
    width = x2 - x1
    height = y2 - y1
    area = width * height
    return area


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
    api_key = os.getenv("weather_api")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    weather_condition = weather_data.get("weather")[0].get("main")
    if weather_condition in ["Clear", "Clouds"]:
        return "good"
    else:
        return "bad"

        
def load_yolo_model(model_path):
    model = attempt_load(model_path)
    model.eval()
    return model

yolo_model = load_yolo_model(model_path)

@app.route("/", methods=["POST"])
def calculate_accident():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    total_people = data.get("total_people")

    api_key = os.getenv("GOOGLE_MAP_API_KEY")
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