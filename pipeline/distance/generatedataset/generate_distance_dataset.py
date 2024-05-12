import argparse

import pandas as pd

# Person who stand - distance from camera to person:
# height - 100% - 228 cm


def main(distance_to_object_with_full_height: int):
    lower_limit_percentage = 1
    upper_limit_percentage = 50

    percentage_range = list(range(1, 101))
    lower_limit_indicator = lower_limit_percentage / percentage_range[-1]
    upper_limit_indicator = upper_limit_percentage / percentage_range[-1]

    height_percentage_range_output = []
    width_percentage_range_output = []
    move_by_output = []

    for height_percentage in percentage_range:
        width_percentage_range_per_height = list(range(lower_limit_percentage + 1, upper_limit_percentage))
        lower_limit_percentage = int(lower_limit_indicator * height_percentage)
        upper_limit_percentage = int(upper_limit_indicator * height_percentage)

        for width_percentage in width_percentage_range_per_height:
            width_percentage_range_output.append(width_percentage)
            height_percentage_range_output.append(height_percentage)
            move_by_output.append(int(distance_to_object_with_full_height / float(height_percentage / 100)))

    for width_percentage in percentage_range:
        width_percentage_range_per_width = list(range(lower_limit_percentage + 1, upper_limit_percentage))
        lower_limit_percentage = int(lower_limit_indicator * width_percentage)
        upper_limit_percentage = int(upper_limit_indicator * width_percentage)

        for height_percentage in width_percentage_range_per_width:
            width_percentage_range_output.append(width_percentage)
            height_percentage_range_output.append(height_percentage)
            move_by_output.append(int(distance_to_object_with_full_height / float(width_percentage / 100)))

    data = pd.DataFrame({
        'width_percentage': width_percentage_range_output,
        'height_percentage': height_percentage_range_output,
        'move_by': move_by_output,
    })

    data.to_csv('distance_dataset.csv', index=False)


if __name__ == "__main__":
    # python3 generate_distance_dataset.py -od 228
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-od', '--object-distance', type=int, required=True,
                        help='distance in cm from camera to object when it has 100% height.')
    args = parser.parse_args()
    main(args.object_distance)
