from torch import Tensor

from main.service.clock import TimeProvider

FIELDNAMES = [
    'tracked_id',
    'detected_class_name',
    'detection_probability',
    'detected_object_width',
    'detected_object_height',
    'detection_time_in_sec'
]


class TrackedRecord:
    def __init__(self, box: Tensor, class_name: str, detection_probability: float, start_time: float, tracked_id: int):
        self._box = box
        self._tracked_id = tracked_id
        self._class_name = class_name
        self._detection_probability = detection_probability
        self._obj_height = int(self._box[3] - self._box[1])
        self._obj_width = int(self._box[2] - self._box[0])
        self._elapsed_time = TimeProvider.elapsed_time(start_time)

    def get_tracked_id(self):
        return self._tracked_id

    def get_class_name(self):
        return self._class_name

    def get_detection_probability(self):
        return self._detection_probability

    def get_height(self):
        return self._obj_height

    def get_width(self):
        return self._obj_width

    def get_elapsed_time(self):
        return self._elapsed_time

    def get_box(self):
        return self._box
