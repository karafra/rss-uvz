from abc import ABC, abstractmethod
from src.AbstractProcess import AbstractProcess
from typing import Type

class IService(ABC):

    @property
    @abstractmethod
    def _THREAD(self) -> Type[AbstractProcess]: ...
    
    @abstractmethod
    def start_service(self): ...

    @abstractmethod
    def stop_service(self): ...