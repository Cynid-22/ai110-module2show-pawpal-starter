from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Pet:
    Name: str
    Species: str
    Age: int
    SpecialRequirements: Optional[str] = None

    def GetDetails(self) -> str:
        pass

    def UpdateDetails(self, Name: str, Species: str, Age: int, SpecialRequirements: str) -> None:
        pass

@dataclass
class Task:
    Name: str
    Duration: int
    PriorityLevel: str
    IsCompleted: bool = False

    def MarkAsComplete(self) -> None:
        pass

    def UpdateDuration(self, NewDuration: int) -> None:
        pass

    def UpdatePriority(self, NewPriority: str) -> None:
        pass

class Owner:
    def __init__(self, Name: str, AvailableTime: int) -> None:
        self.Name: str = Name
        self.AvailableTime: int = AvailableTime
        self.Pets: List[Pet] = []

    def GetAvailableTime(self) -> int:
        pass

    def UpdateAvailableTime(self, NewTime: int) -> None:
        pass

    def AddPet(self, NewPet: Pet) -> None:
        pass

class Scheduler:
    def __init__(self) -> None:
        self.AllTasks: List[Task] = []
        self.SelectedPlan: List[Task] = []
        self.RemainingTime: int = 0

    def AddTask(self, NewTask: Task) -> None:
        pass

    def RemoveTask(self, TaskToRemove: Task) -> None:
        pass

    def GenerateSchedule(self, AvailableTime: int) -> None:
        pass
