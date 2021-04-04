from abc import ABC, abstractmethod
from src.AbstractProcess import AbstractProcess
from typing import Type

class IService(ABC):

    def __init__(self) -> None:
        self.process = None
        super().__init__()

    @property
    @abstractmethod
    def _PROCESS(self) -> Type[AbstractProcess]: ...

    @abstractmethod
    def start_service(self): ...

    @abstractmethod
    def stop_service(self): ...

    @abstractmethod
    def interact(self, *args, **kwargs): ...