import os
import cv2
import numpy as np
import pandas as pd
from io import StringIO

# CSV content provided by the user
csv_content = """
class, r, g, b
unlabeled, 0, 0, 0
paved-area, 128, 64, 128
dirt, 130, 76, 0
grass, 0, 102, 0
gravel, 112, 103, 87
water, 28, 42, 168
rocks, 48, 41, 30
pool, 0, 50, 89
vegetation, 107, 142, 35
roof, 70, 70, 70
wall, 102, 102, 156
window, 254, 228, 12
door, 254, 148, 12
fence, 190, 153, 153
fence-pole, 153, 153, 153
person, 255, 22, 96
dog, 102, 51, 0
car, 9, 143, 150
bicycle, 119, 11, 32
tree, 51, 51, 0
bald-tree, 190, 250, 190
ar-marker, 112, 150, 146
obstacle, 2, 135, 115
conflicting, 255, 0, 0
"""

# Convert the CSV-RGB content to yolo detection format
csv_file_like_object = StringIO(csv_content)
class_dict = pd.read_csv(csv_file_like_object, skipinitialspace=True)

color_class_id = {(row['r'], row['g'], row['b']): index for index, row in class_dict.iterrows()}

masks_dir_path = 'C:/Users/damia/PycharmProjects/object-tracker-dl/data/masks/val'
mask_files = [f for f in os.listdir(masks_dir_path) if f.endswith('.png')]

output_txt_dir_path = 'C:/Users/damia/OneDrive/Pulpit/labels/val'

if not os.path.exists(output_txt_dir_path):
    os.makedirs(output_txt_dir_path)

for mask_file in mask_files:
    mask_image_path = os.path.join(masks_dir_path, mask_file)

    mask = cv2.imread(mask_image_path, cv2.IMREAD_COLOR)
    if mask is None:
        print(f"Error: Unable to load the image at path {mask_image_path}")
        continue
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

    annotations = []

    for (r, g, b), class_id in color_class_id.items():
        class_mask = np.all(mask == np.array([r, g, b]), axis=-1).astype(np.uint8)

        contours, _ = cv2.findContours(class_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_center = (x + w / 2) / mask.shape[1]
            y_center = (y + h / 2) / mask.shape[0]
            width = w / mask.shape[1]
            height = h / mask.shape[0]
            annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")

    base_filename = os.path.splitext(mask_file)[0]
    annotations_path = os.path.join(output_txt_dir_path, base_filename + '.txt')
    with open(annotations_path, 'w') as file:
        file.write('\n'.join(annotations))
