from sympy.utilities.codegen import Result
from ultralytics import YOLO

from distance.AngleResolver import AngleResolver
from distance.DistanceResolver import DistanceResolver
from persistance import FileTrackObjectRepository
from screen.ScreenPrinter import ScreenPrinter
from track.TrackedObject import TrackedRecord


class Tracker:

    def __init__(
            self,
            tracking_model_path: str,
            distance_model_path: str,
            angle_model_path: str,
            model_confidence: float,
            track_object_repository: FileTrackObjectRepository,
            screen_printer: ScreenPrinter,
            start_time: float
    ):
        self._tracking_model = YOLO(tracking_model_path)
        self._distance_resolver = DistanceResolver(distance_model_path)
        self._angle_resolver = AngleResolver(angle_model_path)
        self._model_confidence = model_confidence
        self._track_object_repository = track_object_repository
        self._screen_printer = screen_printer
        self._start_time = start_time

    def run(self, frame) -> Result:
        results: list = self._tracking_model.track(frame, verbose=False, persist=True, conf=self._model_confidence)
        boxes = results[0].boxes
        boxes_xyxy = boxes.xyxy.cpu()

        if boxes.id is not None:
            tracked_ids = boxes.id.int().cpu().tolist()

            for box, tracked_id, class_name_cl, detection_probability in zip(
                    boxes_xyxy, tracked_ids, boxes.cls, boxes.conf.cpu().numpy()
            ):
                class_name = self._tracking_model.names[int(class_name_cl)]
                tracked_record: TrackedRecord = TrackedRecord(
                    box=box,
                    class_name=class_name,
                    detection_probability=detection_probability,
                    start_time=self._start_time,
                    tracked_id=tracked_id
                )
                deep_distance = self._distance_resolver.resolve(tracked_record.obj_height, tracked_record.obj_width)  # todo to optimize, do it for following object
                self._track_object_repository.save_record(tracked_record)  # todo could be async
                self._screen_printer.draw_tracked_data(frame, box, tracked_record, deep_distance)
        return results[0]
