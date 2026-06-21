from abc import ABC, abstractclassmethod

class CorrectorBase(ABC):
    @abstractclassmethod
    def correct(self, results: list[dict]) -> list[dict]:
        ...