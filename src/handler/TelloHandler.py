from djitellopy import Tello
from sympy import true

from handler.Handler import Handler


# DOCS https://djitellopy.readthedocs.io/en/latest/tello/

class TelloHandler(Handler):

    def __init__(self):
        self._drone_client = Tello()
        self._drone_client.connect()
        self._drone_client.streamon()
        # self._drone_client.takeoff()

    def is_opened(self) -> bool:
        return true

    def get_center_point(self) -> tuple[int, int]:
        _, frame = self.read()
        h, w, _ = frame.shape
        return h // 2, w // 2

    def read(self):
        return true, self._drone_client.get_frame_read().frame

    def release(self):
        self._drone_client.land()