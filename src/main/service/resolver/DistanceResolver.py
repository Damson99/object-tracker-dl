class DistanceResolver:

    def resolve(self, height_as_percentage: int) -> int:
        if 90 > height_as_percentage > 80:
            return 0
        if height_as_percentage > 90:
            return -40
        else:
            return 40
