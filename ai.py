# from flask import Flask, request, jsonify
# from PIL import Image
# import torch
# from models.experimental import attempt_load

# app = Flask(__name__)

# # 모델 로드
# model = attempt_load('my_project/exp4/weights/best.pt', map_location=torch.device('cpu'))

# # 이미지 전처리 함수 (크기 조정, 정규화 등)
# def preprocess_image(image):
#     # 이미지 처리 로직을 구현하세요.
#     # 필요한 경우 이미지 크기 조정, 정규화 등의 작업을 수행합니다.
#     return preprocessed_image

# # 객체 탐색 및 분류 함수
# def detect_objects(image):
#     # 객체 탐색 및 분류 로직을 구현하세요.
#     # 입력 이미지에 대해 모델을 사용하여 객체 탐색과 분류를 수행합니다.
#     results = model(preprocess_image(image))
    
#     # 결과 반환 (예: bounding box와 클래스 정보 포함된 리스트)
#     return results

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image found'})
    
#     image_file = request.files['image']
    
#     try:
#         image = Image.open(image_file)
#         results = detect_objects(image)
        
#         # 결과 처리 (예: JSON 형태로 변환하여 반환)
#         response_data = []
        
#         for result in results:
#             label = result['label']
#             confidence = result['confidence']
#             bbox = result['bbox']
            
#             response_data.append({
#                 'label': label,
#                 'confidence': confidence,
#                 'bbox': bbox
#             })
        
#         return jsonify(response_data)
    
#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run()


import torch
from PIL import Image

# 모델 로딩
model = torch.hub.load('ultralytics/yolov5', 'custom', path='my_project/exp4/weights/best.pt')  # or yolov5m, yolov5l, yolov5x

# 이미지 로딩 및 변환
img = Image.open('folder/train/images/20230720095731.png')  # your image path

# Inference
results = model(img)

# 결과 출력
results.print()  # print results to screen

# 결과를 이미지 위에 그리기 (optional)
results.show()  # display results superimposed on image

