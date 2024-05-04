MAX_HEIGHT_FOR_PERSON = 540
METERS_FROM_CAMERA_WHEN_MAX_HEIGHT_PER_PERSON = 2


class DistanceResolver:
    def __init__(self, distance_model_path: str):
        self._distance_model_path = distance_model_path  # todo add model

    def resolve(self, obj_height, obj_width):
        return METERS_FROM_CAMERA_WHEN_MAX_HEIGHT_PER_PERSON / (obj_height / MAX_HEIGHT_FOR_PERSON)
