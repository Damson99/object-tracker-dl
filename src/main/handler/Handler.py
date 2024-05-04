from abc import abstractmethod, ABC


class Handler(ABC):

    @abstractmethod
    def is_opened(self) -> bool:
        pass

    @abstractmethod
    def get_center_point(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def read(self) -> tuple:
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def move(self, angle_to_move):
        pass
