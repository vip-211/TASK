
from abc import ABC, abstractmethod
from typing import Any
from utils.logger import setup_logger


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"agent.{name}")

    @abstractmethod
    def execute(self, state: Any) -> Any:
        pass
