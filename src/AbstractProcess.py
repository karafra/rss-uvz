from multiprocessing import Queue
from abc import ABC, abstractmethod
from typing import Union, Callable, Any
from multiprocessing.context import Process


class AbstractProcess(Process, ABC):

    def __init__(self, target: Union[Callable[..., Any]]):
        super().__init__()
        self.daemon: bool = True
        self.queue: Queue = Queue()
        self.args_queue: Queue = Queue()
        self.target: Union[Callable[..., Any]] = target
        self.process = Process(target=self._thread_function)
        self.process.start()

    def _stop(self) -> None:
        """Kills thread with the process"""
        self.queue.close()
        self.process.kill()

    @abstractmethod
    def _thread_function(self) -> None:
        """
        Continuously runs function supplied in target argument
        to construtor, and stores results in queue.
        """
