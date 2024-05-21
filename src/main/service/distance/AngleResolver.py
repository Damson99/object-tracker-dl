import joblib
import numpy as np


class AngleResolver:
    def __init__(self, angle_model_path: str):
        self._angle_model = joblib.load(angle_model_path)

    def resolve(self, width_position_in_percentage: int) -> int:
        input_angle = np.array([[width_position_in_percentage]])
        return int(self._angle_model.predict(input_angle))
