from abc import ABC, abstractmethod

class TyperBase(ABC):
    @abstractmethod
    def type_text(self, text: str) -> None:
        ...