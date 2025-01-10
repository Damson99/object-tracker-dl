from abc import ABC

from djitellopy import Tello
from sympy import true

from main.handler.Handler import Handler


# DOCS https://djitellopy.readthedocs.io/en/latest/tello/

class TelloHandler(Handler, ABC):

    def __init__(self):
        super().__init__()
        self._drone_client = Tello()
        self._drone_client.connect()
        print(self._drone_client.get_battery())
        self._drone_client.streamon()

    def run(self):
        pass
        self._drone_client.takeoff()
        # self._drone_client.move_up(50)

    def is_opened(self) -> bool:
        return true

    def get_center_point(self) -> tuple[int, int]:
        _, frame = self.read()
        h, w, _ = frame.shape
        return int(h / 2), int(w / 2)

    def read(self):
        return true, self._drone_client.get_frame_read().frame

    def release(self):
        self._drone_client.land()

    def move(self, angle: int, move_by: int):
        print("move_by", move_by)
        self._drone_client.send_rc_control(
            int(0),
            int(move_by),
            int(0),
            int(angle)
        )
