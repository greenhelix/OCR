from abc import ABC, abstractmethod

class CorrectorBase(ABC):
    @abstractmethod
    def correct(self, results: list[dict]) -> list[dict]:
        ...