import csv

from webencodings import UTF8

from service.track.TrackedObject import FIELDNAMES, TrackedRecord


class FileTrackObjectRepository:

    def __init__(self):
        self.file = open('tracked_data.csv', 'a', encoding=UTF8.name, newline='')
        self.file.truncate(0)
        self.writer = csv.DictWriter(self.file, fieldnames=FIELDNAMES)
        self.writer.writeheader()

    def save_record(self, tracked_record: TrackedRecord):
        tracked_record = {
            FIELDNAMES[0]: tracked_record.tracked_id,
            FIELDNAMES[1]: tracked_record.class_name,
            FIELDNAMES[2]: tracked_record.detection_probability,
            FIELDNAMES[3]: tracked_record.obj_height,
            FIELDNAMES[4]: tracked_record.obj_width,
            FIELDNAMES[5]: tracked_record.elapsed_time,
        }
        self.writer.writerow(tracked_record)

    def close(self):
        self.file.close()
