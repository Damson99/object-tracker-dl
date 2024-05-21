import numpy
from torch import Tensor
from ultralytics import YOLO

from main.persistance import FileTrackObjectRepository
from main.service.track.TrackedObject import TrackedRecord


class Tracker:

    def __init__(
            self,
            tracking_model_path: str,
            model_confidence: float,
            track_object_repository: FileTrackObjectRepository,
            start_time: float
    ):
        self._tracking_model = YOLO(tracking_model_path)
        self._model_confidence = model_confidence
        self._track_object_repository = track_object_repository
        self._start_time = start_time

    def track(self, frame: numpy.ndarray) -> tuple:
        results: list = self._tracking_model.track(frame, verbose=False, persist=True, conf=self._model_confidence)
        boxes = results[0].boxes
        boxes_xyxy = boxes.xyxy.cpu()
        return results[0].plot(), boxes, boxes_xyxy

    def build_record(self, class_name_cl, box: Tensor, tracked_id: int, detection_probability: float) -> TrackedRecord:
        class_name = self._tracking_model.names[int(class_name_cl)]
        tracked_record = TrackedRecord(
            box=box,
            class_name=class_name,
            detection_probability=detection_probability,
            start_time=self._start_time,
            tracked_id=tracked_id
        )
        # self._track_object_repository.save_record(tracked_record)
        return tracked_record

