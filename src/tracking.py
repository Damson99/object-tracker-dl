import time
import cv2
import sys
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

from RecordWriter import RecordWriter

PIXELS_PER_METER = 200
TXT_COLOR, TXT_BACKGROUND, BOUND_BOX_COLOR, OBJECT_CENTROID_COLOR = ((0, 0, 0), (255, 255, 255), (255, 0, 255), (0, 0, 0))
MAX_HEIGHT_FOR_PERSON = 540
METERS_FROM_CAMERA_WHEN_MAX_HEIGHT_PER_PERSON = 2


def track(model_path, video_path, record_writer):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    center_point = (w // 2, h // 2)
    out = cv2.VideoWriter('tracking.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h))

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Video is empty.")
            break

        annotator = Annotator(frame, line_width=1)
        results = model.track(frame, verbose=False, persist=True, conf=0.7)
        boxes = results[0].boxes.xyxy.cpu()

        if results[0].boxes.id is not None:
            tracked_ids = results[0].boxes.id.int().cpu().tolist()

            for box, tracked_id in zip(boxes, tracked_ids):
                obj_height = int(box[3] - box[1])
                obj_width = int(box[2] - box[0])
                save_tracked_result(obj_height, obj_width, record_writer, start_time, tracked_id)

                annotator.box_label(box, label=str(tracked_id), color=BOUND_BOX_COLOR)
                annotator.visioneye(box, center_point, OBJECT_CENTROID_COLOR, OBJECT_CENTROID_COLOR, 2, 5)
                draw_tracked_data(frame, box, obj_height)

        out.write(frame)
        cv2.imshow("tracking", results[0].plot())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("--- %s seconds ---" % elapse_time(start_time))
    record_writer.close()
    out.release()
    cap.release()
    cv2.destroyAllWindows()


def save_tracked_result(obj_height, obj_width, record_writer, start_time, tracked_id):
    elapsed_time = elapse_time(start_time)
    record_writer.save_record([tracked_id, 'person', 0.7, obj_height, obj_width, elapsed_time])  # make this async and get real class name with probability


def elapse_time(start_time):
    return time.time() - start_time


def draw_tracked_data(frame, box, obj_height):
    centroid_box_point = centroid_box_points(box)
    absolute_distance = compute_absolute_distance(obj_height)

    text_size, _ = cv2.getTextSize(f"Distance: {absolute_distance:.2f} m", cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
    cv2.rectangle(frame, (centroid_box_point[0], centroid_box_point[1] - text_size[1] - 10),
                  (centroid_box_point[0] + text_size[0] + 10, centroid_box_point[1]), TXT_BACKGROUND, -1)
    cv2.putText(frame, f"Distance: {absolute_distance:.2f} m",
                (centroid_box_point[0], centroid_box_point[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.2, TXT_COLOR, 3)


def centroid_box_points(box):
    return int((box[0] + box[2]) // 2), int((box[1] + box[3]) // 2)


def compute_absolute_distance(obj_height):
    return compute_deep_distance(obj_height)


# def euclidean_distance(center_point, other_point):
#     return math.sqrt((other_point[0] - center_point[0]) ** 2 + (other_point[1] - center_point[1]) ** 2)


def compute_deep_distance(obj_height):
    return METERS_FROM_CAMERA_WHEN_MAX_HEIGHT_PER_PERSON / (obj_height / MAX_HEIGHT_FOR_PERSON)


if __name__ == "__main__":
    model_path = str(sys.argv[1])
    video_path = str(sys.argv[2])
    record_writer = RecordWriter()

    track(model_path, video_path, record_writer)
