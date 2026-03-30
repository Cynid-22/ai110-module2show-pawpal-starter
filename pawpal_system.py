from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Pet:
    Name: str
    Species: str
    Age: int
    SpecialRequirements: Optional[str] = None
    Tasks: List['Task'] = field(default_factory=list)

    def GetDetails(self) -> str:
        Reqs: str = self.SpecialRequirements if self.SpecialRequirements else "None"
        return f"{self.Name} the {self.Species} (Age: {self.Age}, Special Needs: {Reqs})"

    def UpdateDetails(self, Name: str, Species: str, Age: int, SpecialRequirements: str) -> None:
        self.Name = Name
        self.Species = Species
        self.Age = Age
        self.SpecialRequirements = SpecialRequirements

    def AddTask(self, NewTask: 'Task') -> None:
        self.Tasks.append(NewTask)

@dataclass
class Task:
    Description: str
    Duration: int
    PriorityLevel: int
    Frequency: str
    TargetPet: Pet
    IsCompleted: bool = False

    def MarkAsComplete(self) -> None:
        self.IsCompleted = True

    def UpdateDuration(self, NewDuration: int) -> None:
        self.Duration = NewDuration

    def UpdatePriority(self, NewPriority: int) -> None:
        self.PriorityLevel = NewPriority

class Owner:
    def __init__(self, Name: str, AvailableTime: int) -> None:
        self.Name: str = Name
        self.AvailableTime: int = AvailableTime
        self.Pets: List[Pet] = []

    def GetAvailableTime(self) -> int:
        return self.AvailableTime

    def UpdateAvailableTime(self, NewTime: int) -> None:
        self.AvailableTime = NewTime

    def AddPet(self, NewPet: Pet) -> None:
        self.Pets.append(NewPet)

    def GetAllTasks(self) -> List[Task]:
        AllTasks: List[Task] = []
        for PetItem in self.Pets:
            AllTasks.extend(PetItem.Tasks)
        return AllTasks

class Scheduler:
    def __init__(self, SystemOwner: Owner) -> None:
        self.SystemOwner: Owner = SystemOwner
        self.SelectedPlan: List[Task] = []

    def GenerateSchedule(self, AvailableTime: Optional[int] = None) -> List[Task]:
        Limit: int = AvailableTime if AvailableTime is not None else self.SystemOwner.AvailableTime
        AllTasks: List[Task] = self.SystemOwner.GetAllTasks()
        
        PendingTasks: List[Task] = [T for T in AllTasks if not T.IsCompleted]
        SortedTasks: List[Task] = sorted(PendingTasks, key=lambda T: T.PriorityLevel, reverse=True)
        
        self.SelectedPlan = []
        RemainingTime: int = Limit
        
        for TaskItem in SortedTasks:
            if TaskItem.Duration <= RemainingTime:
                self.SelectedPlan.append(TaskItem)
                RemainingTime -= TaskItem.Duration
                
        return self.SelectedPlan
