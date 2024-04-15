import csv

FIELDNAMES = [
    'tracked_id',
    'detected_class_name',
    'detection_probability',
    'detected_object_width',
    'detected_object_height',
    'detection_time_in_sec'
]


class RecordWriter:

    def __init__(self):
        self.file = open('tracked_data.csv', 'a', encoding='UTF8', newline='')
        self.file.truncate(0)
        self.writer = csv.DictWriter(self.file, fieldnames=FIELDNAMES)
        self.writer.writeheader()

    def save_record(self, tracked_attributes):
        tracked_record = {
            FIELDNAMES[0]: tracked_attributes[0],
            FIELDNAMES[1]: tracked_attributes[1],
            FIELDNAMES[2]: tracked_attributes[2],
            FIELDNAMES[3]: tracked_attributes[3],
            FIELDNAMES[4]: tracked_attributes[4],
            FIELDNAMES[5]: tracked_attributes[5],
        }
        self.writer.writerow(tracked_record)

    def close(self):
        self.file.close()
