from abc import ABC, abstractmethod, abstractproperty

class IService(ABC):

    @abstractmethod
    def start_service(self): ...

    @abstractmethod
    def stop_service(self): ...