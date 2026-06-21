from abc import ABC, abstractclassmethod

class TyperBase(ABC):
    @abstractclassmethod
    def type_text(self, text: str) -> None:
        ...