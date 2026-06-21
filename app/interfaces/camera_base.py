from abc import ABC, abstractmethod

class CameraBase(ABC):
    @abstractmethod
    def open(self) -> None: ...


