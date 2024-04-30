from torch import Tensor

from service.clock import TimeProvider

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
        self.tracked_id = tracked_id
        self.class_name = class_name
        self.detection_probability = detection_probability
        self.obj_height = int(box[3] - box[1])
        self.obj_width = int(box[2] - box[0])
        self.elapsed_time = TimeProvider.elapsed_time(start_time)
