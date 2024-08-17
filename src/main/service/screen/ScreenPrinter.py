import cv2
import numpy

PIXELS_PER_METER = 200
TXT_COLOR = (0, 0, 0)
TXT_BACKGROUND = (255, 255, 255)
BOUND_BOX_COLOR = (255, 0, 255)
OBJECT_CENTROID_COLOR = (0, 0, 0)
TITLE = 'tracking'


class ScreenPrinter:
    def __init__(self):
        self._point_clicked = -1, -1

    def show(self, output_frame: numpy.ndarray):
        cv2.imshow(TITLE, output_frame)

    def handle_mouse(self, output_frame: numpy.ndarray):
        cv2.setMouseCallback(TITLE, self._click_event, output_frame)

    def get_clicked_point(self) -> tuple[int, int]:
        x, y = self._point_clicked
        self._point_clicked = -1, -1
        return x, y

    def _click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._point_clicked = x, y


