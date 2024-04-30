from abc import abstractmethod


class Handler:

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
