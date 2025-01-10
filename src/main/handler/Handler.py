from abc import abstractmethod, ABC

import numpy


class Handler(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def is_opened(self) -> bool:
        pass

    @abstractmethod
    def get_center_point(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def read(self) -> tuple[bool, numpy.ndarray]:
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def move(self, angle: int, deep_distance: int):
        pass
