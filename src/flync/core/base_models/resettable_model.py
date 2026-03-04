from abc import ABC, abstractmethod


class BaseRegistry(ABC):

    @classmethod
    @abstractmethod
    def reset(cls):
        """Reset function to clear the registry."""
