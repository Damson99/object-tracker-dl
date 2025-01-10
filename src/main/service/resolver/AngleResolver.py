class AngleResolver:

    HALF_OF_SCREEN = 50

    def resolve(self, width_position_in_percentage: int) -> int:
        return (width_position_in_percentage - self.HALF_OF_SCREEN) * 2
