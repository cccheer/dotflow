from abc import ABC, abstractmethod


class ServicePlugin(ABC):
    plugin_type: str

    @abstractmethod
    def validate_config(self, config: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate(self, config: dict) -> dict:
        raise NotImplementedError
