from concurrent import futures

import cv2

from main.handler.FileHandler import FileHandler
from main.handler.Handler import Handler
from main.handler.TelloHandler import TelloHandler
from main.persistance.FileTrackObjectRepository import FileTrackObjectRepository
from main.service.clock import TimeProvider
from main.service.distance.AngleResolver import AngleResolver
from main.service.distance.DistanceResolver import DistanceResolver
from main.service.screen.ScreenPrinter import ScreenPrinter
from main.service.track.TrackedObject import TrackedRecord
from main.service.track.Tracker import Tracker


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

        self._valid_should_provide_single_source(is_drone_source, video_path)
        self._valid_model_confidence(model_confidence)

        self._handler = self._choose_handler(is_drone_source, video_path)
        self._screen_printer = ScreenPrinter()
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
        self._command_consumer_executor = futures.ThreadPoolExecutor(1)

    def manage(self):
        tracking_id = 1
        tracking_record = None
        while self._handler.is_opened():
            is_success, frame = self._handler.read()

            if not is_success:
                print("Video is empty.")
                break

            output_frame, boxes, boxes_xyxy = self._tracker.track(frame)
            if boxes.id is not None:
                tracked_ids = boxes.id.int().cpu().tolist()
                screen_height, screen_width, _ = output_frame.shape

                for box, tracked_id, class_name_cl, detection_probability in zip(
                        boxes_xyxy, tracked_ids, boxes.cls, boxes.conf.cpu().numpy()
                ):
                    self._screen_printer.handle_mouse(output_frame)
                    x_clicked, y_clicked = self._screen_printer.get_clicked_point()

                    tracked_record = self._tracker.build_record(class_name_cl, box, tracked_id, detection_probability)
                    tracking_record = self._update_tracking_object(
                        tracked_record=tracked_record,
                        tracking_record=tracking_record,
                        tracking_id=tracking_id,
                        x_clicked=x_clicked,
                        y_clicked=y_clicked
                    )
                    tracking_id = tracking_record.get_tracked_id()

                x_position_percentage = tracking_record.get_x_position_percentage(screen_width)
                y_position_percentage = tracking_record.get_y_position_percentage(screen_height)
                move_by = self._distance_resolver.resolve(y_position_percentage, x_position_percentage)
                angle = self._angle_resolver.resolve(x_position_percentage)
                print('angle {}, move_by {}'.format(angle, move_by))
                self._command_consumer_executor.submit(self._handler.move, angle, move_by)

            self._screen_printer.show(output_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print("--- %s seconds ---" % TimeProvider.elapsed_time(self._start_time))
        self._handler.release()
        self._command_consumer_executor.shutdown()
        self._track_object_repository.close()
        cv2.destroyAllWindows()

    def _update_tracking_object(
            self,
            tracked_record: TrackedRecord,
            tracking_record: TrackedRecord,
            tracking_id: int,
            x_clicked: int,
            y_clicked: int
    ):
        tracked_box = tracked_record.get_box()
        if tracked_box[0] < x_clicked < tracked_box[2] and tracked_box[1] < y_clicked < tracked_box[3]:
            tracking_id = tracked_record.get_tracked_id()
        if tracking_id == tracked_record.get_tracked_id():
            tracking_record = tracked_record
        return tracking_record

    def _choose_handler(self, is_drone_source, video_path) -> Handler:
        if is_drone_source:
            return TelloHandler()
        else:
            return FileHandler(video_path)

    def _valid_should_provide_single_source(self, is_drone_source, video_path):
        if video_path is not None and is_drone_source:
            raise ValueError('video-path and drone-source are passed as arguments, choose one.')

    def _valid_model_confidence(self, model_confidence):
        conf_as_str_len = len(str(model_confidence))
        if (model_confidence is None
                or (model_confidence > 1.0 > model_confidence
                    or conf_as_str_len != 3)):
            raise ValueError('invalid model-confidence parameter. Should be value in range 0.1 - 1.0.')
