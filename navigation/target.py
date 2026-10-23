from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationTarget:
    x: float
    y: float