import argparse

import pandas as pd

# Person who stand - distance from camera to person:
# height - 100% - 228 cm


def main(distance_to_object_with_full_height: int, stay_away_from_object_distance: int):
    lower_limit_percentage = 10
    upper_limit_percentage = 70

    percentage_range = list(range(30, 101))
    lower_limit_indicator = lower_limit_percentage / percentage_range[-1]
    upper_limit_indicator = upper_limit_percentage / percentage_range[-1]

    height_percentage_range_output = []
    move_by_output = []

    for height_percentage in percentage_range:
        lower_limit_percentage = int(lower_limit_indicator * height_percentage)
        upper_limit_percentage = int(upper_limit_indicator * height_percentage)

        height_percentage_range_output.append(height_percentage)
        move_by = int(distance_to_object_with_full_height / float(height_percentage / 100))
        # if move_by > stay_away_from_object_distance:
        move_by = move_by - stay_away_from_object_distance
        # elif stay_away_from_object_distance > move_by > 0:
        #     move_by = stay_away_from_object_distance - move_by
        # else:
        #     move_by = move_by + stay_away_from_object_distance
        move_by_output.append(move_by)

    data = pd.DataFrame({
        'height_percentage': height_percentage_range_output,
        'move_by': move_by_output,
    })

    data.to_csv('distance_dataset.csv', index=False)


if __name__ == "__main__":
    # python3 generate_distance_dataset.py -od 228 -sa 500
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-od', '--object-real-distance', type=int, required=True,
                        help='distance in cm from camera to object when it has 100% height.', )
    parser.add_argument('-sa', '--stay-away-distance', type=int, default=500,
                        help='a constant from which the drone is to stay away from the object in cm.', )
    args = parser.parse_args()

    stay_away_distance = args.stay_away_distance
    if stay_away_distance < 0:
        stay_away_distance = stay_away_distance * -1
    main(args.object_real_distance, stay_away_distance)
