import argparse
import os

from PIL import Image, ImageOps, ImageEnhance


def perform(
        input_path: str,
        output_path: str,
        image_format: str,
        image_size_x_y: tuple[int, int],
):
    image = Image.open(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    augmented_images = [(f"{base_name}_original", image)]

    rotated_90 = image.rotate(90, expand=True)
    rotated_180 = image.rotate(180, expand=True)
    rotated_270 = image.rotate(270, expand=True)
    augmented_images.extend([
        (f"{base_name}_rotated_90", rotated_90),
        (f"{base_name}_rotated_180", rotated_180),
        (f"{base_name}_rotated_270", rotated_270)
    ])

    rotated_15 = image.rotate(15, expand=True)
    rotated_30 = image.rotate(30, expand=True)
    augmented_images.extend([
        (f"{base_name}_rotated_15", rotated_15),
        (f"{base_name}_rotated_30", rotated_30)
    ])

    flipped_horizontal = ImageOps.mirror(image)
    flipped_vertical = ImageOps.flip(image)
    augmented_images.extend([
        (f"{base_name}_flipped_horizontal", flipped_horizontal),
        (f"{base_name}_flipped_vertical", flipped_vertical)
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
        output_path = os.path.join(output_path, f'{image_name:03d}.{image_format}')
        img = img.resize(image_size_x_y)
        img.save(output_path)


# python3 dataset_augmentation.py -ip /path/pokemons -op /path/out -is 128x128 -if png -gm
def main():
    args = parse_args().parse_args()
    image_size_arr = args.image_size.lower().split('x')

    for filename in os.listdir(args.input_path):
        file_path = os.path.join(args.input_path, filename)
        perform(
            file_path,
            args.output_path,
            args.image_format,
            (int(image_size_arr[0]), int(image_size_arr[1]))
        )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--input-path', type=str, help='path which contains train and test directories.')
    parser.add_argument('-op', '--output-path', type=str, help='path where the generated dataset will be stored.')
    parser.add_argument('-if', '--image-format', choices=['png', 'jpg'], help='image format.')
    parser.add_argument('-is', '--image-size', type=str, help='size of the output images, format INTxINT.')
    return parser


if __name__ == '__main__':
    main()
