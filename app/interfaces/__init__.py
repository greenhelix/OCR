from abc import ABC, abstractmethod
import numpy as np

class CameraBase(ABC):
    
    @abstractmethod
    def open(self) -> None: ... # camera conn open

    @abstractmethod
    def read(self) -> np.ndarray: ... # frame 1 retrun 

    @abstractmethod
    def release(self) -> None: ... # camera conn close

