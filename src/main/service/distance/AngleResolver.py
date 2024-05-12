import joblib
import numpy as np
from torch import Tensor


class AngleResolver:
    def __init__(self, angle_model_path: str):
        self._angle_model = joblib.load(angle_model_path)

    def resolve(self, box: Tensor, screen_width: int) -> int:
        width_position_as_float = ((box[0] + box[2]) / 2) / screen_width
        width_position_in_percentage = int(width_position_as_float * 100)
        input_angle = np.array([[width_position_in_percentage]])
        return int(self._angle_model.predict(input_angle))
