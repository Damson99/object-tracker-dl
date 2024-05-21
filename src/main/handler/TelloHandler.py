import random
import time
from threading import Thread

from djitellopy import Tello
from sympy import true

from main.handler import TelloReceiverHandler
from main.handler.Handler import Handler


# DOCS https://djitellopy.readthedocs.io/en/latest/tello/

class TelloHandler(Handler):

    def __init__(self):
        self._drone_client = Tello()
        self._drone_client.connect()
        self._drone_client.streamon()
        Tello.RESPONSE_TIMEOUT = 0.1

        print(self._drone_client.get_battery())

        self._drone_client.set_speed(100)
        self._drone_client.takeoff()

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
        try:
            self._drone_client.rotate_clockwise(int(angle))
            if move_by > 20:
                if move_by > 500:
                    move_by = 500
                self._drone_client.move_forward(int(move_by))
            else:
                if move_by < -20:
                    if move_by < -500:
                        move_by = -500
                    self._drone_client.move_back(int(move_by))
        except Exception as e:
            print('error while sending command {}'.format(e))
