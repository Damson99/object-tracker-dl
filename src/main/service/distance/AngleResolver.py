import joblib
import numpy as np
from torch import Tensor


class AngleResolver:
    def __init__(self, angle_model_path: str, screen_width_center: int):
        self._angle_model = joblib.load(angle_model_path)
        self._screen_width = screen_width_center * 2

    def resolve(self, box: Tensor) -> int:
        width_position_as_float = ((box[0] + box[2]) / 2) / self._screen_width
        width_position_in_percentage = int(width_position_as_float * 100)
        print(width_position_in_percentage)
        input_angle = np.array([[width_position_in_percentage]])
        return int(self._angle_model.predict(input_angle))
