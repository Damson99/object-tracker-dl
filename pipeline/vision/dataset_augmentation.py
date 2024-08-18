import argparse
import os

from PIL import Image, ImageOps, ImageEnhance


def perform(
        input_path: str,
        output_path: str,
        image_format: str
):
    image = Image.open(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    augmented_images = [(f"{base_name}_original", image)]

    rotated_15 = image.rotate(15, expand=True)
    rotated_30 = image.rotate(30, expand=True)
    augmented_images.extend([
        (f"{base_name}_rotated_15", rotated_15),
        (f"{base_name}_rotated_30", rotated_30)
    ])

    mirror = ImageOps.mirror(image)
    augmented_images.extend([
        (f"{base_name}_mirror", mirror)
    ])

    for x_shift, y_shift in [(50, 0), (0, 50), (50, 50), (-50, 0), (0, -50), (-50, -50)]:
        translated_image = image.transform(image.size, Image.AFFINE, (1, 0, x_shift, 0, 1, y_shift))
        augmented_images.append((f"{base_name}_translated_{x_shift}_{y_shift}", translated_image))

    scaled_up = image.resize((int(image.width * 1.2), int(image.height * 1.2)))
    scaled_down = image.resize((int(image.width * 0.8), int(image.height * 0.8)))
    augmented_images.extend([
        (f"{base_name}_scaled_up", scaled_up),
        (f"{base_name}_scaled_down", scaled_down)
    ])

    enhancer_brightness = ImageEnhance.Brightness(image)
    enhancer_saturation = ImageEnhance.Color(image)
    bright_image = enhancer_brightness.enhance(1.5)
    dark_image = enhancer_brightness.enhance(0.5)
    saturated_image = enhancer_saturation.enhance(1.5)
    desaturated_image = enhancer_saturation.enhance(0.5)
    augmented_images.extend([
        (f"{base_name}_bright", bright_image),
        (f"{base_name}_dark", dark_image),
        (f"{base_name}_saturated", saturated_image),
        (f"{base_name}_desaturated", desaturated_image)
    ])

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for image_name, img in augmented_images:
        file = f'{image_name}.{image_format}'
        output_path = os.path.join(output_path, file)
        img.save(output_path)
        output_path = output_path.removesuffix(file)


# python3 dataset_augmentation.py -ip /path/pokemons -op /path/out -is 128x128 -if png
def main():
    args = parse_args().parse_args()

    for filename in os.listdir(args.input_path):
        file_path = os.path.join(args.input_path, filename)
        perform(
            file_path,
            args.output_path,
            args.image_format
        )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-ip', '--input-path', type=str, help='path which contains train and test directories.', required=True
    )
    parser.add_argument(
        '-op', '--output-path', type=str, help='path where the generated dataset will be stored.', required=True
    )
    parser.add_argument(
        '-if', '--image-format', choices=['png', 'jpg'], help='image format.', required=True
    )
    return parser


if __name__ == '__main__':
    main()
