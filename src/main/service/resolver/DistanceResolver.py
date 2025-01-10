class DistanceResolver:

    def resolve(self, height_as_percentage: int) -> int:
        if 90 > height_as_percentage > 80:
            return 0
        if height_as_percentage > 90:
            return -20
        else:
            return 20
