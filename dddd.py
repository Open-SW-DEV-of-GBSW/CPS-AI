import os
import cv2
import numpy as np

# 데이터 폴더 경로 설정
data_folder = "folder/test/images"

# 이미지와 라벨 데이터를 함께 증강하는 함수
def augment_data(image, labels):
    # 이미지 회전
    angle = np.random.randint(-10, 10)
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # 밝기 조절
    brightness = np.random.randint(-30, 30)
    brightened_image = cv2.add(rotated_image, np.array([brightness]))

    # 라벨 데이터 조정
    new_labels = []
    for label in labels:
        class_id, x, y, w, h = map(float, label.split())
        # 회전된 이미지에 맞게 좌표를 조정
        new_x = (x * width) / width
        new_y = (y * height) / height
        new_w = (w * width) / width
        new_h = (h * height) / height
        new_labels.append(f"{class_id} {new_x} {new_y} {new_w} {new_h}")

    return brightened_image, new_labels

# 데이터 폴더 내의 모든 이미지 파일 가져오기
image_files = [file for file in os.listdir(data_folder) if file.endswith(".jpg")]

# 이미지와 라벨 데이터를 증강하고 저장
for image_file in image_files:
    image_path = os.path.join(data_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join("folder/test/labels", label_file)  # 라벨 파일 경로 설정

    # 이미지 로드
    image = cv2.imread(image_path)

    # 라벨 로드
    with open(label_path, 'r') as f:
        labels = f.read().strip().split('\n')

    # 데이터 증강
    augmented_image, augmented_labels = augment_data(image, labels)

    # 이미지 결과 저장
    cv2.imwrite(image_path, augmented_image)

    # 라벨 결과 저장
    with open(label_path, 'w') as f:
        f.write('\n'.join(augmented_labels))
