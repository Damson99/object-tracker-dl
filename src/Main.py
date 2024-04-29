import argparse
import cv2

from persistance.FileTrackObjectRepository import FileTrackObjectRepository
from screen.ScreenPrinter import ScreenPrinter
from clock import TimeProvider
from track.Tracker import Tracker


def process(args: argparse.Namespace, tracked_obj_repository: FileTrackObjectRepository):
    cap = cv2.VideoCapture(args.video_path)
    screen_width, screen_height = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
    center_point = (screen_width // 2, screen_height // 2)
    screen_printer = ScreenPrinter(center_point)
    start_time = TimeProvider.now()
    tracker = Tracker(
        tracking_model_path=args.tracking_model_path,
        distance_model_path=args.distance_model_path,
        angle_model_path=args.angle_model_path,
        model_confidence=args.model_confidence,
        track_object_repository=tracked_obj_repository,
        screen_printer=screen_printer,
        start_time=start_time
    )

    while cap.isOpened():
        is_success, frame = cap.read()

        if not is_success:
            print("Video is empty.")
            break

        result = tracker.run(frame)
        screen_printer.show(result.plot())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("--- %s seconds ---" % TimeProvider.elapsed_time(start_time))
    tracked_obj_repository.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-vp', '--video-path', type=str, required=True,
                        help='Path to video that will be processed.')
    parser.add_argument('-tmp', '--tracking-model-path', type=str, required=True,
                        help='Path to tracking model.')
    parser.add_argument('-dmp', '--distance-model-path', type=str, required=False,
                        help='Path to distance model.')
    parser.add_argument('-amp', '--angle-model-path', type=str, required=False,
                        help='Path to angle model.')
    parser.add_argument('-mc', '--model-confidence', type=float, required=False, default=0.7,
                        help='Model confidence of detected class.')

    process(parser.parse_args(), FileTrackObjectRepository())
