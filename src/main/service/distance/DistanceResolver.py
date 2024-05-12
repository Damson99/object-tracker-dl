import joblib
import numpy


class DistanceResolver:
    def __init__(self, distance_model_path: str):
        self._distance_model = joblib.load(distance_model_path)

    def resolve(self, height_position_in_percentage: int, width_position_in_percentage: int) -> int:
        return self._distance_model.predict([[height_position_in_percentage, width_position_in_percentage]])[0]
