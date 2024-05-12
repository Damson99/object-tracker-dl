import argparse

import pandas as pd


def main(half_camera_angle_visibility: int):
    width_percentage_range = list(range(1, 101))
    angle = []

    for width_percentage in width_percentage_range:
        if width_percentage < 50:
            angle.append(int((width_percentage / 49) * half_camera_angle_visibility - half_camera_angle_visibility))
        elif width_percentage >= 50:
            angle.append(int(((width_percentage - 50) / 50) * half_camera_angle_visibility))

    data = pd.DataFrame({
        'width_percentage': width_percentage_range,
        'angle': angle,
    })

    data.to_csv('width_angle_dataset.csv', index=False)


if __name__ == "__main__":
    # python3 generate_angle_dataset.py -av 30
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-av', '--angle-visibility', type=int, required=True,
                        help='camera angle visibility in degrees.')
    args = parser.parse_args()
    main(int(args.angle_visibility / 2))
