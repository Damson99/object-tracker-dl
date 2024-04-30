import cv2

from handler.FileHandler import FileHandler
from handler.TelloHandler import TelloHandler
from service.distance.AngleResolver import AngleResolver
from service.distance.DistanceResolver import DistanceResolver
from persistance.FileTrackObjectRepository import FileTrackObjectRepository
from service.screen.ScreenPrinter import ScreenPrinter
from service.clock import TimeProvider
from service.track.Tracker import Tracker


class TrackingManager:
    def __init__(
            self,
            video_path: str,
            is_drone_source: bool,
            distance_model_path: str,
            angle_model_path: str,
            tracking_model_path: str,
            model_confidence: float
    ):

        if video_path is not None and is_drone_source:
            raise ValueError('video-path and drone-source are passed as arguments, choose one.')

        conf_as_str_len = len(str(model_confidence))
        if (model_confidence is None
                or (model_confidence > 1.0 > model_confidence
                    or conf_as_str_len != 3)):
            raise ValueError('invalid model-confidence parameter. Should be value in range 0.1 - 1.0.')

        self._distance_resolver = DistanceResolver(distance_model_path)
        self._angle_resolver = AngleResolver(angle_model_path)
        self._track_object_repository = FileTrackObjectRepository()
        self._start_time = TimeProvider.now()
        self._tracker = Tracker(
            tracking_model_path=tracking_model_path,
            model_confidence=model_confidence,
            track_object_repository=self._track_object_repository,
            start_time=self._start_time
        )
        if is_drone_source:
            self._handler = TelloHandler()
        else:
            self._handler = FileHandler(video_path)

        center_point = self._handler.get_center_point()
        self._screen_printer = ScreenPrinter(center_point)

    def manage(self):
        while self._handler.is_opened():
            is_success, frame = self._handler.read()

            if not is_success:
                print("Video is empty.")
                break

            results, boxes, boxes_xyxy = self._tracker.track(frame)
            if boxes.id is not None:
                tracked_ids = boxes.id.int().cpu().tolist()

                for box, tracked_id, class_name_cl, detection_probability in zip(
                        boxes_xyxy, tracked_ids, boxes.cls, boxes.conf.cpu().numpy()
                ):
                    tracked_record = self._tracker.build_record(class_name_cl, box, tracked_id, detection_probability)
                    deep_distance = self._distance_resolver.resolve(tracked_record.obj_height,
                                                                    tracked_record.obj_width)  # todo to optimize, do it for following object
                    self._screen_printer.draw_tracked_data(frame, box, tracked_record, deep_distance)

            self._screen_printer.show(results[0].plot())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._handler.release()
                break

        print("--- %s seconds ---" % TimeProvider.elapsed_time(self._start_time))
        self._track_object_repository.close()
        self._handler.release()
        cv2.destroyAllWindows()
