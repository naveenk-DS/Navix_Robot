from abc import ABC, abstractmethod


class MotionController(ABC):
    @abstractmethod
    def move_forward(self, distance: float) -> None:
        """Move the robot forward by the requested distance."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stop all robot movement."""
        raise NotImplementedError


class SimulatedMotionController(MotionController):
    def move_forward(self, distance: float) -> None:
        print(f"[SIMULATION] Moving forward {distance} meter(s).")

    def stop(self) -> None:
        print("[SIMULATION] Robot stopped.")
