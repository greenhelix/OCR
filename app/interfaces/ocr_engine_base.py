from abc import ABC, abstractmethod
import numpy as np

class OCREngineBase(ABC):
    @abstractmethod
    def recognize(self, frame: np.ndarray) -> list[dict]:
        ...

