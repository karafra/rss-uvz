from abc import ABC, abstractmethod, abstractproperty
import logging

class IService(ABC):

    __logger = logging.getLogger(__name__) 

    @abstractmethod
    def start_service(self): ...

    @abstractmethod
    def stop_service(self): ...