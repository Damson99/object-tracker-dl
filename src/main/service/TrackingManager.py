from concurrent import futures

import cv2
import numpy
from torch import Tensor

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
        self._angle_executor = futures.ThreadPoolExecutor(1)

    def manage(self):
        tracking_id = 1
        tracking_object = None
        tracking_box = None
        while self._handler.is_opened():
            is_success, frame = self._handler.read()

            if not is_success:
                print("Video is empty.")
                break

            output_frame, boxes, boxes_xyxy = self._tracker.track(frame)
            if boxes.id is not None:
                tracked_ids = boxes.id.int().cpu().tolist()

                for box, tracked_id, class_name_cl, detection_probability in zip(
                        boxes_xyxy, tracked_ids, boxes.cls, boxes.conf.cpu().numpy()
                ):
                    self._screen_printer.handle_mouse(output_frame)
                    x_clicked, y_clicked = self._screen_printer.get_clicked_point()

                    tracked_record = self._tracker.build_record(class_name_cl, box, tracked_id, detection_probability)
                    tracking_box, tracking_object, new_tracking_id = self._update_tracking_object(
                        output_frame=output_frame,
                        box=box,
                        tracking_box=tracking_box,
                        tracked_record=tracked_record,
                        tracking_object=tracking_object,
                        tracking_id=tracking_id,
                        x_clicked=x_clicked,
                        y_clicked=y_clicked
                    )
                    tracking_id = new_tracking_id

                self._angle_executor.submit(self._handle_async, output_frame, tracking_box)

            self._screen_printer.show(output_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print("--- %s seconds ---" % TimeProvider.elapsed_time(self._start_time))
        self._handler.release()
        self._angle_executor.shutdown()
        self._track_object_repository.close()
        cv2.destroyAllWindows()

    def _update_tracking_object(
            self,
            output_frame: numpy.ndarray,
            box: Tensor,
            tracking_box: Tensor,
            tracked_record: TrackedRecord,
            tracking_object: TrackedRecord,
            tracking_id: int,
            x_clicked: int,
            y_clicked: int
    ):
        if box[0] < x_clicked < box[2] and box[1] < y_clicked < box[3]:
            tracking_id = tracked_record.tracked_id
        if tracking_id == tracked_record.tracked_id:
            tracking_box = box
            tracking_object = tracked_record
            deep_distance = self._distance_resolver.resolve(tracking_object.obj_height, tracking_object.obj_width)
            self._screen_printer.draw_tracked_data(output_frame, box, tracked_record, deep_distance)
        return tracking_box, tracking_object, tracking_id

    def _handle_async(self, output_frame: numpy.ndarray, tracking_box: Tensor):
        _, screen_width, _ = output_frame.shape
        angle_to_move = self._angle_resolver.resolve(tracking_box, screen_width)
        self._handler.move(angle_to_move)

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