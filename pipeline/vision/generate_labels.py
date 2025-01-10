from PIL import Image
import numpy as np
import cv2
import os


def find_bounding_boxes(image_path):
    image = Image.open(image_path).convert("L")
    image_np = np.array(image)

    _, thresh = cv2.threshold(image_np, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    h, w = image_np.shape

    boxes = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        x_center = (x + width / 2) / w
        y_center = (y + height / 2) / h
        width /= w
        height /= h
        boxes.append((x_center, y_center, width, height))

    return boxes


def save_yolo_format(boxes, output_path):
    with open(output_path, 'w') as file:
        for box in boxes:
            file.write(f"0 {box[0]} {box[1]} {box[2]} {box[3]}\n")


def process_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_filename in os.listdir(input_dir):
        if image_filename.lower().endswith(('.jpg', '.png')):
            image_path = os.path.join(input_dir, image_filename)
            boxes = find_bounding_boxes(image_path)
            output_path = os.path.join(output_dir, os.path.splitext(image_filename)[0] + '.txt')
            save_yolo_format(boxes, output_path)


val_input_dir = '/content/dataset/val/masks'
val_output_dir = '/content/dataset/val/labels'
train_input_dir = '/content/dataset/train/masks'
train_output_dir = '/content/dataset/train/labels'

process_images(val_input_dir, val_output_dir)
process_images(train_input_dir, train_output_dir)
