from abc import ABC, abstractmethod


class Solver(ABC):
    @abstractmethod
    def solve(msg: str) -> None:
        pass
