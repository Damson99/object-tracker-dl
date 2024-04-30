import argparse

from service.TrackingManager import TrackingManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-vp', '--video-path', type=str, required=False,
                        help='Path to video that will be processed.')
    parser.add_argument('-ds', '--drone-source', type=bool, required=False,
                        help='Informs program that it should use drone as a camera source. '
                             'Before that, there is a need to connect to the drone\'s wifi network')
    parser.add_argument('-tmp', '--tracking-model-path', type=str, required=True,
                        help='Path to tracking model.')
    parser.add_argument('-dmp', '--distance-model-path', type=str, required=False,
                        help='Path to distance model.')
    parser.add_argument('-amp', '--angle-model-path', type=str, required=False,
                        help='Path to angle model.')
    parser.add_argument('-mc', '--model-confidence', type=float, required=False, default=0.7,
                        help='Model confidence of detected class.')

    args = parser.parse_args()
    TrackingManager(
        video_path=args.video_path,
        is_drone_source=args.drone_source,
        distance_model_path=args.distance_model_path,
        angle_model_path=args.angle_model_path,
        tracking_model_path=args.tracking_model_path,
        model_confidence=args.model_confidence
    ).manage()
