from abc import ABC, abstractmethod

class Command(ABC):
    """Command interface"""
    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def description(self) -> str:
        pass