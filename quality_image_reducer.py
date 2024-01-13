from PIL import Image
import os

def batch_reduce_image_quality(folder_path, quality_reduction):
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                with Image.open(file_path) as img:
                    original_quality = 100
                    new_quality = int(original_quality * (1 - quality_reduction / 100))

                    output_path = os.path.join(folder_path, file)

                    img.save(output_path, quality=new_quality)
                    print(f"Reduced quality of {file} and saved to {output_path}")
            except Exception as e:
                print(f"Failed to process {file}: {e}")

folder_path = 'tmp'
quality_reduction = 40

batch_reduce_image_quality(folder_path, quality_reduction)
