from djitellopy import Tello
from sympy import true

from main.handler.Handler import Handler


# DOCS https://djitellopy.readthedocs.io/en/latest/tello/

class TelloHandler(Handler):

    def __init__(self):
        self._drone_client = Tello()
        self._drone_client.connect()
        print(self._drone_client .get_battery())
        self._drone_client.streamon()
        self._drone_client.set_speed(100)
        # self._drone_client.takeoff()

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

    def move(self, angle: int, deep_distance: int):
        print(deep_distance)
        try:
            # self._drone_client.rotate_clockwise(angle)
            self._drone_client.go_xyz_speed_yaw_mid(
                0,
                0,
                int(deep_distance),
                50,
                int(angle),
                0,
                0
            )
        except Exception as e:
            print('error while sending command {}'.format(e))
