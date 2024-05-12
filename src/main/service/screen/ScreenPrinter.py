import cv2
import numpy
from torch import Tensor
from ultralytics.utils.plotting import Annotator

from main.service.track.TrackedObject import TrackedRecord

PIXELS_PER_METER = 200
TXT_COLOR = (0, 0, 0)
TXT_BACKGROUND = (255, 255, 255)
BOUND_BOX_COLOR = (255, 0, 255)
OBJECT_CENTROID_COLOR = (0, 0, 0)
TITLE = 'tracking'


class ScreenPrinter:
    def __init__(self):
        self._point_clicked = -1, -1

    def draw_tracked_data(self, frame, box, tracked_object: TrackedRecord, deep_distance):
        self._annotate_object(box, frame, tracked_object)
        centroid_box_point = self._centroid_box_points(box)

        text_size, _ = cv2.getTextSize(f"Distance: {deep_distance:.2f} m", cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
        cv2.rectangle(frame, (centroid_box_point[0], centroid_box_point[1] - text_size[1] - 10),
                      (centroid_box_point[0] + text_size[0] + 10, centroid_box_point[1]), TXT_BACKGROUND, -1)
        cv2.putText(frame, f"Distance: {deep_distance:.2f} m",
                    (centroid_box_point[0], centroid_box_point[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.2, TXT_COLOR, 3)

    def show(self, output_frame: numpy.ndarray):
        cv2.imshow(TITLE, output_frame)

    def handle_mouse(self, output_frame: numpy.ndarray):
        cv2.setMouseCallback(TITLE, self._click_event, output_frame)

    def get_clicked_point(self) -> tuple[int, int]:
        x, y = self._point_clicked
        self._point_clicked = -1, -1
        return x, y

    def _annotate_object(self, box, frame, tracked_object):
        h, w, _ = frame.shape
        center_point = h, w
        annotator = Annotator(frame, line_width=1)
        annotator.box_label(box, label=str(tracked_object.tracked_id), color=BOUND_BOX_COLOR)
        annotator.visioneye(box, center_point, OBJECT_CENTROID_COLOR, OBJECT_CENTROID_COLOR, 2, 5)

    def _centroid_box_points(self, box: Tensor):
        return int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)

    def _click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._point_clicked = x, y


